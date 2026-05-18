/**
 * darkmode.js — Descarte Certo
 *
 * Gerenciador de tema com suporte a 3 modos: light | dark | system
 *
 * Ciclo ao clicar no botão: light → dark → system → light ...
 *
 * Decisões técnicas:
 *  - O script inline no <head> do base.html aplica o tema ANTES do render (anti-FOUC).
 *    Este arquivo só cuida da interatividade e é carregado com defer.
 *  - A classe .theme-transitions-ready é adicionada DEPOIS do primeiro render
 *    para evitar que a transição CSS dispare na carga inicial da página.
 *  - localStorage chave: 'dc-theme' (dc = Descarte Certo, evita colisão)
 */

(function ThemeManager() {
  const STORAGE_KEY   = 'dc-theme';
  const THEMES        = ['light', 'dark', 'system'];
  const TRANSITION_CLASS = 'theme-transitions-ready';

  const root          = document.documentElement;
  const toggleBtn     = document.getElementById('theme-toggle');

  // ─── ESTADO ATUAL ─────────────────────────────────────────────────────────

  /**
   * Lê o tema salvo. O script inline no <head> já aplicou ao <html>,
   * então apenas sincronizamos o estado JS.
   */
  function getCurrentTheme() {
    return localStorage.getItem(STORAGE_KEY) || 'system';
  }

  // ─── APLICAR TEMA ─────────────────────────────────────────────────────────

  /**
   * Aplica o tema ao <html> e persiste no localStorage.
   * @param {string} theme - 'light' | 'dark' | 'system'
   */
  function applyTheme(theme) {
    if (!THEMES.includes(theme)) {
      console.warn(`[ThemeManager] Tema inválido: "${theme}". Usando "system".`);
      theme = 'system';
    }

    root.setAttribute('data-theme', theme);
    localStorage.setItem(STORAGE_KEY, theme);

    // Atualiza aria-label do botão para anunciar o estado atual ao leitor de tela
    if (toggleBtn) {
      const labels = {
        light:  'Tema claro ativo. Clique para alternar para escuro.',
        dark:   'Tema escuro ativo. Clique para alternar para sistema.',
        system: 'Tema do sistema ativo. Clique para alternar para claro.',
      };
      toggleBtn.setAttribute('aria-label', labels[theme]);
    }
  }

  // ─── CICLAR TEMAS ─────────────────────────────────────────────────────────

  function cycleTheme() {
    const current    = getCurrentTheme();
    const currentIdx = THEMES.indexOf(current);
    const next       = THEMES[(currentIdx + 1) % THEMES.length];
    applyTheme(next);
  }

  // ─── SINCRONIZAR COM O SISTEMA ────────────────────────────────────────────

  /**
   * Se o usuário alterou a preferência de cor do sistema operacional
   * e está no modo "system", atualiza a aparência sem salvar nada.
   * O CSS cuida do visual via prefers-color-scheme — só garantimos o data-theme.
   */
  function syncWithSystem() {
    const current = getCurrentTheme();
    if (current === 'system') {
      // Re-aplica "system" para disparar o re-render via CSS
      root.setAttribute('data-theme', 'system');
    }
  }

  // ─── TRANSIÇÕES ───────────────────────────────────────────────────────────

  /**
   * Ativa as transições CSS APÓS o primeiro render.
   * Se ativássemos antes, o tema inicial apareceria com uma animação estranha.
   *
   * requestAnimationFrame duplo: garante que o browser pintou pelo menos 1 frame
   * antes de ativarmos as transições.
   */
  function enableTransitions() {
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        root.classList.add(TRANSITION_CLASS);
      });
    });
  }

  // ─── INICIALIZAÇÃO ────────────────────────────────────────────────────────

  function init() {
    // Garante que o estado JS está sincronizado com o que o script inline aplicou
    const saved = getCurrentTheme();
    applyTheme(saved);

    // Ativa transições após o primeiro frame renderizado
    enableTransitions();

    // Botão de toggle
    if (toggleBtn) {
      toggleBtn.addEventListener('click', () => {
        cycleTheme();
      });
    } else {
      console.warn('[ThemeManager] Botão #theme-toggle não encontrado no DOM.');
    }

    // Escuta mudanças na preferência do sistema operacional
    if (window.matchMedia) {
      window
        .matchMedia('(prefers-color-scheme: dark)')
        .addEventListener('change', syncWithSystem);
    }
  }

  // DOM já está pronto quando defer é usado, mas checamos por segurança
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();