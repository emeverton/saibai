(function () {
  'use strict';

  var ROOT = '[data-saibai-hero]';
  var BOX = '[data-saibai-hero-box]';
  var SCALER = '[data-saibai-hero-scaler]';
  var STAGE = '[data-saibai-hero-stage]';
  var FRAME = '[data-saibai-hero-frame]';
  var MOBILE_MQ = '(max-width: 989px)';

  var BOX_W = 264;
  var BOX_H = 232;

  function clearBoxInline(box, scaler) {
    if (box) {
      box.style.top = '';
      box.style.bottom = '';
      box.style.width = '';
      box.style.height = '';
      box.style.transform = '';
    }
    if (scaler) scaler.style.transform = '';
  }

  function initHeroScroll(root) {
    var box = root.querySelector(BOX);
    var scaler = root.querySelector(SCALER);
    var stage = root.querySelector(STAGE);
    var frame = root.querySelector(FRAME);

    if (!box || !frame || !stage) return;

    var mql = window.matchMedia ? window.matchMedia(MOBILE_MQ) : null;
    var reducedMotion = window.matchMedia
      ? window.matchMedia('(prefers-reduced-motion: reduce)').matches
      : false;

    var boxW = BOX_W;
    var boxH = BOX_H;
    var cached = { mediaH: BOX_H, stageH: BOX_H * 2, scrollRange: 1 };
    var last = { top: -1, scale: -1 };
    var ticking = false;
    var desktopBound = false;
    var baseDocTop = 0;

    function isMobile() {
      return !!(mql && mql.matches);
    }

    function measureLayout() {
      boxW = box.offsetWidth || BOX_W;
      boxH = box.offsetHeight || BOX_H;
      cached.mediaH = frame.offsetHeight || boxH;
      cached.stageH = stage.offsetHeight || cached.mediaH + boxH;
      /* Faixa de scroll = altura do box (desce da borda da mídia até o fim da zona) */
      cached.scrollRange = Math.max(boxH, 1);
      baseDocTop = root.getBoundingClientRect().top + (window.scrollY || window.pageYOffset || 0);
    }

    function applyBoxTop(top) {
      box.style.top = top + 'px';
      box.style.bottom = 'auto';
    }

    function progressFromScroll() {
      /* Delta visual: quanto o topo do hero subiu no viewport (= scroll efetivo no bloco) */
      var rectTop = root.getBoundingClientRect().top;
      var scrolled = baseDocTop - rectTop;
      if (scrolled < 0) scrolled = 0;
      return Math.min(scrolled / cached.scrollRange, 1);
    }

    function updateHeroScroll() {
      var endTop = cached.mediaH;
      var startTop = Math.max(cached.mediaH - boxH, 0);

      if (reducedMotion) {
        applyBoxTop(endTop);
        ticking = false;
        return;
      }

      var rect = root.getBoundingClientRect();
      var viewportH = window.innerHeight || 0;
      if (rect.bottom < 0 || rect.top > viewportH) {
        ticking = false;
        return;
      }

      var progress = progressFromScroll();
      var top = startTop + progress * boxH;
      var scale = 1 + progress * 0.04;

      if (last.top !== top) {
        applyBoxTop(top);
        last.top = top;
      }

      if (scaler) {
        var scaleRounded = scale.toFixed(4);
        if (last.scale !== scaleRounded) {
          scaler.style.transform = 'scale(' + scaleRounded + ')';
          last.scale = scaleRounded;
        }
      }

      ticking = false;
    }

    function onScroll() {
      if (!ticking) {
        ticking = true;
        window.requestAnimationFrame(updateHeroScroll);
      }
    }

    function enableDesktop() {
      measureLayout();
      box.style.width = boxW + 'px';
      box.style.height = boxH + 'px';
      box.style.bottom = 'auto';
      last.top = -1;
      last.scale = -1;
      updateHeroScroll();

      if (!desktopBound) {
        window.addEventListener('scroll', onScroll, { passive: true });
        desktopBound = true;
      }
    }

    function disableDesktop() {
      clearBoxInline(box, scaler);
      last.top = -1;
      last.scale = -1;
      if (desktopBound) {
        window.removeEventListener('scroll', onScroll);
        desktopBound = false;
      }
    }

    function syncMode() {
      if (isMobile()) {
        disableDesktop();
        return;
      }
      enableDesktop();
    }

    function onResize() {
      if (isMobile()) {
        disableDesktop();
        return;
      }
      enableDesktop();
    }

    syncMode();
    window.addEventListener('resize', onResize, { passive: true });
    if (mql) {
      if (typeof mql.addEventListener === 'function') {
        mql.addEventListener('change', syncMode);
      } else if (typeof mql.addListener === 'function') {
        mql.addListener(syncMode);
      }
    }

    /* Remeasure quando a imagem do hero carrega (mediaH começa 0 em alguns loads) */
    var heroImg = frame.querySelector('img');
    if (heroImg && !heroImg.complete) {
      heroImg.addEventListener('load', function () {
        if (!isMobile()) enableDesktop();
      });
    }
    window.addEventListener('load', function () {
      if (!isMobile()) enableDesktop();
    });
  }

  function initHero(root) {
    if (!root || root.dataset.saibaiHeroInit === 'true') return;
    root.dataset.saibaiHeroInit = 'true';

    function startScroll() {
      initHeroScroll(root);
    }

    if ('requestIdleCallback' in window) {
      window.requestIdleCallback(startScroll, { timeout: 800 });
    } else {
      window.setTimeout(startScroll, 120);
    }
  }

  function boot() {
    var nodes = document.querySelectorAll(ROOT);
    for (var i = 0; i < nodes.length; i++) {
      initHero(nodes[i]);
    }
  }

  function scheduleBoot() {
    if ('requestIdleCallback' in window) {
      window.requestIdleCallback(boot, { timeout: 1500 });
    } else {
      window.setTimeout(boot, 800);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', scheduleBoot, { once: true });
  } else {
    scheduleBoot();
  }
})();
