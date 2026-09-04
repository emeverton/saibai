import type { DestinationResult, NormalizedTrackingEvent, TrackingDestination } from '../types';

export class TikTokDestination implements TrackingDestination {
  name = 'tiktok';

  async send(_event: NormalizedTrackingEvent): Promise<DestinationResult> {
    return {
      destination: this.name,
      status: 'skipped',
      error: 'TikTok Events API placeholder',
    };
  }
}
