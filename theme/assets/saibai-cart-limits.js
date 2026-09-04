/**
 * Empório Saibai — limite de caixas de alcachofra por pedido.
 * Teto agregado: product_type "Alcachofra In Natura" (handles alcachofra-in-natura-*).
 * Intercepta /cart/add|change|update (JSON + FormData).
 */
(function () {
  'use strict';

  if (window.__saibaiCartLimitsInit) return;
  window.__saibaiCartLimitsInit = true;

  var cfg = window.saibaiCartLimits || {};
  var MAX = parseInt(cfg.max, 10);
  if (!MAX || MAX < 1) MAX = 2;
  var TYPE = String(cfg.productType || 'Alcachofra In Natura').toLowerCase();
  var PREFIX = String(cfg.handlePrefix || 'alcachofra-in-natura');
  var MSG =
    cfg.message ||
    'Limite de 2 caixas de alcachofra fresca por pedido. Para pedidos maiores, fale conosco no WhatsApp.';
  var variantSet = {};
  var ids = cfg.variantIds || [];
  var i;
  for (i = 0; i < ids.length; i++) {
    variantSet[String(ids[i])] = true;
  }

  function isBoxItem(item) {
    if (!item) return false;
    var id = String(item.id || item.variant_id || '');
    if (id && variantSet[id]) return true;
    var type = String(item.product_type || item.productType || '').toLowerCase();
    if (type === TYPE) return true;
    var handle = String(item.handle || '');
    return handle.indexOf(PREFIX) === 0;
  }

  function isBoxVariantId(id) {
    return !!variantSet[String(id)];
  }

  function countBoxes(items) {
    var n = 0;
    var j;
    for (j = 0; j < items.length; j++) {
      if (isBoxItem(items[j])) n += parseInt(items[j].quantity, 10) || 0;
    }
    return n;
  }

  function cloneItems(items) {
    var out = [];
    var j;
    for (j = 0; j < items.length; j++) {
      out.push({
        id: items[j].id,
        key: items[j].key,
        quantity: items[j].quantity,
        handle: items[j].handle,
        product_type: items[j].product_type,
      });
    }
    return out;
  }

  function getCart() {
    return fetch('/cart.js', { credentials: 'same-origin' }).then(function (r) {
      return r.json();
    });
  }

  function rejectResponse() {
    return Promise.resolve(
      new Response(
        JSON.stringify({
          status: 422,
          message: MSG,
          description: MSG,
          errors: MSG,
        }),
        {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        }
      )
    );
  }

  function parseJsonBody(body) {
    if (typeof body !== 'string') return null;
    try {
      return JSON.parse(body);
    } catch (e) {
      return null;
    }
  }

  function parseFormDataBody(body) {
    if (typeof FormData === 'undefined' || !(body instanceof FormData)) return null;
    var id = body.get('id');
    var qty = parseInt(body.get('quantity') || '1', 10);
    if (!id) return null;
    return { id: id, quantity: isNaN(qty) ? 1 : qty };
  }

  function extractAdds(payload) {
    if (!payload) return [];
    if (payload.items && payload.items.length) {
      return payload.items.map(function (it) {
        return {
          id: it.id,
          quantity: parseInt(it.quantity, 10) || 1,
        };
      });
    }
    if (payload.id) {
      return [{ id: payload.id, quantity: parseInt(payload.quantity, 10) || 1 }];
    }
    return [];
  }

  function projectAfterAdd(cartItems, adds) {
    var projected = cloneItems(cartItems);
    var a;
    for (a = 0; a < adds.length; a++) {
      var addId = String(adds[a].id);
      var addQty = adds[a].quantity;
      var found = false;
      var j;
      for (j = 0; j < projected.length; j++) {
        if (String(projected[j].id) === addId) {
          projected[j].quantity += addQty;
          found = true;
          break;
        }
      }
      if (!found && isBoxVariantId(addId)) {
        projected.push({
          id: addId,
          quantity: addQty,
          handle: PREFIX,
          product_type: cfg.productType || 'Alcachofra In Natura',
        });
      } else if (!found) {
        projected.push({
          id: addId,
          quantity: addQty,
          handle: '',
          product_type: '',
        });
      }
    }
    return projected;
  }

  function projectAfterChange(cartItems, payload) {
    var projected = cloneItems(cartItems);
    if (!payload) return projected;
    var qty = parseInt(payload.quantity, 10);
    if (isNaN(qty)) return projected;
    var j;
    if (payload.line != null) {
      var lineIdx = parseInt(payload.line, 10) - 1;
      if (lineIdx >= 0 && lineIdx < projected.length) {
        projected[lineIdx].quantity = qty;
      }
      return projected;
    }
    if (payload.id != null) {
      var keyOrId = String(payload.id);
      for (j = 0; j < projected.length; j++) {
        if (String(projected[j].key) === keyOrId || String(projected[j].id) === keyOrId) {
          projected[j].quantity = qty;
          break;
        }
      }
    }
    return projected;
  }

  function projectAfterUpdate(cartItems, payload) {
    var projected = cloneItems(cartItems);
    if (!payload || !payload.updates) return projected;
    var updates = payload.updates;
    var key;
    for (key in updates) {
      if (!Object.prototype.hasOwnProperty.call(updates, key)) continue;
      var qty = parseInt(updates[key], 10);
      if (isNaN(qty)) continue;
      var j;
      for (j = 0; j < projected.length; j++) {
        if (String(projected[j].id) === String(key) || String(projected[j].key) === String(key)) {
          projected[j].quantity = qty;
          break;
        }
      }
    }
    return projected;
  }

  function wouldExceed(projected) {
    return countBoxes(projected) > MAX;
  }

  function cartUrlKind(url) {
    if (!url) return null;
    if (url.indexOf('/cart/add') !== -1) return 'add';
    if (url.indexOf('/cart/change') !== -1) return 'change';
    if (url.indexOf('/cart/update') !== -1) return 'update';
    return null;
  }

  var originalFetch = window.fetch;
  window.fetch = function (input, init) {
    var url = typeof input === 'string' ? input : (input && input.url) || '';
    var kind = cartUrlKind(url);
    if (!kind) {
      return originalFetch.apply(this, arguments);
    }

    var args = arguments;
    var body = init && init.body;
    var payload = parseJsonBody(typeof body === 'string' ? body : null);
    if (!payload) payload = parseFormDataBody(body);

    return getCart()
      .then(function (cart) {
        var items = cart.items || [];
        var projected = items;

        if (kind === 'add') {
          var adds = extractAdds(payload);
          var onlyNonBox = true;
          var a;
          for (a = 0; a < adds.length; a++) {
            if (isBoxVariantId(adds[a].id)) {
              onlyNonBox = false;
              break;
            }
          }
          if (onlyNonBox && adds.length) {
            return originalFetch.apply(window, args);
          }
          projected = projectAfterAdd(items, adds);
        } else if (kind === 'change') {
          projected = projectAfterChange(items, payload);
        } else if (kind === 'update') {
          projected = projectAfterUpdate(items, payload);
        }

        if (wouldExceed(projected)) {
          return rejectResponse();
        }
        return originalFetch.apply(window, args);
      })
      .catch(function () {
        return originalFetch.apply(window, args);
      });
  };
})();
