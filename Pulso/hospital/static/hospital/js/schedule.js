function publicarEscala(id) {

  const url = window.hospital.urls.publishSchedule.replace("<id>", id)
  
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-CSRFToken': window.getCookie('csrftoken')
    },
    body: id
  })
  .then(response => {
    if (!response.ok) throw new Error('Erro ao publicar escala');
    location.reload();
    return response.text();
  })
  .then(text => {
    location.reload();
  })
  .catch(err => {
    location.reload();
  });
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('.message').forEach(el => {
    setTimeout(() => {
      el.style.transition = "opacity 0.5s";
      el.style.opacity = 0;
      setTimeout(() => el.remove(), 500);
    }, 5000); 
  });
});

function excluirEscala(event) {
    event.preventDefault();

    const botao = event.currentTarget;
    const idEscala = botao.dataset.id;

    window.customConfirm("Tem certeza que deseja excluir esta escala?", function (confirmado, dados) {
        if (!confirmado) return;

        const urlRequisicao = `delete/`;
        const csrfToken = window.getCookie('csrftoken');

        fetch(urlRequisicao, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "X-Requested-With": "n-XMLHttpRequest"
            }
        })
        .then(response => {
            if (!response.ok) throw new Error("Erro na requisição");
            return response.json();
        })
        .then(data => {
            if (data.success) {
                if (data.redirect_url) {
                    window.location.href = data.redirect_url;
                } else {
                    const blocoEscala = botao.closest(".bloco-escala");
                    blocoEscala?.remove();
                }
            } else {
                alert(data.message || "Erro ao excluir escala.");
            }
        })
        .catch(error => console.error("Erro ao excluir:", error));
    }, { idEscala }); // <-- Passa o idEscala como dado extra
}

const botao = document.getElementById("delete-schedule");
if (botao) {
    botao.addEventListener("click", excluirEscala);
} else {
    console.warn("Botão com id 'delete-schedule' não encontrado.");
}
