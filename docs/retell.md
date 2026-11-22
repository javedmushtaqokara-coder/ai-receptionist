# Retell (voice platform)

Last checked: 2026-11-22

## Access
- Base URL: `https://api.retellai.com`
- Auth: `Authorization: Bearer $RETELL_API_KEY` (key in `/.env`)
- Network: `api.retellai.com` is on the cloud environment's allowed hosts.

## Key test (works)
- `GET /list-voices` returns 200 with a valid key and 401 with an invalid key.
  Use this endpoint to test the key.

## Deprecated endpoints (return 400, don't use)
- `GET /list-agents` is a legacy agent list endpoint. Retired; see
  https://docs.retellai.com/deprecation-notice/2026/07-31_agent_list_endpoints
- `GET /list-phone-numbers` is a legacy list endpoint. Retired; see
  https://docs.retellai.com/deprecation-notice/2026/06-15_legacy_list_endpoints
- TODO: read those migration notes and record the replacement list endpoints
  before the first client build.
