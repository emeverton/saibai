(function () {
  'use strict';

  var STORAGE_KEY = 'saibai_coupon_popup_dismiss';
  var ROOT_SELECTOR = '[data-saibai-coupon]';
  var EXIT_THRESHOLD = 8;

  function readDismissed() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      var data = JSON.parse(raw);
      if (!data || !data.until) return null;
      if (Date.now() > data.until) {
        localStorage.removeItem(STORAGE_KEY);
        return null;
      }
      return data;
    } catch (error) {
      return null;
    }
  }

  function dismissPopup(expireDays) {
    var days = parseInt(expireDays, 10) || 7;
    try {
      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({ until: Date.now() + days * 24 * 60 * 60 * 1000 })
      );
    } catch (error) {
      /* ignore */
    }
  }

  function pushEvent(name, params) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(Object.assign({ event: name }, params || {}));
  }

  function isConsentBlocking() {
    if (window.SaibaiConsent && window.SaibaiConsent.isBannerVisible) {
      return window.SaibaiConsent.isBannerVisible();
    }
    var consent = document.querySelector('[data-saibai-consent]');
    return !!(consent && !consent.hasAttribute('hidden'));
  }

  function hasConsent() {
    return window.SaibaiConsent && typeof window.SaibaiConsent.readConsent === 'function'
      ? !!window.SaibaiConsent.readConsent()
      : false;
  }

  function isTouchUI() {
    if (window.matchMedia && window.matchMedia('(pointer: coarse)').matches) return true;
    return 'ontouchstart' in window;
  }

  function copyCode(code, statusEl, copyBtn) {
    var done = function (ok) {
      if (!statusEl) return;
      statusEl.hidden = false;
      statusEl.textContent = ok ? 'Cupom copiado!' : 'Selecione e copie: ' + code;
      if (copyBtn && ok) {
        var copyLabel = copyBtn.getAttribute('data-copy-label') || 'Copiar';
        copyBtn.textContent = 'Copiado';
        setTimeout(function () {
          copyBtn.textContent = copyLabel;
        }, 2000);
      }
    };

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(code).then(function () {
        done(true);
      }).catch(function () {
        done(false);
      });
      return;
    }

    var input = copyBtn && copyBtn.closest('[data-saibai-coupon]')
      ? copyBtn.closest('[data-saibai-coupon]').querySelector('.saibai-coupon__code')
      : null;
    if (input) {
      input.focus();
      input.select();
      try {
        done(document.execCommand('copy'));
      } catch (error) {
        done(false);
      }
    } else {
      done(false);
    }
  }

  function lockBodyScroll() {
    var lock = window.SaibaiScrollLock;
    if (lock && typeof lock.lock === 'function') {
      lock.lock();
      return;
    }
    var scrollbarWidth = Math.max(0, window.innerWidth - document.documentElement.clientWidth);
    document.documentElement.style.setProperty('--saibai-scrollbar-w', scrollbarWidth + 'px');
    document.body.classList.add('saibai-modal-scroll-lock');
  }

  function unlockBodyScroll() {
    var lock = window.SaibaiScrollLock;
    if (lock && typeof lock.unlock === 'function') {
      lock.unlock();
      return;
    }
    document.body.classList.remove('saibai-modal-scroll-lock');
    document.documentElement.style.removeProperty('--saibai-scrollbar-w');
  }

  function setOpen(root, open) {
    if (open) {
      root.removeAttribute('hidden');
      root.setAttribute('aria-hidden', 'false');
      lockBodyScroll();
      return;
    }
    root.setAttribute('hidden', 'hidden');
    root.setAttribute('aria-hidden', 'true');
    unlockBodyScroll();
  }

  function bindExitIntent(onTrigger) {
    var fired = false;

    function fire() {
      if (fired) return;
      fired = true;
      cleanup();
      onTrigger();
    }

    function handleMouseLeave(event) {
      if (event.clientY > EXIT_THRESHOLD) return;
      fire();
    }

    function handleMouseOut(event) {
      var related = event.relatedTarget || event.toElement;
      if (related) return;
      if (event.clientY > EXIT_THRESHOLD) return;
      fire();
    }

    document.documentElement.addEventListener('mouseleave', handleMouseLeave, { passive: true });
    document.addEventListener('mouseout', handleMouseOut, { passive: true });

    function cleanup() {
      document.documentElement.removeEventListener('mouseleave', handleMouseLeave);
      document.removeEventListener('mouseout', handleMouseOut);
    }

    return cleanup;
  }

  function bindBackButtonExit(onTrigger) {
    /* Trap de history.pushState desativado — quebrava o botão voltar / history.back().
       Mobile: dispara exit intent após idle curto, sem consumir navegação. */
    var fired = false;
    var timer = setTimeout(function () {
      if (fired) return;
      fired = true;
      onTrigger();
    }, 28000);

    return function () {
      clearTimeout(timer);
    };
  }

  function isPremiumBrowsePage() {
    var body = document.body;
    if (!body || !body.classList) return false;
    return body.classList.contains('template-collection')
      || body.classList.contains('template-product')
      || body.classList.contains('template-search');
  }

  function initPopup(root) {
    if (!root || root.dataset.saibaiCouponReady === 'true') return;
    if (readDismissed()) return;
    if (isPremiumBrowsePage()) return;

    root.dataset.saibaiCouponReady = 'true';

    var expireDays = root.getAttribute('data-expire-days') || '7';
    var armDelay = parseInt(root.getAttribute('data-arm-delay'), 10) || 0;
    var statusEl = root.querySelector('[data-saibai-coupon-status]');
    var copyBtn = root.querySelector('[data-saibai-coupon-copy]');
    var code = copyBtn ? copyBtn.getAttribute('data-code') || '' : '';
    var opened = false;
    var armed = false;
    var disarmTrigger = null;
    var armTimer = null;

    function canOpen() {
      return !opened && !readDismissed() && hasConsent() && !isConsentBlocking();
    }

    function trapFocus(event) {
      if (root.hasAttribute('hidden') || event.key !== 'Tab') return;
      var focusable = root.querySelectorAll(
        'button:not([disabled]), a[href], input:not([disabled]), [tabindex]:not([tabindex="-1"])'
      );
      if (!focusable.length) return;
      var first = focusable[0];
      var last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }

    function teardownListeners() {
      document.removeEventListener('keydown', onKeydown);
      document.removeEventListener('keydown', trapFocus);
      if (disarmTrigger) {
        disarmTrigger();
        disarmTrigger = null;
      }
      if (armTimer) {
        clearTimeout(armTimer);
        armTimer = null;
      }
    }

    function closePopup() {
      setOpen(root, false);
      teardownListeners();
      dismissPopup(expireDays);
    }

    function onKeydown(event) {
      if (event.key === 'Escape') closePopup();
    }

    function openPopup(trigger) {
      if (!canOpen()) return;
      opened = true;
      teardownListeners();
      setOpen(root, true);
      document.addEventListener('keydown', onKeydown);
      document.addEventListener('keydown', trapFocus);
      pushEvent('saibai_coupon_popup_view', { coupon_code: code, trigger: trigger });
      pushEvent('exit_intent', { source: 'saibai_coupon_popup', coupon_code: code, trigger: trigger });
      var closeBtn = root.querySelector('[data-saibai-coupon-close].saibai-coupon__close');
      if (closeBtn) closeBtn.focus();
    }

    function armExitTrigger() {
      if (isTouchUI()) {
        disarmTrigger = bindBackButtonExit(function () {
          openPopup('exit_intent_back');
        });
        return;
      }

      disarmTrigger = bindExitIntent(function () {
        openPopup('exit_intent');
      });
    }

    function armTrigger() {
      if (armed || !canOpen()) return;
      armed = true;

      armTimer = setTimeout(function () {
        armTimer = null;
        if (!canOpen()) return;
        armExitTrigger();
      }, armDelay);
    }

    root.addEventListener('click', function (event) {
      if (event.target.closest('[data-saibai-coupon-close]')) {
        closePopup();
        return;
      }

      if (event.target.closest('[data-saibai-coupon-copy]')) {
        copyCode(code, statusEl, copyBtn);
        pushEvent('saibai_coupon_copy', { coupon_code: code });
        return;
      }

      var cta = event.target.closest('[data-saibai-coupon-cta]');
      if (cta) {
        pushEvent('saibai_coupon_popup_click', {
          coupon_code: code,
          link_url: cta.getAttribute('data-href')
        });
        closePopup();
        var href = cta.getAttribute('data-href');
        if (href) window.location.href = href;
      }
    });

    if (hasConsent()) {
      armTrigger();
    } else {
      document.addEventListener('saibai:consent-resolved', function onConsent() {
        document.removeEventListener('saibai:consent-resolved', onConsent);
        armTrigger();
      });
    }
  }

  function boot() {
    document.querySelectorAll(ROOT_SELECTOR).forEach(initPopup);
  }

  window.SaibaiCoupon = {
    readDismissed: readDismissed
  };

  function applyCartCoupon(hint) {
    var code = hint.getAttribute('data-code');
    if (!code) return;

    var scope = hint.closest('modal-component') || hint.closest('cart-drawer') || document;
    var form = scope.querySelector('form.cart-discount__form');
    var input = form ? form.querySelector('input[name="discount"]') : null;
    var submitBtn = form ? form.querySelector('.cart-discount__button, button[type="submit"]') : null;

    if (!input || !form) {
      pushEvent('saibai_cart_coupon_apply_fail', { coupon_code: code, reason: 'no_form' });
      return;
    }

    input.value = code;
    input.dispatchEvent(new Event('input', { bubbles: true }));
    pushEvent('saibai_cart_coupon_apply', { coupon_code: code });

    if (typeof form.requestSubmit === 'function') {
      form.requestSubmit(submitBtn || undefined);
      return;
    }
    if (submitBtn) {
      submitBtn.click();
      return;
    }
    form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
  }

  function initCartHints() {
    document.addEventListener('click', function (event) {
      var btn = event.target.closest('[data-saibai-cart-coupon-apply]');
      if (!btn) return;
      event.preventDefault();
      var hint = btn.closest('[data-saibai-cart-coupon-hint]');
      if (hint) applyCartCoupon(hint);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
  initCartHints();
})();
