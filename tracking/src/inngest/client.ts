import { Inngest } from 'inngest';

export const inngest = new Inngest({
  id: 'saibai-tracking',
  eventKey: process.env.INNGEST_EVENT_KEY,
});
