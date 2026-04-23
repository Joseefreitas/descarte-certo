const btn = document.querySelector('.menu-toggle');
const menu = document.querySelector('.caixa-menu');

btn.addEventListener('click', () => {
  menu.classList.toggle('ativo');

  if (menu.classList.contains('ativo')) {
    btn.textContent = '✖ Menu';
  } else {
    btn.textContent = '☰ Menu';
  }
});