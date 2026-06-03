# API Documentation and Integration Guide

This article covers common customer questions about our REST API and helps support agents triage integration-related issues.

## API authentication

- The API uses Bearer token authentication.
- Tokens are generated in the developer settings page of the account.
- Tokens do not expire but can be revoked at any time.
- Enterprise customers can use OAuth 2.0 service accounts for server-to-server integrations.

## Common API errors

| Status code | Meaning | Action |
|---|---|---|
| 401 | Invalid or missing token | Check token in Authorization header |
| 403 | Token lacks required scope | Generate a new token with correct permissions |
| 429 | Rate limit exceeded | Check rate limit headers, implement backoff |
| 500 | Internal server error | Check status page, report if persistent |

## Rate limits

- Free tier: 100 requests/hour
- Pro tier: 1,000 requests/hour
- Enterprise: custom limits — contact account manager

## Documentation gaps

If a customer reports that API documentation is missing or incorrect, log a documentation-gap ticket with the exact endpoint or field name that is unclear or wrong.

KEYWORDS: api, rest api, integration, authentication, bearer token, oauth, rate limit, api error, 401, 403, 429, webhook, endpoint, api key, documentation
