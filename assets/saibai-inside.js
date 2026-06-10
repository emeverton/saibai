(function () {
  'use strict';

  var ROOT = '[data-saibai-inside]';
  var TRACK = '[data-saibai-ins-track]';
  var CARD = '[data-saibai-ins-card]';
  var CURRENT = '[data-saibai-ins-current]';

  function initInside(section) {
    if (!section || section.dataset.saibaiInsInit === 'true') return;
    section.dataset.saibaiInsInit = 'true';

    var track = section.querySelector(TRACK);
    var prev = section.querySelector('.saibai-ins__nav--prev');
    var next = section.querySelector('.saibai-ins__nav--next');
    var currentEl = section.querySelector(CURRENT);
    if (!track || !prev || !next || !currentEl) return;

    var cards = track.querySelectorAll(CARD);
    var total = cards.length;
    if (!total) return;

    function scrollStep() {
      var card = cards[0];
      if (!card) return track.clientWidth * 0.75;
      var style = window.getComputedStyle(track);
      var gap = parseFloat(style.columnGap || style.gap || 0) || 0;
      return card.offsetWidth + gap;
    }

    function getActiveIndex() {
      var pad = parseFloat(window.getComputedStyle(track).scrollPaddingLeft || 0) || 0;
      var center = track.scrollLeft + pad + track.clientWidth * 0.15;
      var i;
      var best = 0;
      var bestDist = Infinity;

      for (i = 0; i < cards.length; i++) {
        var dist = Math.abs(cards[i].offsetLeft - center);
        if (dist < bestDist) {
          bestDist = dist;
          best = i;
        }
      }

      return best + 1;
    }

    function updateNav() {
      var maxScroll = track.scrollWidth - track.clientWidth;
      var hasOverflow = maxScroll > 4;

      prev.hidden = !hasOverflow;
      next.hidden = !hasOverflow;
      if (!hasOverflow) {
        currentEl.textContent = '1';
        return;
      }

      prev.disabled = track.scrollLeft <= 2;
      next.disabled = track.scrollLeft >= maxScroll - 2;
      currentEl.textContent = String(getActiveIndex());
    }

    prev.addEventListener('click', function () {
      track.scrollBy({ left: -scrollStep(), behavior: 'smooth' });
    });

    next.addEventListener('click', function () {
      track.scrollBy({ left: scrollStep(), behavior: 'smooth' });
    });

    track.addEventListener('scroll', updateNav, { passive: true });
    window.addEventListener('resize', updateNav, { passive: true });
    updateNav();
  }

  function boot() {
    var nodes = document.querySelectorAll(ROOT);
    for (var i = 0; i < nodes.length; i++) {
      initInside(nodes[i]);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
