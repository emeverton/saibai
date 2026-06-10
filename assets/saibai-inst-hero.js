(function () {
  'use strict';

  var ROOT = '[data-saibai-inst-hero]';
  var BOX = '[data-saibai-inst-hero-box]';
  var SCALER = '[data-saibai-inst-hero-scaler]';
  var STAGE = '[data-saibai-inst-hero-stage]';
  var ZONE = '[data-saibai-inst-hero-zone]';
  var FRAME = '[data-saibai-inst-hero-frame]';

  var ZONE_H = 179;

  function initInstHeroScroll(root) {
    var box = root.querySelector(BOX);
    var scaler = root.querySelector(SCALER);
    var stage = root.querySelector(STAGE);
    var zone = root.querySelector(ZONE);
    var frame = root.querySelector(FRAME);

    if (!box || !frame || !stage) return;

    var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var cached = {
      mediaH: ZONE_H,
      zoneH: ZONE_H,
      boxH: ZONE_H,
      stageH: ZONE_H * 2,
      scrollRange: 1
    };
    var last = { top: -1, scale: -1, locked: null };
    var ticking = false;

    box.style.bottom = 'auto';

    function measureLayout() {
      cached.mediaH = frame.offsetHeight;
      cached.zoneH = zone ? zone.offsetHeight : ZONE_H;
      cached.boxH = box.offsetHeight;
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
      var startTop = cached.mediaH - cached.boxH;

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

      var top = startTop + progress * cached.zoneH;
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

  function initInstHero(root) {
    if (!root || root.dataset.saibaiInstHeroInit === 'true') return;
    root.dataset.saibaiInstHeroInit = 'true';
    initInstHeroScroll(root);
  }

  function boot() {
    var nodes = document.querySelectorAll(ROOT);
    for (var i = 0; i < nodes.length; i++) {
      initInstHero(nodes[i]);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
