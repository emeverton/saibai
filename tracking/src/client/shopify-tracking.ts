/**
 * Shopify storefront client — Customer Events + first-party IDs + server ingest.
 * Bundle/copy to theme assets or load via theme.liquid after consent.
 */

const COOKIE_VISITOR = 'vlt_visitor_id';
const COOKIE_SESSION = 'vlt_session_id';
const ATTR_KEYS = [
  'utm_source',
  'utm_medium',
  'utm_campaign',
  'utm_content',
  'utm_term',
  'gclid',
  'fbclid',
  'ttclid',
  'msclkid',
] as const;

export interface ShopifyTrackingClientConfig {
  endpoint: string;
  secret: string;
  shopId?: string;
  debug?: boolean;
}

function readCookie(name: string): string | undefined {
  const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`));
  return match ? decodeURIComponent(match[1]) : undefined;
}

function writeCookie(name: string, value: string, days: number) {
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/; SameSite=Lax`;
}

function ensureIds() {
  let visitorId = readCookie(COOKIE_VISITOR);
  if (!visitorId) {
    visitorId = crypto.randomUUID();
    writeCookie(COOKIE_VISITOR, visitorId, 365);
  }

  let sessionId = readCookie(COOKIE_SESSION);
  if (!sessionId) {
    sessionId = crypto.randomUUID();
    writeCookie(COOKIE_SESSION, sessionId, 1);
  }

  return { visitorId, sessionId };
}

function captureAttribution() {
  const params = new URLSearchParams(window.location.search);
  const data: Record<string, string> = {};

  for (const key of ATTR_KEYS) {
    const value = params.get(key);
    if (value) {
      data[key] = value;
      try {
        localStorage.setItem(`vlt_${key}`, value);
      } catch {
        /* ignore */
      }
    } else {
      try {
        const stored = localStorage.getItem(`vlt_${key}`);
        if (stored) data[key] = stored;
      } catch {
        /* ignore */
      }
    }
  }

  return data;
}

export function createShopifyTrackingClient(config: ShopifyTrackingClientConfig) {
  const { visitorId, sessionId } = ensureIds();
  const attribution = captureAttribution();

  async function track(
    eventName: string,
    payload: Record<string, unknown> = {},
  ) {
    const body = {
      event_id: crypto.randomUUID(),
      event_name: eventName,
      event_time: Math.floor(Date.now() / 1000),
      source: 'shopify',
      shopify_shop_id: config.shopId,
      visitor_id: visitorId,
      session_id: sessionId,
      page_url: window.location.href,
      referrer: document.referrer || undefined,
      landing_page: attribution.landing_page ?? window.location.href,
      user_agent: navigator.userAgent,
      ...attribution,
      ...payload,
    };

    if (config.debug) console.info('[vlt-tracking]', body);

    const response = await fetch(config.endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-tracking-secret': config.secret,
      },
      body: JSON.stringify(body),
      keepalive: true,
    });

    return response.json();
  }

  function bindShopifyAnalytics() {
    if (!window.Shopify?.analytics) return;

    const publish = window.Shopify.analytics.publish?.bind(window.Shopify.analytics);
    if (!publish) return;

    const map: Record<string, string> = {
      page_viewed: 'page_view',
      product_viewed: 'product_view',
      collection_viewed: 'collection_view',
      search_submitted: 'search',
      product_added_to_cart: 'add_to_cart',
      product_removed_from_cart: 'remove_from_cart',
      checkout_started: 'begin_checkout',
      checkout_shipping_info_submitted: 'add_shipping_info',
      payment_info_submitted: 'add_payment_info',
      checkout_completed: 'purchase',
    };

    document.addEventListener('shopify:analytics:publish', (event: Event) => {
      const detail = (event as CustomEvent).detail;
      const mapped = map[detail?.name];
      if (!mapped) return;

      void track(mapped, {
        properties: detail?.payload ?? {},
        product_id: detail?.payload?.productVariant?.product?.id,
        variant_id: detail?.payload?.productVariant?.id,
        value: detail?.payload?.checkout?.totalPrice?.amount,
        currency: detail?.payload?.checkout?.totalPrice?.currencyCode,
        order_id: detail?.payload?.checkout?.order?.id,
        checkout_id: detail?.payload?.checkout?.token,
        items: detail?.payload?.cartLine?.merchandise
          ? [
              {
                product_id: detail.payload.cartLine.merchandise.product?.id,
                variant_id: detail.payload.cartLine.merchandise.id,
                quantity: detail.payload.cartLine.quantity,
              },
            ]
          : undefined,
      });
    });
  }

  function bindCustomEvents() {
    document.addEventListener('click', (event) => {
      const target = event.target as HTMLElement | null;
      if (!target) return;

      const wa = target.closest('[data-saibai-track="whatsapp"], a[href*="wa.me"], a[href*="whatsapp.com"]');
      if (wa) void track('whatsapp_click', { properties: { href: (wa as HTMLAnchorElement).href } });

      const phone = target.closest('[data-saibai-track="phone"], a[href^="tel:"]');
      if (phone) void track('phone_click', { properties: { href: (phone as HTMLAnchorElement).href } });

      const email = target.closest('[data-saibai-track="email"], a[href^="mailto:"]');
      if (email) void track('email_click', { properties: { href: (email as HTMLAnchorElement).href } });

      const cta = target.closest('[data-saibai-track="cta"]');
      if (cta) void track('cta_click', { properties: { label: cta.textContent?.trim() } });
    });

    const depths = new Set<number>();
    window.addEventListener(
      'scroll',
      () => {
        const max = document.documentElement.scrollHeight - window.innerHeight;
        if (max <= 0) return;
        const pct = Math.round((window.scrollY / max) * 100);
        for (const mark of [25, 50, 75, 90]) {
          if (pct >= mark && !depths.has(mark)) {
            depths.add(mark);
            void track('scroll_depth', { properties: { depth: mark } });
          }
        }
      },
      { passive: true },
    );
  }

  function init() {
    bindShopifyAnalytics();
    bindCustomEvents();
    void track('page_view');
  }

  return { track, init, visitorId, sessionId };
}

declare global {
  interface Window {
    Shopify?: {
      analytics?: {
        publish?: (name: string, payload?: Record<string, unknown>) => void;
      };
    };
  }
}
