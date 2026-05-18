/**
 * carousel.js — Descarte Certo
 *
 * Classe ES6+ para carrossel acessível, performático e sem dependências.
 *
 * Decisões técnicas:
 *  - Loop infinito via clonagem de slides (sem glitch de "volta rápida")
 *  - Touch/swipe com passive listeners (não bloqueia scroll do browser)
 *  - Animação exclusivamente via transform (GPU, sem reflow)
 *  - IntersectionObserver para pausar autoplay fora da viewport
 *  - Limpa todos os listeners e timers ao destruir (sem vazamento de memória)
 *  - Funciona com 1, 2 ou N slides
 */

class Carousel {
  /**
   * @param {HTMLElement} element - Container .carousel
   * @param {Object}      options - Configurações opcionais
   */
  constructor(element, options = {}) {
    if (!(element instanceof HTMLElement)) {
      console.error('[Carousel] Elemento inválido:', element);
      return;
    }

    this.root = element;

    // Configurações com defaults
    this.config = {
      autoplayDelay:    options.autoplayDelay    ?? 5000,    // ms entre slides
      transitionSpeed:  options.transitionSpeed  ?? 600,     // ms da animação CSS
      swipeThreshold:   options.swipeThreshold   ?? 50,      // px mínimos para swipe
      pauseOnHover:     options.pauseOnHover     ?? true,
      pauseOnFocus:     options.pauseOnFocus     ?? true,
      ...options,
    };

    // Estado interno
    this._currentIndex   = 0;  // índice no array original (0-based)
    this._isTransitioning = false;
    this._autoplayTimer  = null;
    this._isPaused       = false;
    this._isDestroyed    = false;

    // Rastreamento de touch/swipe
    this._touchStartX   = 0;
    this._touchStartY   = 0;
    this._touchDeltaX   = 0;
    this._isDragging    = false;

    // Coleção de listeners para remoção limpa (evita vazamento de memória)
    this._listeners = [];

    this._init();
  }

  // ─── INICIALIZAÇÃO ────────────────────────────────────────────────────────

  _init() {
    const slides = Array.from(this.root.querySelectorAll('.carousel__slide'));

    if (slides.length === 0) {
      this._renderFallback();
      return;
    }

    this._originalSlides = slides;
    this._totalOriginal  = slides.length;

    // Com apenas 1 slide não há necessidade de controles
    if (this._totalOriginal === 1) {
      this._setupSingleSlide();
      return;
    }

    this._buildDOM();
    this._setupAccessibility();
    this._setupEventListeners();
    this._setupIntersectionObserver();
    this._startAutoplay();
  }

  _renderFallback() {
    const track = this.root.querySelector('.carousel__track');
    if (track) {
      track.innerHTML = '<div class="carousel__fallback">Nenhuma imagem disponível</div>';
    }
  }

  _setupSingleSlide() {
    // Esconde botões e dots — não fazem sentido com 1 slide
    this.root.querySelectorAll('.carousel__btn, .carousel__dots').forEach(el => {
      el.style.display = 'none';
    });
  }

  /**
   * Constrói os dots e garante que o track esteja no lugar.
   * Os clones de slides (para loop infinito) são criados aqui.
   *
   * Estratégia de loop infinito:
   *  Original: [A, B, C]
   *  Com clones: [C*, A, B, C, A*]
   *   - C* = clone do último, posicionado antes do primeiro
   *   - A* = clone do primeiro, posicionado depois do último
   *  Ao chegar em A*, fazemos um "jump" silencioso (sem transição) para A real.
   *  Ao chegar em C*, fazemos um "jump" silencioso para C real.
   *  Resultado: loop infinito sem piscar ou voltar visualmente.
   */
  _buildDOM() {
    this._track = this.root.querySelector('.carousel__track');

    if (!this._track) {
      console.error('[Carousel] .carousel__track não encontrado');
      return;
    }

    // Clona primeiro e último para loop infinito
    const firstClone = this._originalSlides[0].cloneNode(true);
    const lastClone  = this._originalSlides[this._totalOriginal - 1].cloneNode(true);

    firstClone.setAttribute('aria-hidden', 'true');
    lastClone.setAttribute('aria-hidden',  'true');
    firstClone.classList.add('carousel__slide--clone');
    lastClone.classList.add('carousel__slide--clone');

    // Insere clones: lastClone no início, firstClone no final
    this._track.insertBefore(lastClone,   this._track.firstChild);
    this._track.appendChild(firstClone);

    // _allSlides inclui os clones. Índice 0 = lastClone, índice 1 = slide original 0, etc.
    this._allSlides = Array.from(this._track.querySelectorAll('.carousel__slide'));
    this._cloneOffset = 1; // quantos clones antes dos slides reais

    // Posiciona no primeiro slide real (índice 1 no array com clones)
    this._trackPosition = this._cloneOffset; // sempre aponta para o índice em _allSlides
    this._setTrackPosition(this._trackPosition, false); // false = sem transição

    // Cria os dots
    this._buildDots();

    // Busca botões prev/next
    this._btnPrev = this.root.querySelector('.carousel__btn--prev');
    this._btnNext = this.root.querySelector('.carousel__btn--next');
  }

