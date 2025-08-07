window.getCookie = (name) =>  {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

window.customConfirm = (mensagem, callback, data = {}) => {
    const modal = document.getElementById('confirmModal');
    const confirmText = document.getElementById('confirmText');
    const btnYes = document.getElementById('confirmYes');
    const btnNo = document.getElementById('confirmNo');
    const btnClose = document.getElementById('confirmClose');

    confirmText.textContent = mensagem;
    modal.style.display = 'flex';
    modal.classList.add('active');

    // Remove event listeners antigos (se houver)
    btnYes.replaceWith(btnYes.cloneNode(true));
    const newBtnYes = document.getElementById('confirmYes');

    newBtnYes.onclick = () => {
        modal.style.display = 'none';
        modal.classList.remove('active');
        callback(true, data);  // <-- envia os dados
    };

    const cancelar = () => {
        modal.style.display = 'none';
        modal.classList.remove('active');
        callback(false, data);
    };

    btnNo.onclick = cancelar;
    btnClose.onclick = cancelar;

    modal.onclick = (e) => {
        if (e.target === modal) cancelar();
    };

    document.onkeydown = function (e) {
        if (e.key === "Escape") cancelar();
    };
};