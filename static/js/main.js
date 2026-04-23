const btn = document.querySelector('.menu-toggle');
const menu = document.querySelector('.caixa-menu');

btn.addEventListener('click', (e) => {
  e.stopPropagation();
  menu.classList.toggle('ativo');

  if (menu.classList.contains('ativo')) {
    btn.textContent = '✖ Menu';
  } else {
    btn.textContent = '☰ Menu';
  }
});