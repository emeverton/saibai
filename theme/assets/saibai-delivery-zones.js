/**
 * Empório Saibai — zonas de entrega (Brasil, todas as UFs).
 * Valida CEP via ViaCEP (UF) e exige CEP brasileiro no checkout.
 * Build 2026-09-02.
 */
(function () {
  'use strict';

  if (window.SaibaiDelivery) return;

  var STORAGE_KEY = 'saibai_delivery_zone_v5';
  var MSG_OUT =
    'Informe um CEP válido no Brasil. Entregamos em todo o território nacional.';
  var MSG_TRANSIT =
    'Fora de São Paulo, o produto pode sofrer algumas alterações devido ao tempo de entrega.';
  var MSG_OK_PREFIX = 'Entregamos em ';
  var WHATSAPP =
    (window.saibaiDeliveryZones && window.saibaiDeliveryZones.whatsapp) ||
    'https://wa.me/551530101451';

  var BRASIL_UFS = (window.saibaiDeliveryZones && window.saibaiDeliveryZones.ufs) || [
    'AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG',
    'PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO'
  ];

  /* Faixas CEP oficiais Brasil (8 dígitos). Fallback se ViaCEP falhar em UF. */
  var CEP_RANGES = [
    [1000000, 99999999]
  ];

  function onlyDigits(value) {
    return String(value || '').replace(/\D/g, '');
  }

  function formatCep(value) {
    var d = onlyDigits(value).slice(0, 8);
    if (d.length <= 5) return d;
    return d.slice(0, 5) + '-' + d.slice(5);
  }

  function normalize(text) {
    return String(text || '')
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9\s]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }

  function isOutsideSp(uf) {
    return String(uf || '').toUpperCase() !== 'SP';
  }

  function ufAllowed(uf) {
    var u = String(uf || '').toUpperCase();
    var i;
    for (i = 0; i < BRASIL_UFS.length; i++) {
      if (BRASIL_UFS[i] === u) return true;
    }
    return false;
  }

  function cepInRanges(digits) {
    var n = parseInt(onlyDigits(digits), 10);
    if (isNaN(n)) return false;
    var i;
    for (i = 0; i < CEP_RANGES.length; i++) {
      if (n >= CEP_RANGES[i][0] && n <= CEP_RANGES[i][1]) return true;
    }
    return false;
  }

  function isEligibleAddress(address) {
    if (!address || address.erro) return false;
    if (ufAllowed(address.uf)) return true;
    /* Fallback CEP se UF ausente (raro) */
    return cepInRanges(address.cep);
  }

  function fetchCep(cep) {
    var digits = onlyDigits(cep);
    if (digits.length !== 8) {
      return Promise.reject(new Error('cep_invalid'));
    }
    return fetch('https://viacep.com.br/ws/' + digits + '/json/')
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        if (!data || data.erro) throw new Error('cep_not_found');
        return data;
      });
  }

  function readState() {
    try {
      var raw = window.sessionStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      return JSON.parse(raw);
    } catch (e) {
      return null;
    }
  }

  function writeState(state) {
    try {
      if (!state) {
        window.sessionStorage.removeItem(STORAGE_KEY);
        return;
      }
      window.sessionStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch (e) {
      /* ignore */
    }
  }

  function syncCartAttributes(state) {
    var attrs = {
      delivery_cep: state && state.ok ? state.cep : '',
      delivery_bairro: state && state.ok ? state.bairro : '',
      delivery_city: state && state.ok ? state.city : '',
      delivery_uf: state && state.ok ? state.uf : '',
      delivery_zone_ok: state && state.ok ? '1' : '0'
    };
    return fetch('/cart/update.js', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      credentials: 'same-origin',
      body: JSON.stringify({ attributes: attrs })
    }).catch(function () {
      return null;
    });
  }

  function rememberFromAddress(address, ok) {
    var digits = onlyDigits(address && address.cep);
    var state = {
      ok: !!ok,
      cep: formatCep(digits),
      bairro: (address && address.bairro) || '',
      city: (address && address.localidade) || '',
      uf: (address && address.uf) || '',
      checkedAt: Date.now()
    };
    writeState(state);
    syncCartAttributes(state);
    return state;
  }

  function validateCep(cep) {
    var digits = onlyDigits(cep);
    return fetchCep(digits).then(function (address) {
      var ok = isEligibleAddress(address);
      var state = rememberFromAddress(address, ok);
      return {
        ok: ok,
        address: address,
        state: state,
        message: ok
          ? MSG_OK_PREFIX +
            (address.bairro ? address.bairro + ', ' : '') +
            address.localidade +
            (address.uf ? ' — ' + address.uf : '') +
            '.'
          : MSG_OUT
      };
    });
  }

  function isCheckoutAllowed() {
    var state = readState();
    return !!(state && state.ok === true);
  }

  function setCheckoutDisabled(disabled, reason) {
    var buttons = document.querySelectorAll(
      'button[name="checkout"], .cart__checkout-button, a[href*="/checkout"]'
    );
    var i;
    for (i = 0; i < buttons.length; i++) {
      var btn = buttons[i];
      if (btn.tagName === 'A') {
        if (disabled) {
          btn.setAttribute('aria-disabled', 'true');
          btn.classList.add('saibai-delivery-locked-link');
          btn.addEventListener('click', blockAnchorCheckout, true);
        } else {
          btn.removeAttribute('aria-disabled');
          btn.classList.remove('saibai-delivery-locked-link');
          btn.removeEventListener('click', blockAnchorCheckout, true);
        }
      } else if (disabled) {
        btn.setAttribute('disabled', 'disabled');
        btn.setAttribute('data-saibai-delivery-locked', '1');
        if (reason) btn.setAttribute('title', reason);
      } else if (btn.getAttribute('data-saibai-delivery-locked') === '1') {
        btn.removeAttribute('data-saibai-delivery-locked');
        btn.removeAttribute('title');
        var wrapper = btn.closest('[data-purchase-conditions]');
        var checkbox = wrapper ? wrapper.querySelector('[id^="agree_condition-"]') : null;
        if (checkbox) {
          btn.disabled = !checkbox.checked;
        } else {
          btn.removeAttribute('disabled');
        }
      }
    }

    document.documentElement.classList.toggle('saibai-delivery-locked', disabled);
    document.documentElement.classList.toggle('saibai-delivery-ok', !disabled);

    var dyn = document.querySelectorAll('.additional-checkout-buttons, .cart__dynamic-checkout-buttons');
    for (i = 0; i < dyn.length; i++) {
      dyn[i].hidden = !!disabled;
      dyn[i].style.display = disabled ? 'none' : '';
    }
  }

  function blockAnchorCheckout(e) {
    if (!isCheckoutAllowed()) {
      e.preventDefault();
      e.stopPropagation();
      focusGate();
    }
  }

  function focusGate() {
    var input = document.querySelector('[data-saibai-delivery-cep]');
    if (input) {
      input.focus();
      input.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }

  function gateHtml() {
    return (
      '<div class="saibai-delivery-gate" data-saibai-delivery-gate>' +
      '<p class="saibai-delivery-gate__label">CEP de entrega</p>' +
      '<p class="saibai-delivery-gate__hint">Entregamos em todo o Brasil. Valor e prazo no checkout (Flex Frete).</p>' +
      '<form class="saibai-delivery-gate__form" data-saibai-delivery-form novalidate>' +
      '<label class="visually-hidden" for="SaibaiDeliveryCep">CEP</label>' +
      '<input id="SaibaiDeliveryCep" class="saibai-delivery-gate__input" type="text" inputmode="numeric" autocomplete="postal-code" placeholder="00000-000" maxlength="9" required data-saibai-delivery-cep>' +
      '<button type="submit" class="saibai-delivery-gate__btn" data-saibai-delivery-submit>Verificar</button>' +
      '</form>' +
      '<p class="saibai-delivery-gate__msg" data-saibai-delivery-msg hidden role="status" aria-live="polite"></p>' +
      '<p class="saibai-delivery-gate__transit" data-saibai-delivery-transit hidden role="note"></p>' +
      '<p class="saibai-delivery-gate__out" data-saibai-delivery-out hidden>' +
      '<a href="' +
      WHATSAPP +
      '" target="_blank" rel="noopener noreferrer">Falar no WhatsApp sobre outras regiões</a>' +
      ' · <a href="/pages/politica-de-entrega">Ver áreas atendidas</a>' +
      '</p>' +
      '</div>'
    );
  }

  function showTransit(gate, uf, ok) {
    var note = gate.querySelector('[data-saibai-delivery-transit]');
    if (!note) return;
    var show = !!(ok && uf && isOutsideSp(uf));
    note.hidden = !show;
    note.textContent = show ? MSG_TRANSIT : '';
  }

  function showMsg(gate, text, kind, uf) {
    var msg = gate.querySelector('[data-saibai-delivery-msg]');
    var out = gate.querySelector('[data-saibai-delivery-out]');
    if (!msg) return;
    msg.hidden = !text;
    msg.textContent = text || '';
    msg.className =
      'saibai-delivery-gate__msg' +
      (kind === 'ok' ? ' is-ok' : '') +
      (kind === 'err' ? ' is-err' : '');
    if (out) out.hidden = kind !== 'err';
    showTransit(gate, uf, kind === 'ok');
  }

  function bindGate(gate) {
    if (!gate || gate.dataset.bound === 'true') return;
    gate.dataset.bound = 'true';

    var form = gate.querySelector('[data-saibai-delivery-form]');
    var input = gate.querySelector('[data-saibai-delivery-cep]');
    var btn = gate.querySelector('[data-saibai-delivery-submit]');
    if (!form || !input) return;

    var existing = readState();
    if (existing && existing.cep) {
      input.value = existing.cep;
      if (existing.ok) {
        showMsg(
          gate,
          MSG_OK_PREFIX +
            (existing.bairro ? existing.bairro + ', ' : '') +
            existing.city +
            (existing.uf ? ' — ' + existing.uf : '') +
            '.',
          'ok',
          existing.uf
        );
        setCheckoutDisabled(false);
      } else {
        showMsg(gate, MSG_OUT, 'err');
        setCheckoutDisabled(true, MSG_OUT);
      }
    } else {
      setCheckoutDisabled(true, 'Informe um CEP de entrega no Brasil para continuar.');
    }

    input.addEventListener('input', function () {
      input.value = formatCep(input.value);
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var cep = onlyDigits(input.value);
      if (cep.length !== 8) {
        showMsg(gate, 'Informe um CEP válido com 8 dígitos.', 'err');
        setCheckoutDisabled(true, MSG_OUT);
        return;
      }
      if (btn) {
        btn.disabled = true;
        btn.setAttribute('aria-busy', 'true');
      }
      validateCep(cep)
        .then(function (result) {
          showMsg(gate, result.message, result.ok ? 'ok' : 'err', result.state && result.state.uf);
          setCheckoutDisabled(!result.ok, result.message);
        })
        .catch(function () {
          showMsg(gate, 'Não foi possível validar este CEP. Tente novamente.', 'err');
          setCheckoutDisabled(true, MSG_OUT);
        })
        .finally(function () {
          if (btn) {
            btn.disabled = false;
            btn.removeAttribute('aria-busy');
          }
        });
    });
  }

  function ensureGates() {
    var hosts = document.querySelectorAll('[data-purchase-conditions]');
    var i;
    for (i = 0; i < hosts.length; i++) {
      var host = hosts[i];
      if (host.querySelector('[data-saibai-delivery-gate]')) continue;
      var ctas = host.querySelector('.cart__ctas');
      var wrap = document.createElement('div');
      wrap.innerHTML = gateHtml();
      var gate = wrap.firstChild;
      if (ctas) {
        host.insertBefore(gate, ctas);
      } else {
        host.insertBefore(gate, host.firstChild);
      }
      bindGate(gate);
    }

    var gates = document.querySelectorAll('[data-saibai-delivery-gate]');
    for (i = 0; i < gates.length; i++) {
      bindGate(gates[i]);
    }

    if (!isCheckoutAllowed()) {
      setCheckoutDisabled(true, 'Informe um CEP de entrega no Brasil para continuar.');
    } else {
      setCheckoutDisabled(false);
    }
  }

  function interceptCheckoutClicks() {
    document.addEventListener(
      'click',
      function (e) {
        var t = e.target && e.target.closest
          ? e.target.closest('button[name="checkout"], .cart__checkout-button, a[href*="/checkout"]')
          : null;
        if (!t) return;
        if (isCheckoutAllowed()) return;
        e.preventDefault();
        e.stopPropagation();
        ensureGates();
        focusGate();
      },
      true
    );

    document.addEventListener(
      'submit',
      function (e) {
        var form = e.target;
        if (!form || !form.querySelector) return;
        var checkoutBtn = form.querySelector('button[name="checkout"]');
        if (!checkoutBtn && form.getAttribute('action') && form.getAttribute('action').indexOf('/cart') === -1) {
          return;
        }
        if (!isCheckoutAllowed() && (checkoutBtn || (e.submitter && e.submitter.name === 'checkout'))) {
          e.preventDefault();
          e.stopPropagation();
          ensureGates();
          focusGate();
        }
      },
      true
    );
  }

  function init() {
    ensureGates();
  }

  window.SaibaiDelivery = {
    formatCep: formatCep,
    onlyDigits: onlyDigits,
    normalize: normalize,
    isEligibleAddress: isEligibleAddress,
    validateCep: validateCep,
    fetchCep: fetchCep,
    rememberFromAddress: rememberFromAddress,
    isCheckoutAllowed: isCheckoutAllowed,
    getState: readState,
    messageOut: MSG_OUT,
    transitMessage: MSG_TRANSIT,
    isOutsideSp: isOutsideSp,
    brasilUfs: BRASIL_UFS.slice(),
    sudesteUfs: BRASIL_UFS.slice(),
    refresh: ensureGates
  };

  interceptCheckoutClicks();

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  document.addEventListener('shopify:section:load', init);
  document.addEventListener('cart:updated', init);
  document.addEventListener('cart-drawer:open', init);

  if (typeof MutationObserver === 'function') {
    var moTimer = null;
    var mo = new MutationObserver(function () {
      if (moTimer) window.clearTimeout(moTimer);
      moTimer = window.setTimeout(function () {
        if (
          document.querySelector('[data-purchase-conditions]') &&
          !document.querySelector('[data-saibai-delivery-gate]')
        ) {
          ensureGates();
        }
      }, 120);
    });
    mo.observe(document.body, { childList: true, subtree: true });
  }
})();
