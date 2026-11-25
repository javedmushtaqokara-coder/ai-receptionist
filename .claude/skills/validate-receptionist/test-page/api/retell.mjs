// Vercel version of the local test server, for sharing the test page as a private link.
// Project environment variables: RETELL_API_KEY, ACCESS_CODE, TEST_PAGE_CONFIG (the
// contents of build/test-page.json). vercel.json rewrites /config.json, /v2/* and /v3/* here.
import { proxy } from "../proxy.mjs";

export default async function handler(req, res) {
  const config = JSON.parse(process.env.TEST_PAGE_CONFIG || "{}");
  const path = "/" + String(req.query.route || "");
  if (req.method === "GET" && path === "/config.json") {
    const { agent_id, business_name, agent_name, scenarios } = config;
    return res.status(200).json({ agent_id, business_name, agent_name, scenarios });
  }
  let body = "";
  if (req.method === "POST" || req.method === "PATCH") body = typeof req.body === "string" ? req.body : JSON.stringify(req.body || {});
  try {
    const out = await proxy(
      { method: req.method, path, auth: req.headers.authorization, body,
        sdkVersion: req.headers["x-retell-client-js-sdk-version"] },
      { apiKey: process.env.RETELL_API_KEY, accessCode: process.env.ACCESS_CODE, agentId: config.agent_id },
    );
    res.setHeader("Cache-Control", "no-store");
    return res.status(out.status).json(out.body);
  } catch (err) {
    return res.status(500).json({ error: String(err.message || err) });
  }
}
