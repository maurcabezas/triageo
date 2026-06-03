# Webhook Setup and Troubleshooting

This guide helps customers configure webhooks and diagnose common delivery problems.

## Setting up a webhook

1. Go to Settings > Developer > Webhooks.
2. Click "Add endpoint" and enter the HTTPS URL.
3. Select the events to subscribe to.
4. Save and copy the webhook signing secret.

## Verifying webhook payloads

All webhook payloads include an `X-Signature-256` header. Customers should verify this signature using the signing secret to prevent spoofed events.

## Common delivery failures

| Problem | Cause | Fix |
|---|---|---|
| 401 / 403 responses | Endpoint requires auth that we cannot provide | Remove auth requirement from webhook receiver |
| Timeout | Endpoint takes >10s to respond | Return 200 immediately, process async |
| SSL error | Invalid or self-signed certificate | Use a valid TLS certificate |
| 5xx responses | Server error on customer side | Fix the endpoint error; retries happen for 24h |

## Retry policy

Failed webhooks are retried with exponential backoff: 5 min, 30 min, 2h, 8h, 24h. After 24h the delivery is abandoned and marked as failed in the webhook log.

## Webhook log

All delivery attempts are logged in Settings > Developer > Webhooks > Delivery log. Customers can inspect payloads, response codes, and retry history.

KEYWORDS: webhook, webhook setup, webhook delivery, webhook failure, signature verification, endpoint, webhook retry, integration, event subscription
