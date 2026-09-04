(function () {
  'use strict';

  var ROOT = '[data-saibai-pdp-ship]';
  var BR_COUNTRY = 'Brazil';

  var UF_NAMES = {
    AC: 'Acre', AL: 'Alagoas', AP: 'Amapá', AM: 'Amazonas', BA: 'Bahia',
    CE: 'Ceará', DF: 'Distrito Federal', ES: 'Espírito Santo', GO: 'Goiás',
    MA: 'Maranhão', MT: 'Mato Grosso', MS: 'Mato Grosso do Sul', MG: 'Minas Gerais',
    PA: 'Pará', PB: 'Paraíba', PR: 'Paraná', PE: 'Pernambuco', PI: 'Piauí',
    RJ: 'Rio de Janeiro', RN: 'Rio Grande do Norte', RS: 'Rio Grande do Sul',
    RO: 'Rondônia', RR: 'Roraima', SC: 'Santa Catarina', SP: 'São Paulo',
    SE: 'Sergipe', TO: 'Tocantins'
  };

  function onlyDigits(value) {
    return (value || '').replace(/\D/g, '');
  }

  function formatCep(value) {
    var d = onlyDigits(value).slice(0, 8);
    if (d.length <= 5) return d;
    return d.slice(0, 5) + '-' + d.slice(5);
  }

  function getProductForm(root) {
    var section = root.closest('.shopify-section') || root.closest('product-info');
    if (!section) section = document;
    return section.querySelector('product-form-component form') || section.querySelector('form[action*="/cart/add"]');
  }

  function getVariantId(root) {
    var form = getProductForm(root);
    var input = form && form.querySelector('input[name="id"]');
    if (input && input.value) return parseInt(input.value, 10);
    var attr = root.getAttribute('data-variant-id');
    return attr ? parseInt(attr, 10) : 0;
  }

  function getQuantity(root) {
    var form = getProductForm(root);
    var qty = form && form.querySelector('input[name="quantity"]');
    var val = qty ? parseInt(qty.value, 10) : 1;
    return isNaN(val) || val < 1 ? 1 : val;
  }

  function fetchCep(cep) {
    return fetch('https://viacep.com.br/ws/' + cep + '/json/')
      .then(function (res) { return res.json(); })
      .then(function (data) {
        if (!data || data.erro) throw new Error('CEP inválido');
        return data;
      });
  }

  function ensureCartLine(variantId, quantity) {
    return fetch(window.routes.cart_url + '.js', { credentials: 'same-origin' })
      .then(function (res) { return res.json(); })
      .then(function (cart) {
        var hasVariant = false;
        var i;
        for (i = 0; i < cart.items.length; i++) {
          if (cart.items[i].variant_id === variantId) {
            hasVariant = true;
            break;
          }
        }
        if (hasVariant) return cart;
        return fetch(window.routes.cart_add_url + '.js', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          credentials: 'same-origin',
          body: JSON.stringify({ items: [{ id: variantId, quantity: quantity }] })
        }).then(function (res) { return res.json(); });
      });
  }

  function fetchShippingRates(zip, province) {
    var url = (window.routes.cart_url + '/shipping_rates.json').replace(/\/\//g, '/');
    return fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      credentials: 'same-origin',
      body: JSON.stringify({
        shipping_address: {
          zip: zip,
          country: BR_COUNTRY,
          province: province
        }
      })
    }).then(function (res) { return res.json(); });
  }

  function tryRates(zip, uf) {
    var attempts = [uf, UF_NAMES[uf] || uf];
    var index = 0;

    function next() {
      if (index >= attempts.length) {
        return Promise.reject(new Error('not_found'));
      }
      var province = attempts[index];
      index += 1;
      return fetchShippingRates(zip, province).then(function (data) {
        if (data.shipping_rates && data.shipping_rates.length) return data.shipping_rates;
        if (data.zip && index < attempts.length) return next();
        if (data.shipping_rates) return data.shipping_rates;
        return next();
      });
    }

    return next();
  }

  function formatMoney(price, currency) {
    var formatted;
    if (window.Shopify && typeof window.Shopify.formatMoney === 'function') {
      formatted = Shopify.formatMoney(Math.round(parseFloat(price) * 100), window.money_format);
    } else {
      formatted = (currency || 'R$') + ' ' + price;
    }
    return String(formatted).replace(/r\$/g, 'R$');
  }

  function transitNote(uf) {
    var msg =
      (window.SaibaiDelivery && window.SaibaiDelivery.transitMessage) ||
      'Fora de São Paulo, o produto pode sofrer algumas alterações devido ao tempo de entrega.';
    var outside =
      window.SaibaiDelivery && typeof window.SaibaiDelivery.isOutsideSp === 'function'
        ? window.SaibaiDelivery.isOutsideSp(uf)
        : String(uf || '').toUpperCase() !== 'SP';
    if (!uf || !outside) return '';
    return '<p class="saibai-pdp-ship__transit">' + msg + '</p>';
  }

  function renderResults(el, rates, error, uf) {
    el.hidden = false;
    if (error) {
      el.className = 'saibai-pdp-ship__results saibai-pdp-ship__results--error';
      el.innerHTML = '<p>' + error + '</p>' + transitNote(uf);
      return;
    }
    if (!rates || !rates.length) {
      el.className = 'saibai-pdp-ship__results saibai-pdp-ship__results--empty';
      el.innerHTML = '<p>Não encontramos frete para este CEP. Entregamos em todo o Brasil — confira o CEP ou tente novamente no checkout. <a href="/pages/politica-de-entrega">Ver política de entrega</a></p>' + transitNote(uf);
      return;
    }
    el.className = 'saibai-pdp-ship__results saibai-pdp-ship__results--ok';
    var html = '<ul class="saibai-pdp-ship__list" role="list">';
    var i;
    for (i = 0; i < rates.length; i++) {
      var rate = rates[i];
      html += '<li class="saibai-pdp-ship__rate">';
      html += '<span class="saibai-pdp-ship__rate-name">' + rate.presentment_name + '</span>';
      html += '<span class="saibai-pdp-ship__rate-price">' + formatMoney(rate.price, rate.currency) + '</span>';
      html += '</li>';
    }
    html += '</ul>';
    html += transitNote(uf);
    el.innerHTML = html;
  }

  function getVariantPriceCents(root) {
    var section = root.closest('.shopify-section') || root.closest('product-info') || document;
    var priceEl = section.querySelector('.price-item--last, .price-item--sale, [data-product-price]');
    if (!priceEl) return 0;
    var text = (priceEl.textContent || '').replace(/\s/g, '');
    var match = text.match(/[\d.,]+/);
    if (!match) return 0;
    var normalized = match[0].replace(/\./g, '').replace(',', '.');
    var value = parseFloat(normalized);
    if (isNaN(value)) return 0;
    return Math.round(value * 100);
  }

  function updateFreeShipStatus(root) {
    var threshold = parseInt(root.getAttribute('data-free-ship-threshold') || '0', 10);
    var remainingEl = root.querySelector('[data-saibai-pdp-ship-remaining]');
    var statusOk = root.querySelector('.saibai-pdp-ship__free-status--ok');
    var statusPending = root.querySelector('.saibai-pdp-ship__free-status--pending');
    if (!threshold) return;

    var priceCents = getVariantPriceCents(root);
    var remaining = threshold - priceCents;

    if (remaining <= 0) {
      if (statusPending) statusPending.hidden = true;
      if (statusOk) statusOk.hidden = false;
      return;
    }

    if (statusOk) statusOk.hidden = true;
    if (statusPending) {
      statusPending.hidden = false;
      if (remainingEl) {
        remainingEl.textContent = formatMoney(remaining / 100, 'R$');
      }
    }
  }

  function bindRoot(root) {
    if (root.dataset.saibaiShipBound === 'true') return;
    root.dataset.saibaiShipBound = 'true';

    var form = root.querySelector('[data-saibai-pdp-ship-form]');
    var cepInput = root.querySelector('[data-saibai-pdp-ship-cep]');
    var submitBtn = root.querySelector('[data-saibai-pdp-ship-submit]');
    var results = root.querySelector('[data-saibai-pdp-ship-results]');
    if (!form || !cepInput || !results) return;

    cepInput.addEventListener('input', function () {
      cepInput.value = formatCep(cepInput.value);
    });

    var productForm = getProductForm(root);
    if (productForm) {
      var variantInput = productForm.querySelector('input[name="id"]');
      if (variantInput) {
        variantInput.addEventListener('change', function () {
          root.setAttribute('data-variant-id', variantInput.value);
          updateFreeShipStatus(root);
        });
      }
    }

    updateFreeShipStatus(root);

    if (typeof MainEvents !== 'undefined' && MainEvents.variantUpdate) {
      document.addEventListener(MainEvents.variantUpdate, function () {
        updateFreeShipStatus(root);
      });
    }

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      var cep = onlyDigits(cepInput.value);
      if (cep.length !== 8) {
        renderResults(results, null, 'Informe um CEP válido com 8 dígitos.');
        return;
      }

      var variantId = getVariantId(root);
      if (!variantId) {
        renderResults(results, null, 'Selecione uma opção do produto para calcular o frete.');
        return;
      }

      submitBtn.disabled = true;
      submitBtn.setAttribute('aria-busy', 'true');
      results.hidden = true;

      fetchCep(cep)
        .then(function (address) {
          if (window.SaibaiDelivery && typeof window.SaibaiDelivery.isEligibleAddress === 'function') {
            if (!window.SaibaiDelivery.isEligibleAddress(address)) {
              if (typeof window.SaibaiDelivery.rememberFromAddress === 'function') {
                window.SaibaiDelivery.rememberFromAddress(address, false);
              }
              throw {
                type: 'zone',
                uf: address.uf,
                message: window.SaibaiDelivery.messageOut || 'CEP fora da área de entrega.'
              };
            }
            if (typeof window.SaibaiDelivery.rememberFromAddress === 'function') {
              window.SaibaiDelivery.rememberFromAddress(address, true);
            }
          }
          return ensureCartLine(variantId, getQuantity(root)).then(function () {
            return tryRates(formatCep(cep), address.uf).then(
              function (rates) {
                return { rates: rates, uf: address.uf };
              },
              function () {
                return { rates: [], uf: address.uf };
              }
            );
          });
        })
        .then(function (payload) {
          renderResults(results, payload.rates, null, payload.uf);
        })
        .catch(function (err) {
          if (err && err.type === 'zone') {
            renderResults(results, null, err.message, err.uf);
            return;
          }
          renderResults(results, null, 'Não foi possível calcular o frete. Verifique o CEP ou tente novamente.');
        })
        .finally(function () {
          submitBtn.disabled = false;
          submitBtn.removeAttribute('aria-busy');
        });
    });
  }

  function init() {
    var nodes = document.querySelectorAll(ROOT);
    var i;
    for (i = 0; i < nodes.length; i++) {
      bindRoot(nodes[i]);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  document.addEventListener('shopify:section:load', init);
})();

