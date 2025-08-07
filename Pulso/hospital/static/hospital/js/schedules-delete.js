document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".btn-excluir-escala").forEach(function (botao) {
        botao.addEventListener("click", excluirEscala);
    });
});

function excluirEscala(event) {
    event.preventDefault();

    const botao = event.currentTarget;
    const idEscala = botao.dataset.id;

    console.log("Antes do modal:", idEscala);

    window.customConfirm("Tem certeza que deseja excluir esta escala?", function (confirmado, dados) {
        if (!confirmado) return;

        console.log("Confirmado:", confirmado);
        console.log("Recebido dentro do modal:", dados.idEscala);

        const urlRequisicao = `${dados.idEscala}/delete/`;
        const csrfToken = window.getCookie('csrftoken');

        fetch(urlRequisicao, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(response => {
            if (!response.ok) throw new Error("Erro na requisição");
            return response.json();
        })
        .then(data => {
            if (data.success) {
                const blocoEscala = botao.closest(".bloco-escala");
                blocoEscala?.remove();
            } else {
                alert(data.message || "Erro ao excluir escala.");
            }
        })
        .catch(error => console.error("Erro ao excluir:", error));
    }, { idEscala }); // <-- Passa o idEscala como dado extra
}
