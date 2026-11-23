// Local voice test page for one client's receptionist.
// Usage: node server.mjs <client-folder> [--port 8787] [--no-open]
// Reads RETELL_API_KEY from the environment or the repo's .env, and the agent
// details from <client-folder>/build/test-page.json. No npm install needed.

import { createServer } from "node:http";
import { readFileSync, existsSync } from "node:fs";
import { randomBytes } from "node:crypto";
import { join, resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { spawn } from "node:child_process";
import { proxy } from "./proxy.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const clientDir = resolve(args.find((a) => !a.startsWith("--")) || ".");
const port = Number(args[args.indexOf("--port") + 1]) || 8787;
const noOpen = args.includes("--no-open");

function loadEnvKey() {
  if (process.env.RETELL_API_KEY) return process.env.RETELL_API_KEY;
  // Walk up from the client folder to find the repo's .env.
  let dir = clientDir;
  for (let i = 0; i < 6; i++) {
    const f = join(dir, ".env");
    if (existsSync(f)) {
      const m = readFileSync(f, "utf8").match(/^RETELL_API_KEY=(.+)$/m);
      if (m) return m[1].trim();
    }
    dir = dirname(dir);
  }
  return null;
}

const apiKey = loadEnvKey();
const cfgPath = join(clientDir, "build", "test-page.json");
if (!apiKey) { console.error("RETELL_API_KEY not found in the environment or .env"); process.exit(1); }
if (!existsSync(cfgPath)) { console.error(`Missing ${cfgPath}`); process.exit(1); }
const config = JSON.parse(readFileSync(cfgPath, "utf8"));
const accessCode = randomBytes(16).toString("hex");
const html = readFileSync(join(here, "index.html"), "utf8");

const send = (res, status, body, type = "application/json") => {
  res.writeHead(status, { "Content-Type": type, "Cache-Control": "no-store" });
  res.end(type === "application/json" ? JSON.stringify(body) : body);
};

createServer(async (req, res) => {
  const url = new URL(req.url, "http://localhost");
  try {
    if (req.method === "GET" && url.pathname === "/") return send(res, 200, html, "text/html; charset=utf-8");
    if (req.method === "GET" && url.pathname === "/config.json") {
      // Public details only: no keys.
      const { agent_id, business_name, agent_name, scenarios } = config;
      return send(res, 200, { agent_id, business_name, agent_name, scenarios });
    }
    let body = "";
    for await (const chunk of req) body += chunk;
    const out = await proxy(
      { method: req.method, path: url.pathname, auth: req.headers.authorization, body },
      { apiKey, accessCode, agentId: config.agent_id },
    );
    return send(res, out.status, out.body);
  } catch (err) {
    return send(res, 500, { error: String(err.message || err) });
  }
}).listen(port, "127.0.0.1", () => {
  const link = `http://localhost:${port}/#code=${accessCode}`;
  console.log(`Test page for ${config.business_name}: ${link}`);
  if (noOpen) return;
  const opener = process.platform === "darwin" ? "open" : process.platform === "win32" ? "cmd" : "xdg-open";
  const opArgs = process.platform === "win32" ? ["/c", "start", "", link] : [link];
  try { spawn(opener, opArgs, { stdio: "ignore", detached: true }).unref(); } catch {}
});
