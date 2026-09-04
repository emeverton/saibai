import type { TrackingDestination } from '../types';
import { Ga4Destination } from './ga4';
import { GoogleAdsDestination } from './google-ads';
import { KlaviyoDestination } from './klaviyo';
import { MetaDestination } from './meta';
import { TikTokDestination } from './tiktok';

let registry: TrackingDestination[] | null = null;

export function getDestinations(): TrackingDestination[] {
  if (!registry) {
    registry = [
      new MetaDestination(),
      new Ga4Destination(),
      new GoogleAdsDestination(),
      new TikTokDestination(),
      new KlaviyoDestination(),
    ];
  }
  return registry;
}

export { Ga4Destination, GoogleAdsDestination, KlaviyoDestination, MetaDestination, TikTokDestination };
