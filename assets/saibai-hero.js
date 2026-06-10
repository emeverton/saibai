(function () {
  'use strict';

  var ROOT = '[data-saibai-hero]';
  var BOX = '[data-saibai-hero-box]';
  var SCALER = '[data-saibai-hero-scaler]';
  var STAGE = '[data-saibai-hero-stage]';
  var ZONE = '[data-saibai-hero-zone]';
  var FRAME = '[data-saibai-hero-frame]';

  var BOX_W = 250;
  var BOX_H = 180;

  function initHeroScroll(root) {
    var box = root.querySelector(BOX);
    var scaler = root.querySelector(SCALER);
    var stage = root.querySelector(STAGE);
    var zone = root.querySelector(ZONE);
    var frame = root.querySelector(FRAME);

    if (!box || !frame || !stage) return;

    var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var boxW = box.offsetWidth || BOX_W;
    var boxH = box.offsetHeight || BOX_H;

    var cached = {
      mediaH: boxH,
      zoneH: boxH,
      stageH: boxH * 2,
      scrollRange: 1
    };
    var last = { top: -1, scale: -1, locked: null };
    var ticking = false;

    box.style.width = boxW + 'px';
    box.style.height = boxH + 'px';
    box.style.bottom = 'auto';

    function measureLayout() {
      cached.mediaH = frame.offsetHeight;
      cached.zoneH = zone ? zone.offsetHeight : boxH;
      cached.stageH = stage.offsetHeight;
      cached.scrollRange = cached.stageH > 0 ? cached.stageH * 0.48 : 1;
    }

    function applyBoxTop(top, isLocked) {
      box.style.top = top + 'px';
      box.style.bottom = 'auto';
      root.classList.toggle('is-box-locked', isLocked);
    }

    function updateHeroScroll() {
      measureLayout();

      var endTop = cached.mediaH;
      var startTop = cached.mediaH - boxH;

      if (reducedMotion) {
        applyBoxTop(endTop, true);
        return;
      }

      var rect = root.getBoundingClientRect();
      var viewportH = window.innerHeight;

      if (rect.bottom < 0 || rect.top > viewportH) {
        ticking = false;
        return;
      }

      var progress = 0;
      if (cached.scrollRange > 0) {
        progress = Math.min(Math.max((0 - rect.top) / cached.scrollRange, 0), 1);
      }

      var top = startTop + progress * boxH;
      var scale = 1 + progress * 0.04;
      var isLocked = progress >= 0.98;

      if (last.top !== top) {
        applyBoxTop(top, isLocked);
        last.top = top;
      } else if (last.locked !== isLocked) {
        root.classList.toggle('is-box-locked', isLocked);
      }

      if (scaler) {
        var scaleRounded = scale.toFixed(4);
        if (last.scale !== scaleRounded) {
          scaler.style.transform = 'scale(' + scaleRounded + ')';
          last.scale = scaleRounded;
        }
      }

      last.locked = isLocked;
      ticking = false;
    }

    function onScroll() {
      if (!ticking) {
        ticking = true;
        window.requestAnimationFrame(updateHeroScroll);
      }
    }

    function onResize() {
      boxW = box.offsetWidth || BOX_W;
      boxH = box.offsetHeight || BOX_H;
      box.style.width = boxW + 'px';
      box.style.height = boxH + 'px';
      last.top = -1;
      last.scale = -1;
      last.locked = null;
      onScroll();
    }

    measureLayout();
    updateHeroScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onResize, { passive: true });
  }

  function initHero(root) {
    if (!root || root.dataset.saibaiHeroInit === 'true') return;
    root.dataset.saibaiHeroInit = 'true';

    function startScroll() {
      initHeroScroll(root);
    }

    if ('requestIdleCallback' in window) {
      window.requestIdleCallback(startScroll, { timeout: 1500 });
    } else {
      window.setTimeout(startScroll, 200);
    }
  }

  function boot() {
    var nodes = document.querySelectorAll(ROOT);
    for (var i = 0; i < nodes.length; i++) {
      initHero(nodes[i]);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
