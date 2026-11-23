---
name: research-voice-platform
description: Research a voice AI platform (Retell, Vapi, Bland, and others) end to end and cache the results in /docs. Run whenever a new platform is connected, or when a connected platform's docs have changed. Maps what the platform does natively, how to set up each capability through its REST API (integrations, tools, phone numbers, testing), and where a custom function would be needed.
---

# Research a voice platform

Goal: learn a platform once, write it down in `/docs/<platform>/`, and never
re-learn it. Every client build reads these files instead of the live docs.

## When to run

- **New platform connected** (a platform name and API key were just given):
  always run the full research.
- **Platform already researched:** run only the change check (step 1). Do the
  full research again only if the docs changed. Otherwise stop and use the
  cache.

## Output layout

```
/docs/<platform>/
  SOURCE.md        where the docs came from, when they were fetched, and checksums
  CAPABILITIES.md  the capability map (the main deliverable)
  raw/             the downloaded docs, kept for searching (llms.txt, llms-full.txt, openapi spec)
```

Never write API keys or secrets into any of these files.

## Steps

### 1. Fetch the docs and check for changes

1. Find the machine-readable docs. Try these in order:
   `https://<docs-host>/llms.txt`, `/llms-full.txt`, then the OpenAPI spec
   (often linked at the bottom of `llms.txt`, for example `/openapi.yaml`).
   If none exist, read the docs site page by page, starting from its sitemap.
2. Download them to `/docs/<platform>/raw/`.
3. Compute `sha256sum` of each file. If `SOURCE.md` already exists and every
   checksum matches, **stop: the cache is current.** Update only the
   "Last checked" date in `SOURCE.md`.
4. If the docs host is blocked by the network, allow that host in the cloud
   environment (this needs the owner's approval on a card) and retry.

### 2. Read everything

- Read the whole index (`llms.txt`) so no area is missed.
- Read the full text of every page covering: agent types, tools and function
  calling, custom functions, native integrations, phone numbers and
  telephony, SMS, knowledge bases, dynamic variables, webhooks, testing,
  post-call analysis, limits, pricing, and deprecations.
- Parse the OpenAPI spec for the exact endpoints, required fields, tool type
  enums and auth schemes. Trust the spec over prose when they disagree, and
  note the disagreement.
- Search `raw/llms-full.txt` for the rest instead of reading 2 MB in one go.
  A helper that prints one page by its URL path is worth writing.

### 3. Verify against the live account

Use the key from `.env` and make **read-only** calls only:
- the key or account info endpoint
- list agents, phone numbers, knowledge bases and integrations
- the integration catalog, if there is one

This confirms which endpoints are live, which are retired, and what the
account already has. Never create, buy, or delete anything during research.

### 4. Write CAPABILITIES.md

Use these sections, each with the exact API endpoint and key fields:

1. **Account snapshot:** what the live account has today.
2. **API basics:** base URL, auth header, key test endpoint, pagination,
   and the current (non-deprecated) list endpoints.
3. **Building an agent:** agent types, which one to default to, and the
   create, update and publish sequence.
4. **Native tools:** every built-in tool type and what it is for.
5. **Native integrations:** each provider, its tools, and whether it can be
   connected **by API** (an API key we can enter) or needs the **owner to
   sign in on the dashboard** (OAuth).
6. **Phone numbers:** buying, importing, binding agents, fallback, SMS, and costs.
7. **Knowledge bases and dynamic variables.**
8. **Testing:** every testing method and which ones can run through the API.
9. **Webhooks and post-call analysis.**
10. **Custom function needed:** a table listing each common receptionist
    need, the native way to cover it, and when that falls short so a custom
    function (a hosted endpoint) or code tool is needed.
11. **Dashboard-only:** things the API can't do, which the owner or a
    dashboard step must handle.
12. **Gotchas and deprecations:** retired endpoints and upcoming removals
    with their dates.

### 5. Write SOURCE.md

Include the docs URLs, the fetch date, the checksum of each raw file, and a
"Last checked" date.

### 6. Update CLAUDE.md

Make sure the platform is listed under "Platforms in use" and points to
`/docs/<platform>/CAPABILITIES.md`.

### 7. Report

Report in three parts, the same as a build: **Learned** (the main
capabilities), **Assumed**, and **Couldn't check**.
