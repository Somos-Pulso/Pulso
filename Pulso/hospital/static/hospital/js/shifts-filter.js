document.addEventListener('DOMContentLoaded', function() {
    const select = document.querySelector('select[name="departamento"]');
    
    if (select) {
        select.addEventListener('change', function() {
            const container = document.getElementById('container-plantoes');
            const selectedDept = this.value;

            // Mostrar carregando
            // container.innerHTML = '<div class="text-center py-4"><div class="spinner-border"></div><h3>Carregando seus plantões</h3></div>';

            // Fazer requisição
            fetch(`${window.location.pathname}?departamento=${selectedDept}`, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(response => {
                if (!response.ok) throw new Error("Erro na resposta");
                return response.text();
            })
            .then(html => {
                container.innerHTML = html;
            })
            .catch(error => {
                console.error('Erro:', error);
                container.innerHTML = `
                    <div class="alert alert-danger">
                        Erro ao filtrar. <a href="${window.location.pathname}" class="alert-link">Recarregar</a>
                    </div>`;
            });
        });
    }
});