# Security Policy

## Reporting a Vulnerability

Email security@superinstance.ai or open a private security advisory at github.com/SuperInstance/SuperInstance/security.

Please do not publicly disclose vulnerabilities before we've had a chance to respond.

## Response Time
- Acknowledgment: within 48 hours
- Initial assessment: within 5 business days
- Fix: critical 24h, high 72h, medium 2 weeks, low next release

## API Authentication

| Endpoint | Auth Required | Method |
|----------|--------------|--------|
| `POST /search` | No | — |
| `POST /recommend` | No | — |
| `POST /similar` | No | — |
| `GET /stats` | No | — |
| `GET /clusters` | No | — |
| `GET /docs` | No | — |
| `GET /openapi.json` | No | — |
| `POST /ingest` | **Yes** | `Authorization: Bearer <token>` |

Only `/ingest` requires authentication. All read endpoints are public and free.

### Getting an Ingest Token

Contact security@superinstance.ai or open a GitHub issue to request an ingest token.

### Rate Limiting

Public endpoints are currently unrate-limited for development. We ask that you:
- Keep requests under 10/second sustained
- Use `topK` ≤ 20 for search queries
- Cache results locally

Abuse will result in IP-level blocking. Production rate limits coming soon.

## Scope

**In scope:** Fleet Vector API, superinstance.ai, npm packages (@superinstance/*), GitHub repos (github.com/SuperInstance/*)
**Out of scope:** Social media, third-party services (Cloudflare, npm, GitHub), DoS attacks, social engineering

## Best Practices for Users

- Never share API tokens in public repos
- Use environment variables for credentials
- Pin npm package versions in production
- Report unexpected behavior even if unsure it's a vulnerability
