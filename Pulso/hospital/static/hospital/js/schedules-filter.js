const selects = document.querySelectorAll('.filtro-select');

selects.forEach(select => {
    select.addEventListener('change', () => {
        const periodo = document.getElementById('periodo').value;
        const departamento = document.getElementById('departamento').value;
        const status = document.getElementById('status').value;

        const params = new URLSearchParams({
            periodo: periodo,
            departamento: departamento,
            status: status
        });

        fetch(`filter/?${params.toString()}`, {
            method: "GET",
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(response => {
                if (!response.ok) throw new Error("Erro ao buscar escalas");
                return response.json();
            })
            .then(data => {
                const container = document.getElementById('container-escalas');
                if (container) {
                    container.innerHTML = data.html;
                }
            })
            .catch(error => {
                console.error(error);
                const container = document.getElementById('container-escalas');
                if (container) {
                    container.innerHTML = "<p class='text-danger'>Erro ao carregar as escalas.</p>";
                }
            });
    });
});