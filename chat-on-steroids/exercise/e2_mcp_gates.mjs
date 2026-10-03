#!/usr/bin/env node
/**
 * 实验 E2：复现 chat-on-steroids 本地 MCP 端点的"安全四道门"
 * 原型：repo/src/main/mcp/server.ts —— 绑 127.0.0.1、per-session secret token 路径、
 *       Host 环回校验（防 DNS rebinding）、Origin 环回校验（防浏览器驱动）、body 上限。
 * 这里用零依赖 Node http 复刻这四道门，再用 fetch 从四个攻击视角实测。
 * 运行：node e2_mcp_gates.mjs   （自身起服务+自测，端口随机）
 */
import http from 'node:http';
import { randomBytes, timingSafeEqual } from 'node:crypto';

const TOKEN = randomBytes(16).toString('hex');       // per-session secret path segment
const PATH = `/${TOKEN}/mcp`;                        // 如 server.ts：token 放路径里
const MAX_BODY = 1024;                               // 实验用小上限（真实项目是 8MB）

function safeEqual(a, b) {                           // 仿 server.ts：长度不同直接拒，等长再 timingSafeEqual
  const ba = Buffer.from(a), bb = Buffer.from(b);
  if (ba.length !== bb.length) return false;
  return timingSafeEqual(ba, bb);
}

const server = http.createServer((req, res) => {
  const json = (code, obj) => { res.writeHead(code, { 'content-type': 'application/json' }); res.end(JSON.stringify(obj)); };

  // 门1：请求路径必须携带 secret token（timingSafeEqual 防时序侧信道）
  if (req.url !== PATH || !safeEqual(req.url, PATH)) return json(404, { error: 'not found (token path mismatch)' });

  // 门2：Host 头必须是环回 —— 防 DNS rebinding（攻击者把 evil.com 解析到 127.0.0.1，
  //      浏览器带着合法 Origin 限制失效时，靠 Host 仍能拦下）
  const host = (req.headers.host ?? '').split(':')[0];
  if (host !== '127.0.0.1' && host !== 'localhost') return json(403, { error: 'Host not loopback (DNS rebinding blocked)' });

  // 门3：若带 Origin 头（说明是浏览器发起），Origin 也必须环回
  const origin = req.headers.origin;
  if (origin) {
    let o = ''; try { o = new URL(origin).hostname; } catch {}
    if (o !== '127.0.0.1' && o !== 'localhost') return json(403, { error: 'Origin not loopback (browser cross-origin blocked)' });
  }

  // 门4：body 大小上限
  let size = 0; const chunks = [];
  req.on('data', c => { size += c.length; if (size > MAX_BODY) { json(413, { error: 'body too large' }); req.destroy(); } else chunks.push(c); });
  req.on('end', () => { if (size <= MAX_BODY) json(200, { ok: true, echo: Buffer.concat(chunks).toString().slice(0, 50) }); });
});

await new Promise(r => server.listen(0, '127.0.0.1', r));   // 只绑环回，随机端口
const port = server.address().port;
const base = `http://127.0.0.1:${port}`;

import { request } from 'node:http';
async function probe(name, { path, headers, body }) {
  const h = headers ?? { host: `127.0.0.1:${port}` };
  try {
    const status = await new Promise((resolve) => {
      const req = request({ host: '127.0.0.1', port, path, headers: { ...h, connection: 'close' },
        method: body ? 'POST' : 'GET' }, (res) => {
        let buf = ''; res.on('data', c => buf += c);
        res.on('end', () => { try { console.log(`${String(res.statusCode).padStart(3)}  ${name}  ->  ${(JSON.parse(buf).error) ?? 'ok'}`); } catch { console.log(`${String(res.statusCode).padStart(3)}  ${name}`); } resolve(res.statusCode); });
      });
      req.on('error', (e) => { console.log(`ERR  ${name}  ->  ${e.code ?? e.message}`); resolve(0); });
      if (body) req.write(body); req.end();
    });
    return status;
  } catch (e) { console.log(`ERR  ${name}  ->  ${e.message}`); return 0; }
}

console.log(`secret path = /${TOKEN.slice(0, 8)}…/mcp\n`);
// 5 个攻击视角 + 1 个合法请求
const s1 = await probe('[攻击1] 错误 token 路径', { path: '/deadbeef/mcp' });
const s2 = await probe('[攻击2] 恶意 Host(DNS rebinding)', { path: PATH, headers: { host: 'evil.example:80' } });
const s3 = await probe('[攻击3] 外站 Origin(浏览器驱动)', { path: PATH, headers: { host: `127.0.0.1:${port}`, origin: 'https://evil.example' } });
const s4 = await probe('[攻击4] 超 body 上限', { path: PATH, body: 'x'.repeat(5000) });
const s5 = await probe('[攻击5] token 错但 Host/Origin 都对', { path: PATH + 'x', headers: { host: `127.0.0.1:${port}` } });
const s6 = await probe('[合法] 正确 token + 环回 Host', { path: PATH, body: JSON.stringify({ tool: 'read', path: '/project/README.md' }) });

const pass = s1 === 404 && s2 === 403 && s3 === 403 && s4 === 413 && s5 === 404 && s6 === 200;
console.log(`\n=== 四道门实测: ${pass ? '全部按预期拦截/放行 PASS' : 'FAIL'} ===`);
server.close();
process.exit(pass ? 0 : 1);
