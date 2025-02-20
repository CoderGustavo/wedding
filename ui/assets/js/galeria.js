// Função para abrir o modal com a imagem selecionada
function abrirModal(src) {
    const modal = document.getElementById("modal");
    const imagemModal = document.getElementById("imagemModal");
    imagemModal.src = src;
    modal.style.display = "flex";
}

// Função para fechar o modal
function fecharModal() {
    const modal = document.getElementById("modal");
    modal.style.display = "none";
    modal.classList.remove("zoom"); // Remove o zoom ao fechar
}

// Função para aplicar e remover o zoom
function zoomImagem(event) {
    event.stopPropagation(); // Evita que o modal feche ao clicar na imagem
    const modal = document.getElementById("modal");
    modal.classList.toggle("zoom");
}
