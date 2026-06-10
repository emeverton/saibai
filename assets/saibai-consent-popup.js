(function () {
  'use strict';

  var STORAGE_KEY = 'saibai_consent_v1';
  var ROOT_SELECTOR = '[data-saibai-consent]';
  var BODY_LOCK_CLASS = 'saibai-modal-scroll-lock';
  var scrollLockCount = 0;

  function measureScrollbarWidth() {
    return Math.max(0, window.innerWidth - document.documentElement.clientWidth);
  }

  function lockBodyScroll() {
    scrollLockCount += 1;
    if (scrollLockCount > 1) return;
    var scrollbarWidth = measureScrollbarWidth();
    document.documentElement.style.setProperty('--saibai-scrollbar-w', scrollbarWidth + 'px');
    document.body.classList.add(BODY_LOCK_CLASS);
  }

  function unlockBodyScroll() {
    scrollLockCount = Math.max(0, scrollLockCount - 1);
    if (scrollLockCount > 0) return;
    document.body.classList.remove(BODY_LOCK_CLASS);
    document.documentElement.style.removeProperty('--saibai-scrollbar-w');
  }

  window.SaibaiScrollLock = window.SaibaiScrollLock || {
    measureScrollbarWidth: measureScrollbarWidth,
    lock: lockBodyScroll,
    unlock: unlockBodyScroll
  };

  function readConsent() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (error) {
      return null;
    }
  }

  function writeConsent(consent) {
    try {
      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({
          essential: true,
          analytics: !!consent.analytics,
          marketing: !!consent.marketing,
          updated_at: Date.now()
        })
      );
    } catch (error) {
      /* ignore */
    }
  }

  function readConfig() {
    var node = document.getElementById('SaibaiTrackingConfig');
    if (!node) return {};
    try {
      return JSON.parse(node.textContent || '{}');
    } catch (error) {
      return {};
    }
  }

  function pushEvent(name, params) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(Object.assign({ event: name }, params || {}));
  }

  function loadScript(src, callback) {
    var script = document.createElement('script');
    script.async = true;
    script.src = src;
    script.onload = callback || function () {};
    document.head.appendChild(script);
  }

  function whenShopifyPrivacyReady(callback) {
    if (window.Shopify && window.Shopify.customerPrivacy) {
      callback(window.Shopify.customerPrivacy);
      return;
    }
    if (!window.Shopify || typeof window.Shopify.loadFeatures !== 'function') {
      callback(null);
      return;
    }
    window.Shopify.loadFeatures(
      [{ name: 'consent-tracking-api', version: '0.1' }],
      function (error) {
        callback(!error && window.Shopify.customerPrivacy ? window.Shopify.customerPrivacy : null);
      }
    );
  }

  function registerShopifyConsent(consent, callback) {
    whenShopifyPrivacyReady(function (privacy) {
      if (!privacy) {
        if (callback) callback();
        return;
      }
      privacy.setTrackingConsent(
        {
          analytics: !!consent.analytics,
          marketing: !!consent.marketing,
          preferences: true
        },
        callback || function () {}
      );
    });
  }

  function updateGtagConsent(consent) {
    window.gtag = window.gtag || function () {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push(arguments);
    };
    window.gtag('consent', 'update', {
      analytics_storage: consent.analytics ? 'granted' : 'denied',
      ad_storage: consent.marketing ? 'granted' : 'denied',
      ad_user_data: consent.marketing ? 'granted' : 'denied',
      ad_personalization: consent.marketing ? 'granted' : 'denied'
    });
  }

  function initGa4(config, consent) {
    if (!consent.analytics || !config.ga4_measurement_id) return;

    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () {
      window.dataLayer.push(arguments);
    };

    if (!window.__saibaiGa4Loaded) {
      window.__saibaiGa4Loaded = true;
      window.gtag('js', new Date());
      loadScript('https://www.googletagmanager.com/gtag/js?id=' + config.ga4_measurement_id, function () {
        window.gtag('config', config.ga4_measurement_id, { send_page_view: true });
      });

      document.addEventListener('click', function (e) {
        var btn = e.target.closest('[name="add"], .add-to-cart-button, .quick-add__submit');
        if (!btn || btn.disabled || typeof window.gtag !== 'function') return;
        var form = btn.closest('form[action*="/cart/add"]');
        var productId = form && form.querySelector('[name="id"]') ? form.querySelector('[name="id"]').value : '';
        window.gtag('event', 'add_to_cart', {
          currency: config.currency || 'BRL',
          items: [{ item_id: productId || 'unknown', quantity: 1 }]
        });
      });

      document.addEventListener('click', function (e) {
        var checkout = e.target.closest('[name="checkout"], a[href*="/checkout"]');
        if (!checkout || typeof window.gtag !== 'function') return;
        window.gtag('event', 'begin_checkout', { currency: config.currency || 'BRL' });
      });
    }

    if (config.page_type === 'product' && config.product && !window.__saibaiGa4ViewItem) {
      window.__saibaiGa4ViewItem = true;
      window.gtag('event', 'view_item', {
        currency: config.currency || 'BRL',
        value: config.product.price,
        items: [{
          item_id: config.product.id,
          item_name: config.product.title,
          price: config.product.price,
          quantity: 1
        }]
      });
    }
  }

  function initMeta(config, consent) {
    if (!consent.marketing || !config.meta_pixel_id || window.__saibaiMetaLoaded) return;
    window.__saibaiMetaLoaded = true;

    !function (f, b, e, v, n, t, s) {
      if (f.fbq) return;
      n = f.fbq = function () {
        n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
      };
      if (!f._fbq) f._fbq = n;
      n.push = n;
      n.loaded = !0;
      n.version = '2.0';
      n.queue = [];
      t = b.createElement(e);
      t.async = !0;
      t.src = v;
      s = b.getElementsByTagName(e)[0];
      s.parentNode.insertBefore(t, s);
    }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');

    window.fbq('init', config.meta_pixel_id);
    window.fbq('track', 'PageView');

    if (config.page_type === 'product' && config.product) {
      window.fbq('track', 'ViewContent', {
        content_name: config.product.title,
        content_ids: [config.product.id],
        content_type: 'product',
        value: config.product.price,
        currency: config.currency || 'BRL'
      });
    }
  }

  function applyTracking(consent) {
    var config = readConfig();
    updateGtagConsent(consent);
    initGa4(config, consent);
    initMeta(config, consent);
    pushEvent('saibai_consent_update', {
      analytics: consent.analytics,
      marketing: consent.marketing
    });
    document.dispatchEvent(new CustomEvent('saibai:consent-resolved', { detail: consent }));
  }

  function setOpen(root, open, focusSelector) {
    if (open) {
      root.removeAttribute('hidden');
      root.setAttribute('aria-hidden', 'false');
      lockBodyScroll();
      var focusTarget = focusSelector ? root.querySelector(focusSelector) : null;
      if (focusTarget) focusTarget.focus();
      return;
    }
    root.setAttribute('hidden', 'hidden');
    root.setAttribute('aria-hidden', 'true');
    unlockBodyScroll();
  }

  function showView(root, view) {
    var main = root.querySelector('[data-saibai-consent-main]');
    var prefs = root.querySelector('[data-saibai-consent-prefs]');
    if (main) main.hidden = view === 'prefs';
    if (prefs) prefs.hidden = view !== 'prefs';
  }

  function readPrefInputs(root) {
    var analyticsInput = root.querySelector('[data-saibai-consent-analytics]');
    var marketingInput = root.querySelector('[data-saibai-consent-marketing]');
    return {
      analytics: analyticsInput ? analyticsInput.checked : false,
      marketing: marketingInput ? marketingInput.checked : false
    };
  }

  function syncPrefInputs(root, consent) {
    var analyticsInput = root.querySelector('[data-saibai-consent-analytics]');
    var marketingInput = root.querySelector('[data-saibai-consent-marketing]');
    if (analyticsInput) analyticsInput.checked = !!consent.analytics;
    if (marketingInput) marketingInput.checked = !!consent.marketing;
  }

  function resolveConsent(root, consent) {
    writeConsent(consent);
    registerShopifyConsent(consent, function () {
      applyTracking(consent);
      setOpen(root, false);
    });
  }

  function openPreferences() {
    var root = document.querySelector(ROOT_SELECTOR);
    if (!root) return;
    syncPrefInputs(root, readConsent() || { analytics: false, marketing: false });
    showView(root, 'prefs');
    setOpen(root, true, '[data-saibai-consent-save]');
  }

  function isBannerVisible() {
    var root = document.querySelector(ROOT_SELECTOR);
    return !!(root && !root.hasAttribute('hidden'));
  }

  function initConsent(root) {
    if (!root || root.dataset.saibaiConsentReady === 'true') return;
    root.dataset.saibaiConsentReady = 'true';

    root.addEventListener('click', function (event) {
      var accept = event.target.closest('[data-saibai-consent-accept]');
      if (accept) {
        resolveConsent(root, { analytics: true, marketing: true });
        return;
      }

      var reject = event.target.closest('[data-saibai-consent-reject]');
      if (reject) {
        resolveConsent(root, { analytics: false, marketing: false });
        return;
      }

      if (event.target.closest('[data-saibai-consent-prefs-open]')) {
        showView(root, 'prefs');
        return;
      }

      if (event.target.closest('[data-saibai-consent-prefs-back]')) {
        showView(root, 'main');
        return;
      }

      if (event.target.closest('[data-saibai-consent-save]')) {
        resolveConsent(root, readPrefInputs(root));
      }
    });

    var saved = readConsent();
    if (saved) {
      registerShopifyConsent(saved, function () {
        applyTracking(saved);
      });
      return;
    }

    var bannerOpened = false;
    function showBannerOnce() {
      if (bannerOpened) return;
      bannerOpened = true;
      showView(root, 'main');
      setOpen(root, true, '[data-saibai-consent-accept]');
    }

    function scheduleBanner() {
      function run() {
        whenShopifyPrivacyReady(function (privacy) {
          if (privacy && typeof privacy.shouldShowBanner === 'function' && !privacy.shouldShowBanner()) {
            resolveConsent(root, { analytics: false, marketing: false });
            return;
          }
          showBannerOnce();
        });
      }

      function afterLoad() {
        if (window.requestIdleCallback) {
          window.requestIdleCallback(run, { timeout: 5000 });
        } else {
          setTimeout(run, 2500);
        }
      }

      if (document.readyState === 'complete') {
        afterLoad();
      } else {
        window.addEventListener('load', afterLoad, { once: true });
      }
    }

    scheduleBanner();
  }

  function bindOpenTriggers() {
    document.addEventListener('click', function (event) {
      var trigger = event.target.closest('[data-saibai-consent-open]');
      if (!trigger) return;
      event.preventDefault();
      openPreferences();
    });
  }

  function boot() {
    document.querySelectorAll(ROOT_SELECTOR).forEach(initConsent);
    bindOpenTriggers();
  }

  window.SaibaiConsent = {
    openPreferences: openPreferences,
    readConsent: readConsent,
    isBannerVisible: isBannerVisible
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
