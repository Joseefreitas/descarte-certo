/**
 * menu.js — Descarte Certo
 *
 * Controla o menu lateral (nav drawer).
 *
 * Decisões técnicas:
 *  - inert: bloqueia foco e eventos em elementos fora do menu quando aberto
 *  - Trap de foco dentro do menu (Tab/Shift+Tab circula apenas entre itens do menu)
 *  - Fecha com Escape, com clique no overlay, e com clique fora
 *  - Restaura foco ao botão de abertura após fechar (WCAG 2.4.3)
 */
 
(function MenuManager() {
  const toggleBtn = document.getElementById('menu-toggle');
  const drawer    = document.getElementById('main-nav');
  const overlay   = document.getElementById('nav-overlay');
  const siteMain  = document.querySelector('.site-main');
  const siteFooter= document.querySelector('.site-footer');
 
  if (!toggleBtn || !drawer) {
    console.warn('[MenuManager] Elementos do menu não encontrados.');
    return;
  }
 
  let isOpen = false;
 
  // ─── ABRIR / FECHAR ───────────────────────────────────────────────────────
 
  function open() {
    isOpen = true;
 
    drawer.classList.add('is-open');
    overlay?.classList.add('is-visible');
    toggleBtn.setAttribute('aria-expanded', 'true');
    drawer.setAttribute('aria-hidden', 'false');
 
    // Bloqueia o foco no conteúdo principal enquanto o menu está aberto
    // inert é suportado em todos os browsers modernos (2022+)
    if (siteMain)   siteMain.inert   = true;
    if (siteFooter) siteFooter.inert = true;
 
    // Move o foco para o primeiro link do menu
    const firstLink = drawer.querySelector('a, button');
    firstLink?.focus();
 
    // Escuta Escape para fechar
    document.addEventListener('keydown', handleGlobalKeydown);
  }
 
  function close() {
    isOpen = false;
 
    drawer.classList.remove('is-open');
    overlay?.classList.remove('is-visible');
    toggleBtn.setAttribute('aria-expanded', 'false');
    drawer.setAttribute('aria-hidden', 'true');
 
    // Restaura interatividade do conteúdo principal
    if (siteMain)   siteMain.inert   = false;
    if (siteFooter) siteFooter.inert = false;
 
    // Restaura o foco ao botão que abriu o menu (WCAG 2.4.3)
    toggleBtn.focus();
 
    document.removeEventListener('keydown', handleGlobalKeydown);
  }
 
  function toggle() {
    isOpen ? close() : open();
  }
 
  // ─── TRAP DE FOCO ─────────────────────────────────────────────────────────
 
  /**
   * Limita o Tab/Shift+Tab ao conteúdo do menu enquanto está aberto.
   * Evita que o usuário de teclado "escape" para o conteúdo bloqueado.
   * inert já faz a maior parte do trabalho; este handler é um reforço.
   */
  function trapFocus(e) {
    if (!isOpen || e.key !== 'Tab') return;
 
    const focusable = Array.from(
      drawer.querySelectorAll('a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])')
    ).filter(el => !el.closest('[inert]'));
 
    if (focusable.length === 0) return;
 
    const first = focusable[0];
    const last  = focusable[focusable.length - 1];
 
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  }
 
  // ─── EVENTO GLOBAL: ESCAPE ────────────────────────────────────────────────
 
  function handleGlobalKeydown(e) {
    if (e.key === 'Escape' && isOpen) {
      close();
    }
    trapFocus(e);
  }
 
  // ─── EVENT LISTENERS ──────────────────────────────────────────────────────
 
  toggleBtn.addEventListener('click', toggle);
 
  // Overlay fecha o menu ao clicar
  overlay?.addEventListener('click', close);
 
  // Fecha ao navegar para qualquer link do menu
  drawer.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', close);
  });
 
  // ─── FECHAR EM RESIZE PARA DESKTOP ────────────────────────────────────────
  // Se o usuário redimensionar para desktop com o menu aberto, fecha automaticamente
 
  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      if (isOpen && window.innerWidth >= 1024) {
        close();
      }
    }, 150);
  });
})();
 