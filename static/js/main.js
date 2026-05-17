const btn = document.querySelector('.menu-toggle');
const menu = document.querySelector('.caixa-menu');

if (btn && menu) {
  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    menu.classList.toggle('ativo');

    if (menu.classList.contains('ativo')) {
      btn.textContent = '✖ Menu';
    } else {
      btn.textContent = '☰ Menu';
    }
  });
}

document.addEventListener('click', (e) => {
  if (menu.classList.contains('ativo') && !menu.contains(e.target) && e.target !== btn) {
    menu.classList.remove('ativo');
    btn.textContent = '☰ Menu';
  }
});