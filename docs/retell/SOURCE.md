# Retell: research source

- Docs index: https://docs.retellai.com/llms.txt
- Full docs: https://docs.retellai.com/llms-full.txt
- API spec: https://docs.retellai.com/openapi.yaml
- First researched: 2026-11-23
- Last checked: 2026-11-23

## Checksums (sha256)

Re-run the full research only if one of these changes.

| File | sha256 |
|---|---|
| raw/llms.txt | 2ae5fb29de70b4b137b01295e2e84c9f070ba698894c2042892e74e9550ba1a1 |
| raw/llms-full.txt | c3e4e124ad3b51313aa398a1757987407980419fa28e16431be38bd25724f7fe |
| raw/openapi.yaml | ba29a797b9b472bb08a08fa7489a136e95a29d995dce7c65b48c8772343755fa |

## Change check

```bash
cd docs/retell/raw
curl -sS -o /tmp/llms.txt https://docs.retellai.com/llms.txt
curl -sS -o /tmp/openapi.yaml https://docs.retellai.com/openapi.yaml
sha256sum /tmp/llms.txt /tmp/openapi.yaml
```
