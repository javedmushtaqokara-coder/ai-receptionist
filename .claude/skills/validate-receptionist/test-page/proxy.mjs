// Shared proxy logic for the voice test page.
// The browser SDK sends `Authorization: Bearer <access code>` to our server.
// We check the code, swap in the real Retell API key, and forward only the
// few endpoints a web call needs. The API key never reaches the browser.

const RETELL = "https://api.retellai.com";

// Method + path pattern the page is allowed to use.
const ROUTES = [
  ["POST", /^\/v3\/create-web-call$/],
  ["POST", /^\/v2\/stop-call\/[\w-]+$/],
  ["GET", /^\/v2\/get-call\/[\w-]+$/],
];

export async function proxy({ method, path, auth, body }, { apiKey, accessCode, agentId }) {
  if (!accessCode || auth !== `Bearer ${accessCode}`) {
    return { status: 401, body: { error: "Wrong or missing access code" } };
  }
  if (!ROUTES.some(([m, re]) => m === method && re.test(path))) {
    return { status: 404, body: { error: "Not allowed" } };
  }
  let payload;
  if (method === "POST") {
    payload = body ? JSON.parse(body) : {};
    // Only ever call the agent this page was built for.
    if (path === "/v3/create-web-call") payload.agent_id = agentId;
  }
  const res = await fetch(RETELL + path, {
    method,
    headers: { Authorization: `Bearer ${apiKey}`, "Content-Type": "application/json" },
    body: payload ? JSON.stringify(payload) : undefined,
  });
  const text = await res.text();
  let json;
  try { json = text ? JSON.parse(text) : {}; } catch { json = { raw: text }; }
  // Never send the stored recording or log URLs to the page; the transcript is enough.
  if (path.startsWith("/v2/get-call/") && json && typeof json === "object") {
    json = {
      call_id: json.call_id,
      call_status: json.call_status,
      disconnection_reason: json.disconnection_reason,
      transcript_object: json.transcript_object,
      transcript: json.transcript,
      call_analysis: json.call_analysis,
      latency: json.latency,
    };
  }
  return { status: res.status, body: json };
}
