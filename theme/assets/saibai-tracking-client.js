(function () {
  'use strict';

  var COOKIE_VISITOR = 'vlt_visitor_id';
  var COOKIE_SESSION = 'vlt_session_id';
  var ATTR_KEYS = [
    'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term',
    'gclid', 'fbclid', 'ttclid', 'msclkid'
  ];
  var SCROLL_MARKS = [25, 50, 75, 90];
  var scrollSent = {};
  var ready = false;
  var consent = { analytics: false, marketing: false };

  function readConfig() {
    var node = document.getElementById('SaibaiTrackingConfig');
    if (!node) return null;
    try {
      return JSON.parse(node.textContent || '{}');
    } catch (e) {
      return null;
    }
  }

  function readCookie(name) {
    var match = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'));
    return match ? decodeURIComponent(match[1]) : undefined;
  }

  function writeCookie(name, value, days) {
    var expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = name + '=' + encodeURIComponent(value) + '; expires=' + expires + '; path=/; SameSite=Lax';
  }

  function ensureIds() {
    var visitorId = readCookie(COOKIE_VISITOR);
    if (!visitorId) {
      visitorId = (window.crypto && crypto.randomUUID) ? crypto.randomUUID() : 'v_' + Date.now();
      writeCookie(COOKIE_VISITOR, visitorId, 365);
    }
    var sessionId = readCookie(COOKIE_SESSION);
    if (!sessionId) {
      sessionId = (window.crypto && crypto.randomUUID) ? crypto.randomUUID() : 's_' + Date.now();
      writeCookie(COOKIE_SESSION, sessionId, 1);
    }
    return { visitorId: visitorId, sessionId: sessionId };
  }

  function captureAttribution() {
    var params = new URLSearchParams(window.location.search);
    var data = {};
    var i;
    for (i = 0; i < ATTR_KEYS.length; i++) {
      var key = ATTR_KEYS[i];
      var value = params.get(key);
      if (value) {
        data[key] = value;
        try { localStorage.setItem('vlt_' + key, value); } catch (e) { /* ignore */ }
      } else {
        try {
          var stored = localStorage.getItem('vlt_' + key);
          if (stored) data[key] = stored;
        } catch (e) { /* ignore */ }
      }
    }
    if (!data.landing_page) {
      try {
        data.landing_page = localStorage.getItem('vlt_landing_page') || window.location.href;
        if (!localStorage.getItem('vlt_landing_page')) {
          localStorage.setItem('vlt_landing_page', window.location.href);
        }
      } catch (e) {
        data.landing_page = window.location.href;
      }
    }
    return data;
  }

  function readFbpFbc() {
    return {
      fbp: readCookie('_fbp'),
      fbc: readCookie('_fbc')
    };
  }

  function track(eventName, payload) {
    if (!ready) return Promise.resolve(null);

    var config = readConfig();
    if (!config || !config.tracking_endpoint) return Promise.resolve(null);

    var ids = ensureIds();
    var attribution = captureAttribution();
    var fb = readFbpFbc();
    var body = {
      event_id: (window.crypto && crypto.randomUUID) ? crypto.randomUUID() : 'e_' + Date.now(),
      event_name: eventName,
      event_time: Math.floor(Date.now() / 1000),
      source: 'shopify',
      shopify_shop_id: config.shop_id,
      visitor_id: ids.visitorId,
      session_id: ids.sessionId,
      page_url: window.location.href,
      referrer: document.referrer || undefined,
      user_agent: navigator.userAgent,
      consent_analytics: !!consent.analytics,
      consent_marketing: !!consent.marketing,
      fbp: fb.fbp,
      fbc: fb.fbc
    };

    var key;
    for (key in attribution) {
      if (Object.prototype.hasOwnProperty.call(attribution, key)) {
        body[key] = attribution[key];
      }
    }
    if (payload) {
      for (key in payload) {
        if (Object.prototype.hasOwnProperty.call(payload, key)) {
          body[key] = payload[key];
        }
      }
    }

    if (config.page_type === 'product' && config.product && !body.product_id) {
      body.product_id = String(config.product.id);
      body.value = body.value != null ? body.value : config.product.price;
      body.currency = body.currency || config.currency || 'BRL';
    }

    return fetch(config.tracking_endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      credentials: 'same-origin',
      keepalive: true
    }).catch(function () { return null; });
  }

  function bindDomEvents() {
    document.addEventListener('submit', function (e) {
      var form = e.target;
      if (!form || !form.action || form.action.indexOf('/cart/add') === -1) return;
      var idInput = form.querySelector('[name="id"]');
      track('add_to_cart', {
        variant_id: idInput ? idInput.value : undefined,
        quantity: 1
      });
    }, true);

    document.addEventListener('click', function (e) {
      var target = e.target;
      if (!target || !target.closest) return;

      if (target.closest('[name="checkout"], a[href*="/checkout"]')) {
        track('begin_checkout', { currency: (readConfig() || {}).currency || 'BRL' });
        return;
      }

      if (target.closest('[data-saibai-track="whatsapp"], a[href*="wa.me"], a[href*="whatsapp.com"]')) {
        track('whatsapp_click', { properties: { href: target.closest('a').href } });
        return;
      }
      if (target.closest('[data-saibai-track="phone"], a[href^="tel:"]')) {
        track('phone_click', { properties: { href: target.closest('a').href } });
        return;
      }
      if (target.closest('[data-saibai-track="email"], a[href^="mailto:"]')) {
        track('email_click', { properties: { href: target.closest('a').href } });
        return;
      }
      if (target.closest('[data-saibai-track="cta"]')) {
        var el = target.closest('[data-saibai-track="cta"]');
        track('cta_click', { properties: { label: (el.textContent || '').trim() } });
      }
    });

    window.addEventListener('scroll', function () {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      if (max <= 0) return;
      var pct = Math.round((window.scrollY / max) * 100);
      var i;
      for (i = 0; i < SCROLL_MARKS.length; i++) {
        var mark = SCROLL_MARKS[i];
        if (pct >= mark && !scrollSent[mark]) {
          scrollSent[mark] = true;
          track('scroll_depth', { properties: { depth: mark } });
        }
      }
    }, { passive: true });
  }

  function bindShopifyAnalytics() {
    if (!window.Shopify || !window.Shopify.analytics || typeof window.Shopify.analytics.subscribe !== 'function') {
      return;
    }

    var map = {
      page_viewed: 'page_view',
      product_viewed: 'product_view',
      collection_viewed: 'collection_view',
      search_submitted: 'search',
      product_added_to_cart: 'add_to_cart',
      product_removed_from_cart: 'remove_from_cart',
      checkout_started: 'begin_checkout',
      checkout_shipping_info_submitted: 'add_shipping_info',
      payment_info_submitted: 'add_payment_info',
      checkout_completed: 'purchase'
    };

    var events = Object.keys(map);
    var i;
    for (i = 0; i < events.length; i++) {
      (function (shopifyName) {
        window.Shopify.analytics.subscribe(shopifyName, function (event) {
          var payload = (event && event.data) || {};
          track(map[shopifyName], {
            product_id: payload.productVariant && payload.productVariant.product
              ? String(payload.productVariant.product.id) : undefined,
            variant_id: payload.productVariant ? String(payload.productVariant.id) : undefined,
            order_id: payload.checkout && payload.checkout.order
              ? String(payload.checkout.order.id) : undefined,
            checkout_id: payload.checkout ? payload.checkout.token : undefined,
            value: payload.checkout && payload.checkout.totalPrice
              ? parseFloat(payload.checkout.totalPrice.amount) : undefined,
            currency: payload.checkout && payload.checkout.totalPrice
              ? payload.checkout.totalPrice.currencyCode : undefined
          });
        });
      })(events[i]);
    }
  }

  function initWithConsent(detail) {
    consent.analytics = !!(detail && detail.analytics);
    consent.marketing = !!(detail && detail.marketing);
    if (!consent.analytics && !consent.marketing) return;

    if (ready) return;
    ready = true;

    function startTracking() {
      ensureIds();
      captureAttribution();
      bindDomEvents();
      bindShopifyAnalytics();

      var config = readConfig();
      if (config && config.page_type === 'product' && config.product) {
        track('product_view', {
          product_id: String(config.product.id),
          value: config.product.price,
          currency: config.currency || 'BRL'
        });
      } else {
        track('page_view');
      }
    }

    if ('requestIdleCallback' in window) {
      requestIdleCallback(startTracking, { timeout: 1500 });
    } else {
      setTimeout(startTracking, 1000);
    }
  }

  function boot() {
    document.addEventListener('saibai:consent-resolved', function (e) {
      initWithConsent(e.detail || {});
    });

    if (window.SaibaiConsent && typeof window.SaibaiConsent.readConsent === 'function') {
      var saved = window.SaibaiConsent.readConsent();
      if (saved && (saved.analytics || saved.marketing)) {
        initWithConsent(saved);
      }
    }
  }

  window.SaibaiTracking = { track: track, init: initWithConsent };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
