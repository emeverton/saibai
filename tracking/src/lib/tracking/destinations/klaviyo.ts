import type { DestinationResult, NormalizedTrackingEvent, TrackingDestination } from '../types';

export class KlaviyoDestination implements TrackingDestination {
  name = 'klaviyo';

  async send(_event: NormalizedTrackingEvent): Promise<DestinationResult> {
    return {
      destination: this.name,
      status: 'skipped',
      error: 'Klaviyo Events API placeholder',
    };
  }
}
