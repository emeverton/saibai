export async function sendSlackAlert(message: string, details?: Record<string, unknown>) {
  const webhook = process.env.SLACK_WEBHOOK_URL;
  if (!webhook) return;

  await fetch(webhook, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text: message,
      blocks: details
        ? [
            { type: 'section', text: { type: 'mrkdwn', text: message } },
            {
              type: 'section',
              text: {
                type: 'mrkdwn',
                text: '```' + JSON.stringify(details, null, 2).slice(0, 2800) + '```',
              },
            },
          ]
        : undefined,
    }),
  });
}

export async function sendN8nAlert(payload: Record<string, unknown>) {
  const webhook = process.env.N8N_ALERT_WEBHOOK_URL;
  if (!webhook) return;

  await fetch(webhook, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
}
