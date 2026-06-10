/*
 * Empório Saibai — idle + viewport script loader (homepage)
 * Veltrus Growth & Technology
 */
(function () {
  'use strict';

  function loadScript(src) {
    if (!src || document.querySelector('script[src="' + src + '"]')) return;
    var s = document.createElement('script');
    s.src = src;
    s.defer = true;
    document.head.appendChild(s);
  }

  function loadIdleScripts() {
    var idleScripts = document.querySelectorAll('script[type="text/saibai-defer"][data-src]:not([data-saibai-loaded])');
    for (var i = 0; i < idleScripts.length; i++) {
      idleScripts[i].setAttribute('data-saibai-loaded', '1');
      loadScript(idleScripts[i].getAttribute('data-src'));
    }
  }

  var visibleScripts = document.querySelectorAll('script[type="text/saibai-defer-visible"][data-src][data-root]');
  if (visibleScripts.length && 'IntersectionObserver' in window) {
    for (var j = 0; j < visibleScripts.length; j++) {
      (function (el) {
        if (el.getAttribute('data-saibai-loaded')) return;
        var root = document.querySelector(el.getAttribute('data-root'));
        if (!root) {
          el.setAttribute('data-saibai-loaded', '1');
          loadScript(el.getAttribute('data-src'));
          return;
        }
        var obs = new IntersectionObserver(function (entries) {
          if (!entries[0].isIntersecting) return;
          obs.disconnect();
          el.setAttribute('data-saibai-loaded', '1');
          loadScript(el.getAttribute('data-src'));
        }, { rootMargin: '240px 0px' });
        obs.observe(root);
      })(visibleScripts[j]);
    }
  }

  function scheduleIdle() {
    if ('requestIdleCallback' in window) {
      requestIdleCallback(loadIdleScripts, { timeout: 5000 });
    } else {
      setTimeout(loadIdleScripts, 3500);
    }
  }

  if (document.readyState === 'complete') scheduleIdle();
  else window.addEventListener('load', scheduleIdle, { once: true });
})();
