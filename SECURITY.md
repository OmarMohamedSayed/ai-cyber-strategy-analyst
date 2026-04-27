# Security Policy

## Supported Versions

This project is under active development. Security fixes are applied to the latest `main` branch.

## Reporting a Vulnerability

If you discover a security issue:

1. Do **not** open a public GitHub issue with exploit details.
2. Report privately to the maintainers with:
   - affected component/file
   - reproduction steps
   - impact assessment
   - suggested remediation (if available)

We will acknowledge reports as quickly as possible and provide a remediation timeline.

## Secret Management

- Never commit `.env` files.
- Rotate keys immediately if exposure is suspected.
- Use least privilege for all API keys and credentials.

## Known Sensitive Areas

- OpenAI API key handling (`.env`, runtime config)
- Uploaded document storage (`cyber-strategy-ai/data/uploads/`)
- Persisted strategy outputs (`cyber-strategy-ai/data/strategy_results.json`)