(function () {
  'use strict';

  function hasJudgeMeReviews(widget) {
    if (!widget) return false;
    return !!(
      widget.querySelector('.jdgm-rev')
      || widget.querySelector('.jdgm-rev-widg__reviews .jdgm-rev')
    );
  }

  function updateReviewsTabState() {
    var widgetRoot = document.querySelector('[data-saibai-pdp-reviews-widget]');
    if (!widgetRoot) return;

    var widget = widgetRoot.querySelector('.jdgm-review-widget');
    var hasReviews = hasJudgeMeReviews(widget);
    var reviewsTab = document.getElementById('saibai-tab-avaliacoes');
    var reviewsSummary = document.querySelector('[data-saibai-pdp-reviews-summary]');

    widgetRoot.classList.toggle('saibai-pdp-reviews-widget--has-reviews', hasReviews);
    widgetRoot.classList.toggle('saibai-pdp-reviews-widget--empty', !hasReviews);

    if (reviewsTab) {
      if (hasReviews) {
        reviewsTab.removeAttribute('hidden');
      } else {
        reviewsTab.setAttribute('hidden', '');
      }
    }

    if (reviewsSummary) {
      if (hasReviews) {
        reviewsSummary.removeAttribute('hidden');
      } else {
        reviewsSummary.setAttribute('hidden', '');
      }
    }
  }

  function initReviewsTab() {
    updateReviewsTabState();
    window.setTimeout(updateReviewsTabState, 800);
    window.setTimeout(updateReviewsTabState, 2500);
    window.setTimeout(updateReviewsTabState, 5000);

    var widgetRoot = document.querySelector('[data-saibai-pdp-reviews-widget]');
    if (widgetRoot && typeof MutationObserver === 'function') {
      var observer = new MutationObserver(updateReviewsTabState);
      observer.observe(widgetRoot, { childList: true, subtree: true });
      window.setTimeout(function () {
        observer.disconnect();
      }, 12000);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initReviewsTab);
  } else {
    initReviewsTab();
  }

  document.addEventListener('shopify:section:load', initReviewsTab);
})();
