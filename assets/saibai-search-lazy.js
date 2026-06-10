/*
 * Empório Saibai — lazy-load search JS on header interaction (homepage)
 * Veltrus Growth & Technology
 */
(function () {
  'use strict';
  var cfg = window.__saibaiSearchLazy;
  if (!cfg || !cfg.src) return;

  var loaded = false;
  function loadSearchScript() {
    if (loaded) return;
    loaded = true;
    var s = document.createElement('script');
    s.src = cfg.src;
    s.defer = true;
    document.head.appendChild(s);
  }

  document.addEventListener('toggle', function (e) {
    if (e.target && e.target.matches && e.target.matches('.saibai-header__search-details') && e.target.open) {
      loadSearchScript();
    }
  }, true);

  if (cfg.loadOnPointer) {
    document.addEventListener('pointerdown', function (e) {
      if (e.target.closest && e.target.closest('.saibai-header__search-details')) {
        loadSearchScript();
      }
    }, { passive: true, once: true });
  }
})();
