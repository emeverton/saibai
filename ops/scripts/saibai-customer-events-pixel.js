/**
 * Empório Saibai — Custom Pixel (Customer Events)
 * Cole em: Admin → Configurações → Eventos do cliente → Adicionar pixel personalizado
 * Nome sugerido: Saibai Veltrus Checkout Events
 * Permissões: Análise + Marketing
 *
 * Estratégia anti-duplicata:
 * - Storefront: GA4/Meta via canais Shopify (Google & YouTube, Facebook & Instagram)
 * - Checkout: este pixel envia begin_checkout, purchase, add_to_cart
 * - NÃO dispara PageView (evita duplicar tags dos canais)
 * - Stape: somente server-side/CAPI no container — sem tags browser duplicadas
 *
 * IDs injetados por scripts/configure-saibai-customer-events-pixel.py
 */
var SAIBAI_GA4_ID = '{{GA4_MEASUREMENT_ID}}';
var SAIBAI_META_ID = '{{META_PIXEL_ID}}';

(function () {
  if (!SAIBAI_GA4_ID && !SAIBAI_META_ID) return;

  var gaReady = false;
  var metaReady = false;

  window.dataLayer = window.dataLayer || [];
  function gtag() {
    window.dataLayer.push(arguments);
  }

  function ensureGa4(callback) {
    if (!SAIBAI_GA4_ID || gaReady) {
      if (callback) callback();
      return;
    }
    gaReady = true;
    var gaScript = document.createElement('script');
    gaScript.async = true;
    gaScript.src = 'https://www.googletagmanager.com/gtag/js?id=' + SAIBAI_GA4_ID;
    gaScript.onload = function () {
      gtag('js', new Date());
      gtag('config', SAIBAI_GA4_ID, { send_page_view: false });
      if (callback) callback();
    };
    document.head.appendChild(gaScript);
  }

  function ensureMeta(callback) {
    if (!SAIBAI_META_ID || metaReady) {
      if (callback) callback();
      return;
    }
    metaReady = true;
    !(function (f, b, e, v, n, t, s) {
      if (f.fbq) {
        if (callback) callback();
        return;
      }
      n = f.fbq = function () {
        n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
      };
      if (!f._fbq) f._fbq = n;
      n.push = n;
      n.loaded = true;
      n.version = '2.0';
      n.queue = [];
      t = b.createElement(e);
      t.async = true;
      t.src = v;
      t.onload = function () {
        fbq('init', SAIBAI_META_ID);
        if (callback) callback();
      };
      s = b.getElementsByTagName(e)[0];
      s.parentNode.insertBefore(t, s);
    })(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
  }

  function checkoutItems(checkout) {
    var items = checkout && checkout.lineItems ? checkout.lineItems : [];
    return items.map(function (line) {
      var variant = line.variant || {};
      return {
        item_id: String(variant.sku || variant.id || line.id || ''),
        item_name: line.title || '',
        price: line.finalLinePrice && line.finalLinePrice.amount ? Number(line.finalLinePrice.amount) : undefined,
        quantity: line.quantity || 1
      };
    });
  }

  function checkoutValue(checkout) {
    return checkout && checkout.totalPrice && checkout.totalPrice.amount
      ? Number(checkout.totalPrice.amount)
      : 0;
  }

  function checkoutCurrency(checkout) {
    return (checkout && checkout.currencyCode) || 'BRL';
  }

  function transactionId(checkout) {
    if (!checkout) return '';
    if (checkout.order && checkout.order.id) return String(checkout.order.id);
    if (checkout.token) return String(checkout.token);
    return '';
  }

  analytics.subscribe('checkout_started', function (event) {
    var checkout = event.data && event.data.checkout;
    if (!checkout) return;
    var payload = {
      currency: checkoutCurrency(checkout),
      value: checkoutValue(checkout),
      items: checkoutItems(checkout)
    };
    ensureGa4(function () {
      if (SAIBAI_GA4_ID) gtag('event', 'begin_checkout', payload);
    });
    ensureMeta(function () {
      if (SAIBAI_META_ID) fbq('track', 'InitiateCheckout', { value: payload.value, currency: payload.currency });
    });
  });

  analytics.subscribe('checkout_completed', function (event) {
    var checkout = event.data && event.data.checkout;
    if (!checkout) return;

    var txId = transactionId(checkout);
    var value = checkoutValue(checkout);
    var currency = checkoutCurrency(checkout);
    var items = checkoutItems(checkout);
    var tax = checkout.totalTax && checkout.totalTax.amount ? Number(checkout.totalTax.amount) : 0;
    var shipping =
      checkout.shippingLine && checkout.shippingLine.price && checkout.shippingLine.price.amount
        ? Number(checkout.shippingLine.price.amount)
        : 0;

    ensureGa4(function () {
      if (SAIBAI_GA4_ID) {
        gtag('event', 'purchase', {
          transaction_id: txId,
          value: value,
          currency: currency,
          tax: tax,
          shipping: shipping,
          items: items
        });
      }
    });

    ensureMeta(function () {
      if (SAIBAI_META_ID) {
        fbq('track', 'Purchase', {
          value: value,
          currency: currency,
          content_type: 'product',
          contents: items.map(function (item) {
            return { id: item.item_id, quantity: item.quantity };
          })
        });
      }
    });
  });

  analytics.subscribe('product_added_to_cart', function (event) {
    var cartLine = event.data && event.data.cartLine;
    if (!cartLine) return;
    var merchandise = cartLine.merchandise || {};
    var product = merchandise.product || {};
    var value =
      cartLine.cost && cartLine.cost.totalAmount && cartLine.cost.totalAmount.amount
        ? Number(cartLine.cost.totalAmount.amount)
        : undefined;
    var currency =
      cartLine.cost && cartLine.cost.totalAmount && cartLine.cost.totalAmount.currencyCode
        ? cartLine.cost.totalAmount.currencyCode
        : 'BRL';

    ensureGa4(function () {
      if (SAIBAI_GA4_ID) {
        gtag('event', 'add_to_cart', {
          currency: currency,
          value: value,
          items: [
            {
              item_id: String(merchandise.sku || merchandise.id || product.id || ''),
              item_name: product.title || merchandise.title || '',
              quantity: cartLine.quantity || 1
            }
          ]
        });
      }
    });

    ensureMeta(function () {
      if (SAIBAI_META_ID) {
        fbq('track', 'AddToCart', {
          content_name: product.title || merchandise.title || '',
          content_ids: [String(merchandise.id || product.id || '')],
          content_type: 'product',
          value: value,
          currency: currency
        });
      }
    });
  });
})();
