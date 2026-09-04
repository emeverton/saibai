(function () {
  'use strict';

  var ROOT = '[data-saibai-prod]';
  var TAB = '[data-saibai-prod-tab]';
  var PANEL = '[data-saibai-prod-panel]';

  function initCarousel(panel) {
    if (panel.dataset.saibaiProdCarouselInit === 'true') {
      var trackOnly = panel.querySelector('.saibai-prod__track');
      if (trackOnly) {
        trackOnly.dispatchEvent(new Event('scroll'));
      }
      return;
    }
    panel.dataset.saibaiProdCarouselInit = 'true';

    var track = panel.querySelector('.saibai-prod__track');
    var prev = panel.querySelector('.saibai-prod__nav--prev');
    var next = panel.querySelector('.saibai-prod__nav--next');
    if (!track || !prev || !next) return;

    function scrollStep() {
      var card = track.querySelector('.saibai-prod__card');
      if (!card) return track.clientWidth * 0.8;
      var style = window.getComputedStyle(track);
      var gap = parseFloat(style.columnGap || style.gap || 0) || 0;
      return card.offsetWidth + gap;
    }

    function updateNav() {
      var maxScroll = track.scrollWidth - track.clientWidth;
      var hasOverflow = maxScroll > 4;
      prev.hidden = !hasOverflow;
      next.hidden = !hasOverflow;
      if (!hasOverflow) return;
      prev.disabled = track.scrollLeft <= 2;
      next.disabled = track.scrollLeft >= maxScroll - 2;
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

  function activateTab(section, tabKey) {
    var tabs = section.querySelectorAll(TAB);
    var panels = section.querySelectorAll(PANEL);
    var i;

    for (i = 0; i < tabs.length; i++) {
      var isActive = tabs[i].getAttribute('data-saibai-prod-tab') === tabKey;
      tabs[i].classList.toggle('is-active', isActive);
      tabs[i].setAttribute('aria-selected', isActive ? 'true' : 'false');
    }

    for (i = 0; i < panels.length; i++) {
      var panelActive = panels[i].getAttribute('data-saibai-prod-panel') === tabKey;
      panels[i].classList.toggle('is-active', panelActive);
      if (panelActive) {
        panels[i].removeAttribute('hidden');
        initCarousel(panels[i]);
      } else {
        panels[i].setAttribute('hidden', '');
      }
    }
  }

  function initProducts(section) {
    if (!section || section.dataset.saibaiProdInit === 'true') return;
    section.dataset.saibaiProdInit = 'true';

    var tabs = section.querySelectorAll(TAB);
    var activeTab = section.querySelector(TAB + '.is-active');
    var heroRoot = document.querySelector('[data-saibai-hero]');
    var defaultTab = heroRoot
      ? heroRoot.getAttribute('data-saibai-prod-default')
      : null;
    if (!defaultTab && activeTab) {
      defaultTab = activeTab.getAttribute('data-saibai-prod-tab');
    }
    if (!defaultTab) {
      defaultTab = 'fresca';
    }
    var i;

    for (i = 0; i < tabs.length; i++) {
      tabs[i].addEventListener('click', function () {
        activateTab(section, this.getAttribute('data-saibai-prod-tab'));
      });
    }

    activateTab(section, defaultTab);
  }

  function boot() {
    var nodes = document.querySelectorAll(ROOT);
    for (var i = 0; i < nodes.length; i++) {
      initProducts(nodes[i]);
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
