(function () {
  'use strict';

  var ROOT = '[data-saibai-header]';
  var OPEN = '[data-saibai-header-open]';
  var CLOSE = '[data-saibai-header-close]';
  var DRAWER = '[data-saibai-header-drawer]';
  var MEGA_LAYER = '[data-saibai-mega-layer]';
  var MEGA_TRIGGER = '[data-saibai-mega-trigger]';
  var MEGA_PANEL = '[data-saibai-mega-panel]';
  var MEGA_CLOSE = '[data-saibai-mega-close]';
  var MEGA_ITEM = '[data-saibai-mega-item]';
  var MEGA_OPEN_DELAY = 0;
  var MEGA_CLOSE_FALLBACK = 1500;
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var megaDesktopMq = window.matchMedia ? window.matchMedia('(min-width: 1025px)') : null;

  function isMegaDesktop() {
    return !megaDesktopMq || megaDesktopMq.matches;
  }

  function initHeader(root) {
    if (!root || root.dataset.saibaiHeaderInit === 'true') return;
    root.dataset.saibaiHeaderInit = 'true';

    var section = root.closest('.shopify-section');
    if (section) {
      section.classList.add('header-group-section');
    }

    var drawer = root.querySelector(DRAWER);
    var openBtn = root.querySelector(OPEN);
    var closeEls = root.querySelectorAll(CLOSE);
    var megaLayer = root.querySelector(MEGA_LAYER);
    var megaTriggers = root.querySelectorAll(MEGA_TRIGGER);
    var megaPanels = root.querySelectorAll(MEGA_PANEL);
    var activeTrigger = null;
    var activePanel = null;
    var megaClosing = false;
    var megaCloseTimer = null;
    var megaOpenTimer = null;
    var pendingTrigger = null;

    function resetTriggers() {
      for (var t = 0; t < megaTriggers.length; t++) {
        megaTriggers[t].setAttribute('aria-expanded', 'false');
        megaTriggers[t].classList.remove('is-pending');
      }
    }

    function cancelOpenMega() {
      if (megaOpenTimer) {
        window.clearTimeout(megaOpenTimer);
        megaOpenTimer = null;
      }
      pendingTrigger = null;
      root.classList.remove('is-mega-pending');
    }

    function resetPanels(hidePanels) {
      for (var p = 0; p < megaPanels.length; p++) {
        megaPanels[p].classList.remove('is-active');
        if (hidePanels !== false) {
          megaPanels[p].hidden = true;
        }
      }
    }

    function finishCloseMega() {
      if (!megaLayer) return;

      if (megaCloseTimer) {
        window.clearTimeout(megaCloseTimer);
        megaCloseTimer = null;
      }

      megaLayer.hidden = true;
      resetPanels(true);
      root.classList.remove('is-mega-open');
      document.documentElement.classList.remove('saibai-mega-open');
      activeTrigger = null;
      activePanel = null;
      megaClosing = false;
    }

    function syncFeature(panel, item) {
      if (!panel || !item) return;

      var img = panel.querySelector('[data-saibai-mega-feature-img]');
      var title = panel.querySelector('[data-saibai-mega-feature-title]');
      var cta = panel.querySelector('[data-saibai-mega-feature-cta]');
      var link = panel.querySelector('[data-saibai-mega-feature-link]');
      var imageUrl = item.getAttribute('data-image');
      var itemTitle = item.getAttribute('data-title');
      var itemCta = item.getAttribute('data-cta');
      var itemUrl = item.getAttribute('data-url');

      if (link && itemUrl) link.href = itemUrl;
      if (title && itemTitle) title.textContent = itemTitle;
      if (cta && itemCta) cta.textContent = itemCta;

      if (!img || !imageUrl) return;

      if (img.getAttribute('src') === imageUrl) return;

      img.classList.add('is-fading');
      window.setTimeout(function () {
        img.src = imageUrl;
        if (itemTitle) img.alt = itemTitle;
        img.classList.remove('is-fading');
      }, 180);
    }

    function syncDrill(panel, item) {
      if (!panel || !item) return;
      var target = item.getAttribute('data-saibai-mega-drill-target');
      if (target === null || target === '') return;

      var panes = panel.querySelectorAll('[data-saibai-mega-drill-pane]');
      for (var d = 0; d < panes.length; d++) {
        var pane = panes[d];
        var isMatch = pane.getAttribute('data-saibai-mega-drill-pane') === target;
        pane.classList.toggle('is-active', isMatch);
        pane.hidden = !isMatch;
      }
    }

    function setActiveSidebarItem(panel, item) {
      var items = panel.querySelectorAll(MEGA_ITEM);
      for (var i = 0; i < items.length; i++) {
        items[i].classList.remove('is-current');
      }
      if (item) item.classList.add('is-current');
    }

    function initPanelItems(panel) {
      var items = panel.querySelectorAll(MEGA_ITEM);
      for (var i = 0; i < items.length; i++) {
        (function (item) {
          item.addEventListener('mouseenter', function () {
            if (!panel.classList.contains('is-active')) return;
            setActiveSidebarItem(panel, item);
            syncFeature(panel, item);
            syncDrill(panel, item);
          });

          item.addEventListener('focus', function () {
            if (!panel.classList.contains('is-active')) return;
            setActiveSidebarItem(panel, item);
            syncFeature(panel, item);
            syncDrill(panel, item);
          });
        })(items[i]);
      }

      if (items.length > 0) {
        setActiveSidebarItem(panel, items[0]);
        syncFeature(panel, items[0]);
        syncDrill(panel, items[0]);
      }
    }

    function closeMega() {
      if (!megaLayer || megaClosing) return;
      if (megaLayer.hidden) return;

      cancelOpenMega();

      var panel = activePanel;
      resetTriggers();
      megaLayer.classList.remove('is-open');
      root.classList.remove('is-mega-open');
      document.documentElement.classList.remove('saibai-mega-open');

      if (!panel) {
        finishCloseMega();
        return;
      }

      megaClosing = true;
      panel.classList.remove('is-active');

      function onPanelTransitionEnd(e) {
        if (!e || e.target !== panel) return;
        if (e.propertyName !== 'clip-path') return;
        panel.removeEventListener('transitionend', onPanelTransitionEnd);
        finishCloseMega();
      }

      panel.addEventListener('transitionend', onPanelTransitionEnd);
      megaCloseTimer = window.setTimeout(function () {
        panel.removeEventListener('transitionend', onPanelTransitionEnd);
        finishCloseMega();
      }, MEGA_CLOSE_FALLBACK);
    }

    function slidePanelIn(panel) {
      panel.classList.remove('is-active');
      panel.hidden = false;
      void panel.offsetHeight;
      window.requestAnimationFrame(function () {
        window.requestAnimationFrame(function () {
          panel.classList.add('is-active');
          if (megaLayer) {
            megaLayer.classList.add('is-open');
          }
        });
      });
    }

    function openMegaNow(trigger) {
      if (!megaLayer || !trigger) return;

      var panelId = trigger.getAttribute('aria-controls');
      var panel = panelId ? root.querySelector('#' + panelId) : null;
      if (!panel) return;

      cancelOpenMega();
      closeDrawer();

      if (megaClosing) {
        if (megaCloseTimer) {
          window.clearTimeout(megaCloseTimer);
          megaCloseTimer = null;
        }
        megaClosing = false;
      }

      resetTriggers();

      for (var pi = 0; pi < megaPanels.length; pi++) {
        megaPanels[pi].classList.remove('is-active');
        if (megaPanels[pi] !== panel) {
          megaPanels[pi].hidden = true;
        }
      }

      megaLayer.classList.remove('is-open');
      megaLayer.hidden = false;
      void megaLayer.offsetHeight;

      slidePanelIn(panel);

      root.classList.add('is-mega-open');
      document.documentElement.classList.add('saibai-mega-open');

      trigger.setAttribute('aria-expanded', 'true');
      activeTrigger = trigger;
      activePanel = panel;

      var firstItem = panel.querySelector(MEGA_ITEM);
      if (firstItem) {
        setActiveSidebarItem(panel, firstItem);
        syncFeature(panel, firstItem);
        syncDrill(panel, firstItem);
      }
    }

    function openMega(trigger) {
      if (!megaLayer || !trigger) return;
      /* Mobile/tablet: só drawer — mega desktop não abre (evita overlay translúcido) */
      if (!isMegaDesktop()) {
        cancelOpenMega();
        finishCloseMega();
        return;
      }

      var panelId = trigger.getAttribute('aria-controls');
      var panel = panelId ? root.querySelector('#' + panelId) : null;
      if (!panel) return;

      if (activeTrigger === trigger && activePanel === panel && !megaLayer.hidden && !megaClosing) {
        closeMega();
        return;
      }

      cancelOpenMega();

      if (megaLayer && !megaLayer.hidden && !megaClosing) {
        openMegaNow(trigger);
        return;
      }

      if (reduceMotion) {
        openMegaNow(trigger);
        return;
      }

      pendingTrigger = trigger;
      root.classList.add('is-mega-pending');
      trigger.classList.add('is-pending');

      megaOpenTimer = window.setTimeout(function () {
        megaOpenTimer = null;
        root.classList.remove('is-mega-pending');
        trigger.classList.remove('is-pending');
        pendingTrigger = null;
        openMegaNow(trigger);
      }, MEGA_OPEN_DELAY);
    }

    var drawerHome = drawer ? drawer.parentNode : null;
    var scrollLockY = 0;

    /* Portal para body: fixed dentro de #header-group sticky fica preso à altura do header */
    function mountDrawerToBody() {
      if (!drawer || !document.body) return;
      if (drawer.parentNode !== document.body) {
        document.body.appendChild(drawer);
      }
      drawer.classList.add('is-portaled');
    }

    function restoreDrawerHome() {
      if (!drawer || !drawerHome) return;
      if (drawer.parentNode !== drawerHome) {
        drawerHome.appendChild(drawer);
      }
      drawer.classList.remove('is-portaled');
    }

    function lockBodyScroll(lock) {
      if (lock) {
        scrollLockY = window.scrollY || document.documentElement.scrollTop || 0;
        document.body.style.position = 'fixed';
        document.body.style.top = '-' + scrollLockY + 'px';
        document.body.style.left = '0';
        document.body.style.right = '0';
        document.body.style.width = '100%';
      } else {
        document.body.style.position = '';
        document.body.style.top = '';
        document.body.style.left = '';
        document.body.style.right = '';
        document.body.style.width = '';
        window.scrollTo(0, scrollLockY || 0);
      }
    }

    function openDrawer() {
      closeMega();
      if (!drawer) return;
      mountDrawerToBody();
      lockBodyScroll(true);
      drawer.hidden = false;
      document.documentElement.classList.add('saibai-header-drawer-open');
      if (openBtn) openBtn.setAttribute('aria-expanded', 'true');
    }

    function closeDrawer() {
      if (!drawer) return;
      drawer.hidden = true;
      document.documentElement.classList.remove('saibai-header-drawer-open');
      lockBodyScroll(false);
      restoreDrawerHome();
      if (openBtn) openBtn.setAttribute('aria-expanded', 'false');
    }

    for (var m = 0; m < megaPanels.length; m++) {
      initPanelItems(megaPanels[m]);
    }

    for (var tr = 0; tr < megaTriggers.length; tr++) {
      (function (trigger) {
        trigger.addEventListener('click', function (e) {
          e.preventDefault();
          openMega(trigger);
        });
      })(megaTriggers[tr]);
    }

    if (megaLayer) {
      var megaCloseEls = megaLayer.querySelectorAll(MEGA_CLOSE);
      for (var c = 0; c < megaCloseEls.length; c++) {
        megaCloseEls[c].addEventListener('click', closeMega);
      }

      var backdrop = megaLayer.querySelector('.saibai-mega-layer__backdrop');
      if (backdrop) {
        backdrop.addEventListener('click', closeMega);
      }
    }

    if (openBtn) {
      openBtn.addEventListener('click', openDrawer);
    }

    for (var i = 0; i < closeEls.length; i++) {
      closeEls[i].addEventListener('click', closeDrawer);
    }

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        closeMega();
        closeDrawer();
      }
    });

    var searchDetails = root.querySelectorAll('.saibai-header__search-details');
    for (var s = 0; s < searchDetails.length; s++) {
      (function (details) {
        details.addEventListener('toggle', function () {
          if (!details.open) return;
          closeMega();
          var input = details.querySelector('.search__input');
          if (input) {
            window.requestAnimationFrame(function () {
              input.focus();
            });
          }
        });
      })(searchDetails[s]);
    }
  }

  function boot() {
    var nodes = document.querySelectorAll(ROOT);
    for (var i = 0; i < nodes.length; i++) {
      initHeader(nodes[i]);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
