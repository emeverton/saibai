(function () {
  'use strict';

  function initCarousel(el) {
    if (!el || el.dataset.saibaiAbReady === 'true') return;
    el.dataset.saibaiAbReady = 'true';

    var slides = el.querySelectorAll('.saibai-ab__slide');
    var prevBtn = el.querySelector('.saibai-ab__btn--prev');
    var nextBtn = el.querySelector('.saibai-ab__btn--next');
    var pauseBtn = el.querySelector('.saibai-ab__btn--pause');
    var pauseIcon = pauseBtn ? pauseBtn.querySelector('.saibai-ab__icon-pause') : null;
    var playIcon = pauseBtn ? pauseBtn.querySelector('.saibai-ab__icon-play') : null;
    var interval = parseInt(el.getAttribute('data-interval'), 10) || 6000;
    var index = 0;
    var timer = null;
    var isPaused = false;
    var total = slides.length;

    if (total < 2) {
      if (prevBtn) prevBtn.hidden = true;
      if (nextBtn) nextBtn.hidden = true;
      return;
    }

    function show(i) {
      for (var n = 0; n < total; n++) {
        var on = n === i;
        slides[n].classList.toggle('is-active', on);
        slides[n].setAttribute('aria-hidden', on ? 'false' : 'true');
      }
      index = i;
    }

    function next() {
      show((index + 1) % total);
    }

    function prev() {
      show((index - 1 + total) % total);
    }

    function stop() {
      if (timer) {
        clearInterval(timer);
        timer = null;
      }
    }

    function start() {
      stop();
      if (document.hidden || isPaused) return;
      timer = setInterval(next, interval);
    }

    function setPaused(paused) {
      isPaused = paused;
      if (!pauseBtn) return;
      if (paused) {
        stop();
        pauseBtn.setAttribute('aria-label', 'Reproduzir anúncios');
        pauseBtn.setAttribute('aria-pressed', 'true');
        el.classList.add('is-paused');
        if (pauseIcon) pauseIcon.hidden = true;
        if (playIcon) playIcon.hidden = false;
      } else {
        pauseBtn.setAttribute('aria-label', 'Pausar anúncios');
        pauseBtn.setAttribute('aria-pressed', 'false');
        el.classList.remove('is-paused');
        if (pauseIcon) pauseIcon.hidden = false;
        if (playIcon) playIcon.hidden = true;
        start();
      }
    }

    if (pauseBtn) {
      pauseBtn.addEventListener('click', function () {
        setPaused(!isPaused);
      });
    }

    if (prevBtn) {
      prevBtn.addEventListener('click', function () {
        prev();
        start();
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', function () {
        next();
        start();
      });
    }

    document.addEventListener('visibilitychange', function () {
      if (document.hidden) stop();
      else start();
    });

    start();
  }

  function boot() {
    document.querySelectorAll('[data-saibai-ab-carousel]').forEach(initCarousel);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
