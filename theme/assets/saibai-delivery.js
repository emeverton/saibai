/**
 * Empório Saibai — gate de entrega Brasil (todas as UFs).
 * Fonte única de validação de CEP/checkout. Build 2026-09-02.
 */
(() => {
  'use strict';
  if (window.__saibaiDeliveryInit) return;
  window.__saibaiDeliveryInit = true;
  const cfg = window.saibaiCartPolicy || {};
  const fetchDirect = window.fetch.bind(window);
  const allowedStates = Array.isArray(cfg.allowedStates) && cfg.allowedStates.length
    ? cfg.allowedStates.map((uf) => String(uf || '').toUpperCase()).filter(Boolean)
    : ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO'];
  const storageKey = 'saibai_delivery_zone_v5';
  const outMessage = cfg.outMessage ||
    'Informe um CEP válido no Brasil. Entregamos em todo o território nacional.';
  const transitMessage = cfg.transitMessage ||
    'Fora de São Paulo, o produto pode sofrer algumas alterações devido ao tempo de entrega.';
  const okPrefix = cfg.okPrefix || 'Entregamos em ';
  const isOutsideSp = (uf) => String(uf || '').toUpperCase() !== 'SP';
  const whatsapp = cfg.whatsapp || 'https://wa.me/551530101451';
  const policyUrl = cfg.policyUrl || '/pages/politica-de-entrega';
  const digits = (value) => String(value || '').replace(/\D/g, '');
  const formatCep = (value) => {
    const cep = digits(value).slice(0, 8);
    return cep.length > 5 ? `${cep.slice(0, 5)}-${cep.slice(5)}` : cep;
  };
  const normalize = (value) => String(value || '')
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9\s]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
  const ufAllowed = (uf) => allowedStates.includes(String(uf || '').toUpperCase());
  const readState = () => {
    try {
      const state = JSON.parse(sessionStorage.getItem(storageKey) || 'null');
      return state && ufAllowed(state.uf) ? state : null;
    } catch (_) {
      return null;
    }
  };
  const writeState = (state) => {
    try {
      if (state) sessionStorage.setItem(storageKey, JSON.stringify(state));
      else sessionStorage.removeItem(storageKey);
    } catch (_) {}
  };
  const eligible = (address) => Boolean(
    address && !address.erro && ufAllowed(address.uf)
  );
  const fetchCep = async (value) => {
    const cep = digits(value);
    if (cep.length !== 8) throw new Error('cep_invalid');
    const controller = typeof AbortController === 'function' ? new AbortController() : null;
    const timer = controller ? setTimeout(() => controller.abort(), 6500) : null;
    try {
      const response = await fetchDirect(`https://viacep.com.br/ws/${cep}/json/`, {
        signal: controller?.signal,
      });
      if (!response.ok) throw new Error(`cep_http_${response.status}`);
      const address = await response.json();
      if (!address || address.erro) throw new Error('cep_not_found');
      return address;
    } finally {
      if (timer) clearTimeout(timer);
    }
  };
  const syncAttributes = (state) => fetchDirect('/cart/update.js', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
    credentials: 'same-origin',
    body: JSON.stringify({
      attributes: {
        delivery_cep: state?.ok ? state.cep : '',
        delivery_bairro: state?.ok ? state.bairro : '',
        delivery_city: state?.ok ? state.city : '',
        delivery_uf: state?.ok ? state.uf : '',
        delivery_zone_ok: state?.ok ? '1' : '0',
      },
    }),
  }).catch(() => null);
  const remember = (address, ok) => {
    const state = {
      ok: Boolean(ok),
      cep: formatCep(address?.cep),
      bairro: address?.bairro || '',
      city: address?.localidade || '',
      uf: String(address?.uf || '').toUpperCase(),
      checkedAt: Date.now(),
    };
    writeState(state);
    syncAttributes(state);
    return state;
  };
  const validateCep = async (value) => {
    const address = await fetchCep(value);
    const ok = eligible(address);
    const state = remember(address, ok);
    return {
      ok,
      address,
      state,
      message: ok
        ? `${okPrefix}${address.bairro ? `${address.bairro}, ` : ''}${address.localidade}${address.uf ? ` — ${address.uf}` : ''}.`
        : outMessage,
    };
  };
  const checkoutAllowed = () => readState()?.ok === true;
  function focusGate() {
    ensureGates();
    const input = [...document.querySelectorAll('[data-saibai-delivery-cep]')]
      .find((element) => element.getClientRects().length);
    input?.focus();
    input?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
  const blockAnchor = (event) => {
    if (checkoutAllowed()) return;
    event.preventDefault();
    event.stopPropagation();
    focusGate();
  };
  const setCheckoutLock = (locked, reason = outMessage) => {
    const selector = 'button[name="checkout"], .cart__checkout-button, a[href*="/checkout"]';
    document.querySelectorAll(selector).forEach((control) => {
      if (control instanceof HTMLAnchorElement) {
        control.classList.toggle('saibai-delivery-locked-link', locked);
        control.toggleAttribute('aria-disabled', locked);
        control.removeEventListener('click', blockAnchor, true);
        if (locked) control.addEventListener('click', blockAnchor, true);
        return;
      }
      if (locked) {
        control.dataset.saibaiDeliveryLocked = 'true';
        control.disabled = true;
        control.title = reason;
        return;
      }
      if (control.dataset.saibaiDeliveryLocked !== 'true') return;
      delete control.dataset.saibaiDeliveryLocked;
      control.removeAttribute('title');
      const empty = control.closest(
        'cart-drawer.is-empty, cart-drawer-items.is-empty, cart-items-component.is-empty'
      );
      const checkbox = control
        .closest('[data-purchase-conditions]')
        ?.querySelector('[id^="agree_condition-"]');
      control.disabled = Boolean(empty || (checkbox && !checkbox.checked));
    });
    document.documentElement.classList.toggle('saibai-delivery-locked', locked);
    document.body?.classList.toggle('saibai-delivery-locked', locked);
    document.querySelectorAll('.additional-checkout-buttons, .cart__dynamic-checkout-buttons')
      .forEach((element) => {
        element.hidden = locked;
        element.style.display = locked ? 'none' : '';
      });
  };
  let sequence = 0;
  const createGate = () => {
    sequence += 1;
    const inputId = `SaibaiDeliveryCep-${sequence}`;
    const gate = document.createElement('div');
    gate.className = 'saibai-delivery-gate';
    gate.dataset.saibaiDeliveryGate = '';
    gate.innerHTML = `
      <p class="saibai-delivery-gate__label">CEP de entrega</p>
      <p class="saibai-delivery-gate__hint">Entregamos em todo o Brasil. Valor e prazo no checkout (Flex Frete).</p>
      <form class="saibai-delivery-gate__form" data-saibai-delivery-form novalidate>
        <label class="visually-hidden" for="${inputId}">CEP</label>
        <input id="${inputId}" class="saibai-delivery-gate__input" type="text"
          inputmode="numeric" autocomplete="postal-code" placeholder="00000-000"
          maxlength="9" required data-saibai-delivery-cep>
        <button type="submit" class="saibai-delivery-gate__btn"
          data-saibai-delivery-submit>Verificar</button>
      </form>
      <p class="saibai-delivery-gate__msg" data-saibai-delivery-msg hidden
        role="status" aria-live="polite"></p>
      <p class="saibai-delivery-gate__transit" data-saibai-delivery-transit hidden role="note"></p>
      <p class="saibai-delivery-gate__out" data-saibai-delivery-out hidden>
        <a href="${whatsapp}" target="_blank" rel="noopener noreferrer">Falar no WhatsApp</a>
        · <a href="${policyUrl}">Ver política de entrega</a>
      </p>`;
    return gate;
  };
  const showTransit = (gate, uf, ok) => {
    const note = gate.querySelector('[data-saibai-delivery-transit]');
    if (!note) return;
    const show = Boolean(ok && uf && isOutsideSp(uf));
    note.hidden = !show;
    note.textContent = show ? transitMessage : '';
  };
  const showMessage = (gate, text, status, uf) => {
    const message = gate.querySelector('[data-saibai-delivery-msg]');
    const out = gate.querySelector('[data-saibai-delivery-out]');
    if (!message) return;
    message.hidden = !text;
    message.textContent = text || '';
    message.className =
      `saibai-delivery-gate__msg${status === 'ok' ? ' is-ok' : ''}${status === 'err' ? ' is-err' : ''}`;
    if (out) out.hidden = status !== 'err';
    showTransit(gate, uf, status === 'ok');
  };
  const bindGate = (gate) => {
    if (!gate || gate.dataset.bound === 'true') return;
    gate.dataset.bound = 'true';
    const form = gate.querySelector('[data-saibai-delivery-form]');
    const input = gate.querySelector('[data-saibai-delivery-cep]');
    const button = gate.querySelector('[data-saibai-delivery-submit]');
    if (!form || !input) return;
    const state = readState();
    if (state?.cep) {
      input.value = state.cep;
      showMessage(
        gate,
        state.ok
          ? `${okPrefix}${state.bairro ? `${state.bairro}, ` : ''}${state.city}${state.uf ? ` — ${state.uf}` : ''}.`
          : outMessage,
        state.ok ? 'ok' : 'err',
        state.uf
      );
    }
    setCheckoutLock(!state?.ok, 'Informe um CEP de entrega no Brasil para continuar.');
    input.addEventListener('input', () => {
      input.value = formatCep(input.value);
      if (digits(input.value) !== digits(readState()?.cep)) {
        writeState(null);
        setCheckoutLock(true, 'Verifique o novo CEP para continuar.');
        showMessage(gate, '', '');
      }
    });
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      if (digits(input.value).length !== 8) {
        showMessage(gate, 'Informe um CEP válido com 8 dígitos.', 'err');
        setCheckoutLock(true);
        return;
      }
      button?.setAttribute('aria-busy', 'true');
      if (button) button.disabled = true;
      try {
        const result = await validateCep(input.value);
        showMessage(gate, result.message, result.ok ? 'ok' : 'err', result.state && result.state.uf);
        setCheckoutLock(!result.ok, result.message);
      } catch (_) {
        showMessage(gate, 'Não foi possível validar este CEP. Tente novamente.', 'err');
        setCheckoutLock(true);
      } finally {
        button?.removeAttribute('aria-busy');
        if (button) button.disabled = false;
      }
    });
  };
  function ensureGates() {
    document.querySelectorAll('[data-purchase-conditions]').forEach((host) => {
      let gate = host.querySelector('[data-saibai-delivery-gate]');
      if (!gate) {
        gate = createGate();
        const ctas = host.querySelector('.cart__ctas');
        host.insertBefore(gate, ctas || host.firstChild);
      }
      bindGate(gate);
    });
    setCheckoutLock(!checkoutAllowed(), 'Informe um CEP de entrega no Brasil para continuar.');
  }
  document.addEventListener('click', (event) => {
    const target = event.target instanceof Element
      ? event.target.closest('button[name="checkout"], .cart__checkout-button, a[href*="/checkout"]')
      : null;
    if (!target || checkoutAllowed()) return;
    event.preventDefault();
    event.stopPropagation();
    focusGate();
  }, true);
  document.addEventListener('submit', (event) => {
    const form = event.target;
    const checkout = event.submitter?.name === 'checkout' ||
      form?.querySelector?.('button[name="checkout"]');
    if (!checkout || checkoutAllowed()) return;
    event.preventDefault();
    event.stopPropagation();
    focusGate();
  }, true);
  window.SaibaiDelivery = {
    formatCep,
    onlyDigits: digits,
    normalize,
    isEligibleAddress: eligible,
    validateCep,
    fetchCep,
    rememberFromAddress: remember,
    isCheckoutAllowed: checkoutAllowed,
    getState: readState,
    messageOut: outMessage,
    transitMessage,
    isOutsideSp,
    brasilUfs: allowedStates.slice(),
    sudesteUfs: allowedStates.slice(),
    refresh: ensureGates,
  };
  let refreshTimer;
  const scheduleRefresh = () => {
    clearTimeout(refreshTimer);
    refreshTimer = setTimeout(ensureGates, 80);
  };
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', ensureGates, { once: true });
  } else {
    ensureGates();
  }
  document.addEventListener('shopify:section:load', scheduleRefresh);
  document.addEventListener('cart:updated', scheduleRefresh);
  document.addEventListener('cart-drawer:open', scheduleRefresh);
  new MutationObserver((mutations) => {
    if (mutations.some((mutation) => mutation.addedNodes.length)) scheduleRefresh();
  }).observe(document.documentElement, { childList: true, subtree: true });
})();