  _buildDots() {
    const dotsContainer = this.root.querySelector('.carousel__dots');
    if (!dotsContainer) return;

    dotsContainer.innerHTML = '';

    this._dots = this._originalSlides.map((_, i) => {
      const dot = document.createElement('button');
      dot.type = 'button';
      dot.className = `carousel__dot${i === 0 ? ' is-active' : ''}`;
      dot.setAttribute('aria-label', `Ir para slide ${i + 1} de ${this._totalOriginal}`);
      dot.setAttribute('aria-pressed', i === 0 ? 'true' : 'false');
      dotsContainer.appendChild(dot);
      return dot;
    });
  }

  _setupAccessibility() {
    // O track é a "live region" do carrossel para leitores de tela
    if (this._track) {
      this._track.setAttribute('aria-live', 'off'); // desliga durante autoplay; ativa manualmente
    }

    // Marca slides ocultos como aria-hidden
    this._updateSlideAccessibility();
  }

  _updateSlideAccessibility() {
    this._allSlides?.forEach((slide, i) => {
      const isVisible = i === this._trackPosition;
      slide.setAttribute('aria-hidden', isVisible ? 'false' : 'true');
    });
  }

  // ─── NAVEGAÇÃO ────────────────────────────────────────────────────────────

  /**
   * Move para o próximo slide.
   * @param {boolean} fromUser - true quando chamado por interação do usuário
   */
  next(fromUser = false) {
    if (this._isTransitioning) return;
    this._goTo(this._trackPosition + 1, fromUser);
  }

  prev(fromUser = false) {
    if (this._isTransitioning) return;
    this._goTo(this._trackPosition - 1, fromUser);
  }

  goToIndex(originalIndex) {
    if (this._isTransitioning) return;
    // Converte índice original para índice no array com clones
    this._goTo(originalIndex + this._cloneOffset, true);
  }

  /**
   * Move o track para a posição especificada.
   * Gerencia o "jump" silencioso para implementar o loop infinito.
   */
  _goTo(targetPosition, fromUser = false) {
    if (this._isDestroyed) return;

    this._isTransitioning = true;
    this._trackPosition   = targetPosition;

    // Atualiza _currentIndex (índice do slide original, 0-based)
    this._currentIndex = targetPosition - this._cloneOffset;

    this._setTrackPosition(targetPosition, true);
    this._updateDots();
    this._updateSlideAccessibility();

    if (fromUser) {
      this._resetAutoplay();
    }

    // Após a transição, verifica se precisamos fazer um "jump" silencioso para o loop
    this._afterTransition(() => {
      // Estamos no clone do primeiro slide (após o último real)?
      if (targetPosition >= this._allSlides.length - 1) {
        // Pula silenciosamente para o primeiro slide real
        this._trackPosition = this._cloneOffset;
        this._currentIndex  = 0;
        this._setTrackPosition(this._trackPosition, false);
      }
      // Estamos no clone do último slide (antes do primeiro real)?
      else if (targetPosition <= 0) {
        // Pula silenciosamente para o último slide real
        this._trackPosition = this._allSlides.length - 2;
        this._currentIndex  = this._totalOriginal - 1;
        this._setTrackPosition(this._trackPosition, false);
      }

      this._isTransitioning = false;
    });
  }

  /**
   * Aplica a posição ao track via transform (GPU-accelerated, sem reflow).
   * @param {number}  position    - Índice em _allSlides
   * @param {boolean} withTransition - false para jumps silenciosos
   */
  _setTrackPosition(position, withTransition) {
    if (!this._track) return;

    if (!withTransition) {
      // Desliga a transição CSS temporariamente
      this._track.style.transition = 'none';
    } else {
      this._track.style.transition = `transform ${this.config.transitionSpeed}ms cubic-bezier(0.25, 0.46, 0.45, 0.94)`;
    }

    const percentage = -(position * 100);
    this._track.style.transform = `translateX(${percentage}%)`;
  }

  /**
   * Executa o callback após a transição CSS terminar.
   * Usa transitionend com fallback por timeout — browser pode não disparar
   * transitionend se a tab estiver em background.
   */
  _afterTransition(callback) {
    const fallback = setTimeout(callback, this.config.transitionSpeed + 50);

    const handler = () => {
      clearTimeout(fallback);
      this._track?.removeEventListener('transitionend', handler);
      callback();
    };

    this._track?.addEventListener('transitionend', handler, { once: true });
  }

  // ─── DOTS ─────────────────────────────────────────────────────────────────

  _updateDots() {
    if (!this._dots) return;
    const activeIndex = ((this._currentIndex % this._totalOriginal) + this._totalOriginal) % this._totalOriginal;

    this._dots.forEach((dot, i) => {
      const isActive = i === activeIndex;
      dot.classList.toggle('is-active', isActive);
      dot.setAttribute('aria-pressed', isActive ? 'true' : 'false');
    });
  }

  // ─── AUTOPLAY ─────────────────────────────────────────────────────────────

