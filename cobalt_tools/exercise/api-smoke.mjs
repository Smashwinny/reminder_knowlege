import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { once } from "node:events";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const apiDir = path.resolve(here, "../repo/api");
const apiEntry = path.join(apiDir, "src/cobalt.js");
const origin = "http://127.0.0.1:19100";
let serverOutput = "";

const child = spawn(process.execPath, [apiEntry], {
  cwd: apiDir,
  env: {
    ...process.env,
    API_URL: `${origin}/`,
    API_PORT: "19100",
    API_LISTEN_ADDRESS: "127.0.0.1",
    RATELIMIT_MAX: "100",
  },
  stdio: ["ignore", "pipe", "pipe"],
});
child.stdout.on("data", (chunk) => { serverOutput += chunk.toString(); });
child.stderr.on("data", (chunk) => { serverOutput += chunk.toString(); });

const post = async (body, accept = "application/json") => {
  const response = await fetch(`${origin}/`, {
    method: "POST",
    headers: { Accept: accept, "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return { httpStatus: response.status, body: await response.json() };
};

const waitUntilReady = async () => {
  const deadline = Date.now() + 20000;
  let lastError;
  while (Date.now() < deadline) {
    if (child.exitCode !== null) throw new Error(`API exited early: ${serverOutput}`);
    try {
      const response = await fetch(`${origin}/`);
      if (response.ok) return response.json();
    } catch (error) {
      lastError = error;
    }
    await new Promise((resolve) => setTimeout(resolve, 150));
  }
  throw new Error(`API readiness timeout: ${lastError}\n${serverOutput}`);
};

try {
  const info = await waitUntilReady();
  assert.equal(info.cobalt.version, "11.7.1");
  assert.equal(info.cobalt.url, `${origin}/`);
  assert.equal(info.git.commit, "a636575b09de1fc55d9b8cd98cac88f5f2f16b42");
  assert.ok(Array.isArray(info.cobalt.services));
  assert.ok(info.cobalt.services.length >= 20);

  const missingURL = await post({});
  assert.equal(missingURL.httpStatus, 400);
  assert.equal(missingURL.body.error.code, "error.api.link.missing");

  const wrongAccept = await post(
    { url: "https://example.com/public/123" }, "text/plain",
  );
  assert.equal(wrongAccept.httpStatus, 400);
  assert.equal(wrongAccept.body.error.code, "error.api.header.accept");

  const unsupported = await post({ url: "https://example.com/public/123" });
  assert.equal(unsupported.httpStatus, 400);
  assert.equal(unsupported.body.error.code, "error.api.link.invalid");

  console.log(JSON.stringify({
    suite: "official cobalt API on loopback; no third-party media requests",
    getRoot: {
      version: info.cobalt.version,
      commit: info.git.commit,
      serviceCount: info.cobalt.services.length,
      services: info.cobalt.services,
    },
    postMissingURL: missingURL,
    postWrongAccept: wrongAccept,
    postUnsupportedDomain: unsupported,
  }, null, 2));
  console.log("PASS: official API started and 10 HTTP/schema assertions passed");
} finally {
  if (child.exitCode === null) {
    child.kill();
    await Promise.race([
      once(child, "exit"),
      new Promise((resolve) => setTimeout(resolve, 3000)),
    ]);
    if (child.exitCode === null) child.kill("SIGKILL");
  }
  console.log("--- official API startup output ---");
  console.log(serverOutput.trim());
}
