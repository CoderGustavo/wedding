const carrossel = document.getElementById('carrossel');
const carrosselContent = document.getElementById('carrosselContent');

let isDragging = false;
let startX;
let scrollLeft;

// Iniciar arrasto
carrossel.addEventListener('mousedown', (e) => {
  isDragging = true;
  startX = e.pageX - carrosselContent.offsetLeft;
  scrollLeft = carrosselContent.scrollLeft;
  carrosselContent.classList.add('cursor-grabbing'); // Estilo para indicar o arrasto
});

carrossel.addEventListener('mouseleave', () => {
  isDragging = false;
  carrosselContent.classList.remove('cursor-grabbing');
});

carrossel.addEventListener('mouseup', () => {
  isDragging = false;
  carrosselContent.classList.remove('cursor-grabbing');
});

carrossel.addEventListener('mousemove', (e) => {
  if (!isDragging) return;
  e.preventDefault();
  const x = e.pageX - carrosselContent.offsetLeft;
  const walk = (x - startX) * 1.5; // Velocidade do arrasto
  carrosselContent.scrollLeft = scrollLeft - walk;
});

// Para dispositivos de toque (touch)
carrossel.addEventListener('touchstart', (e) => {
  isDragging = true;
  startX = e.touches[0].pageX - carrosselContent.offsetLeft;
  scrollLeft = carrosselContent.scrollLeft;
});

carrossel.addEventListener('touchend', () => {
  isDragging = false;
});

carrossel.addEventListener('touchmove', (e) => {
  if (!isDragging) return;
  const x = e.touches[0].pageX - carrosselContent.offsetLeft;
  const walk = (x - startX) * 1.5;
  carrosselContent.scrollLeft = scrollLeft - walk;
});