  _startAutoplay() {
    if (this._autoplayTimer) return;

    this._autoplayTimer = setInterval(() => {
      if (!this._isPaused && !this._isTransitioning && !this._isDestroyed) {
        this.next(false);
      }
    }, this.config.autoplayDelay);
  }

  _stopAutoplay() {
    clearInterval(this._autoplayTimer);
    this._autoplayTimer = null;
  }

  _resetAutoplay() {
    this._stopAutoplay();
    this._startAutoplay();
  }

  pause() {
    this._isPaused = true;
  }

  resume() {
    this._isPaused = false;
  }

  // ─── EVENT LISTENERS ──────────────────────────────────────────────────────

  /**
   * Registra todos os event listeners e armazena referências para cleanup.
   * Decisão: bind individual de cada handler para poder remover com removeEventListener.
   */
  _setupEventListeners() {
    // Botões prev/next
    if (this._btnPrev) {
      this._addListener(this._btnPrev, 'click', () => this.prev(true));
    }
    if (this._btnNext) {
      this._addListener(this._btnNext, 'click', () => this.next(true));
    }

    // Dots
    this._dots?.forEach((dot, i) => {
      this._addListener(dot, 'click', () => this.goToIndex(i));
    });

    // Teclado: setas esquerda/direita quando o carrossel tem foco
    this._addListener(this.root, 'keydown', this._handleKeydown.bind(this));

    // Pausar ao hover
    if (this.config.pauseOnHover) {
      this._addListener(this.root, 'mouseenter', () => this.pause());
      this._addListener(this.root, 'mouseleave', () => this.resume());
    }

    // Pausar ao foco (acessibilidade: usuário de teclado quer controlar)
    if (this.config.pauseOnFocus) {
      this._addListener(this.root, 'focusin',  () => this.pause());
      this._addListener(this.root, 'focusout', () => this.resume());
    }

    // Touch/Swipe (passive: não bloqueia scroll nativo do browser)
    this._addListener(this.root, 'touchstart', this._handleTouchStart.bind(this), { passive: true });
    this._addListener(this.root, 'touchmove',  this._handleTouchMove.bind(this),  { passive: true });
    this._addListener(this.root, 'touchend',   this._handleTouchEnd.bind(this),   { passive: true });
  }

  _addListener(target, event, handler, options = {}) {
    target.addEventListener(event, handler, options);
    this._listeners.push({ target, event, handler, options });
  }

  _handleKeydown(e) {
    if (e.key === 'ArrowLeft') {
      e.preventDefault();
      this.prev(true);
    } else if (e.key === 'ArrowRight') {
      e.preventDefault();
      this.next(true);
    }
  }

  _handleTouchStart(e) {
    this._touchStartX = e.touches[0].clientX;
    this._touchStartY = e.touches[0].clientY;
    this._isDragging  = true;
    this._touchDeltaX = 0;
  }

  _handleTouchMove(e) {
    if (!this._isDragging) return;
    this._touchDeltaX = e.touches[0].clientX - this._touchStartX;
    const deltaY      = e.touches[0].clientY - this._touchStartY;

    // Se o movimento é mais vertical que horizontal, não interfere no scroll
    if (Math.abs(deltaY) > Math.abs(this._touchDeltaX)) {
      this._isDragging = false;
    }
  }

  _handleTouchEnd() {
    if (!this._isDragging) return;
    this._isDragging = false;

    if (Math.abs(this._touchDeltaX) >= this.config.swipeThreshold) {
      if (this._touchDeltaX < 0) {
        this.next(true);
      } else {
        this.prev(true);
      }
    }

    this._touchDeltaX = 0;
  }

  // ─── INTERSECTION OBSERVER ────────────────────────────────────────────────

  /**
   * Pausa o autoplay quando o carrossel sai da viewport.
   * Melhora performance e experiência em páginas longas.
   */
  _setupIntersectionObserver() {
    if (!('IntersectionObserver' in window)) return;

    this._observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            this.resume();
          } else {
            this.pause();
          }
        });
      },
      { threshold: 0.1 }
    );

    this._observer.observe(this.root);
  }

  // ─── CLEANUP ──────────────────────────────────────────────────────────────

  /**
   * Remove todos os listeners, timers e observers.
   * Chamar ao remover o componente do DOM para evitar vazamento de memória.
   */
  destroy() {
    if (this._isDestroyed) return;
    this._isDestroyed = true;

    this._stopAutoplay();
    this._observer?.disconnect();

    this._listeners.forEach(({ target, event, handler, options }) => {
      target.removeEventListener(event, handler, options);
    });
    this._listeners = [];
  }
}

// ─── INICIALIZAÇÃO AUTOMÁTICA ─────────────────────────────────────────────────

/**
 * Inicializa todos os carrosseis na página.
 * Expõe instâncias em data-carousel para acesso externo se necessário.
 */
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.carousel').forEach(el => {
    const instance = new Carousel(el, {
      autoplayDelay:   5000,
      transitionSpeed: 600,
      swipeThreshold:  50,
      pauseOnHover:    true,
      pauseOnFocus:    true,
    });

    // Armazena instância no elemento para acesso externo
    el._carouselInstance = instance;
  });
});