import type { DestinationResult, NormalizedTrackingEvent, TrackingDestination } from '../types';

/**
 * Placeholder for Google Ads Enhanced Conversions via offline/upload API.
 * Requires OAuth + conversion action configuration.
 */
export class GoogleAdsDestination implements TrackingDestination {
  name = 'google_ads';

  async send(event: NormalizedTrackingEvent): Promise<DestinationResult> {
    const customerId = process.env.GOOGLE_ADS_CUSTOMER_ID;
    const conversionActionId = process.env.GOOGLE_ADS_CONVERSION_ACTION_ID;

    if (!customerId || !conversionActionId) {
      return {
        destination: this.name,
        status: 'skipped',
        error: 'Google Ads env vars not configured',
      };
    }

    if (event.eventName !== 'purchase' && event.eventName !== 'begin_checkout') {
      return {
        destination: this.name,
        status: 'skipped',
        error: 'Event not eligible for Google Ads conversion',
      };
    }

    return {
      destination: this.name,
      status: 'skipped',
      error: 'Google Ads Enhanced Conversions module pending OAuth implementation',
    };
  }
}
