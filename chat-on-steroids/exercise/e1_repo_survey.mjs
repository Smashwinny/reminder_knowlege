#!/usr/bin/env node
/**
 * 实验 E1：chat-on-steroids 仓库测绘
 * 目的：不运行整个 Electron 应用，仅通过静态扫描源码，验证 README/docs 声称的
 *       工具面（tool surface）、安全机制、多 Agent 机制确实存在于代码中。
 * 运行：node e1_repo_survey.mjs <repo路径>
 */
import { readdirSync, readFileSync, statSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const repo = process.argv[2] ?? '.';
const rel = (...p) => join(repo, ...p);
const read = (...p) => (existsSync(rel(...p)) ? readFileSync(rel(...p), 'utf8') : '');
const count = (text, re) => (text.match(re) ?? []).length;

let ok = 0, fail = 0;
const check = (name, pass, detail) => {
  console.log(`${pass ? 'PASS' : 'FAIL'}  ${name}${detail ? '  -> ' + detail : ''}`);
  pass ? ok++ : fail++;
};

console.log('=== chat-on-steroids 仓库测绘 ===\n');

// 1. 工具声明面：docs/tool-surface.md 说 Core 有 8 个工具
const doc = read('docs', 'tool-surface.md');
const declared = ['read', 'view_image', 'find', 'apply_patch', 'exec_command',
  'write_stdin', 'update_plan', 'agents'];
const coreSrc = read('src', 'main', 'mcp', 'tools-core.ts') + read('src', 'main', 'mcp', 'plan-tool.ts');
const found = declared.filter(t => coreSrc.includes(`'${t}'`) || coreSrc.includes(`"${t}"`));
check('E1.1 Core 工具 8 个全部在 mcp 工具源码中出现', found.length === declared.length,
  `${found.length}/8: ${found.join(', ')}`);
check('E1.1b update_plan 由独立 plan-tool.ts 承载(自 Codex Apache-2.0 改编)',
  /Adapted from OpenAI Codex's update_plan/.test(read('src', 'main', 'mcp', 'plan-tool.ts')));

// 2. 双连接器（surface）：Core + Desktop
const surfaces = read('src', 'main', 'mcp', 'surfaces.ts');
const hasCore = /core/i.test(surfaces), hasDesktop = /desktop/i.test(surfaces);
check('E1.2 surfaces.ts 同时定义 Core 与 Desktop 两个连接器', hasCore && hasDesktop,
  `core=${hasCore} desktop=${hasDesktop}`);

// 3. 本地端点安全四道门（server.ts 注释声明）
const server = read('src', 'main', 'mcp', 'server.ts');
const gates = {
  'token (timingSafeEqual)': server.includes('timingSafeEqual'),
  'Host 环回校验 (DNS rebinding 防护)': server.includes('localhostHostValidation'),
  'Origin 环回校验': server.includes('localhostOriginValidation'),
  'body 大小上限 (8MB)': server.includes('MAX_BODY_BYTES'),
};
const gatesPass = Object.values(gates).every(Boolean);
check('E1.3 MCP 端点安全四道门全部落地', gatesPass, JSON.stringify(gates));

// 4. 沙箱："约束写在代码里，绝不写在提示词里" —— realpath 规范化防 symlink 逃逸
const sandbox = read('src', 'main', 'sandbox.ts');
check('E1.4 沙箱用 realpath 规范化 + 根比对防 symlink/junction 逃逸',
  sandbox.includes('realpath') && /never delegated to prompt text/i.test(sandbox));

// 5. 工具暴露单调性：撤销权限 -> 工具仍在但返 TOOL_DISABLED
const kernel = read('src', 'main', 'mcp', 'kernel.ts');
check('E1.5 kernel.ts 存在 TOOL_DISABLED 单调性机制',
  kernel.includes('TOOL_DISABLED') && /monotonic/i.test(kernel));

// 6. readOnlyHint 注解（免每调用确认）
const hasReadOnlyHint = count(coreSrc + kernel + read('src', 'main', 'mcp', 'code-mode-tool.ts'),
  /readOnlyHint/g);
check('E1.6 readOnlyHint 注解被广泛使用(>=5 处)', hasReadOnlyHint >= 5, `${hasReadOnlyHint} 处`);

// 7. handoff id 本地生成（防模型伪造 id）
const handoff = read('src', 'main', 'session', 'handoff.ts');
check('E1.7 handoff id 用 randomUUID 本地生成', handoff.includes('randomUUID'));

// 8. 多 Agent / Goal-Loop 机制文件存在（shared/ 放类型与策略，session/ 放执行机器）
const agentish = [
  ...safeList(join(repo, 'src', 'shared')),
  ...safeList(join(repo, 'src', 'main', 'session')),
].filter(f => /agent|goal|continuation|finish|handoff/i.test(f));
check('E1.8 shared+session 下多Agent与Goal/Loop机制文件 >= 10 个', agentish.length >= 10,
  `${agentish.length}: ${agentish.slice(0, 8).join(', ')}...`);

// 9. Chrome 扩展白名单只指向 localhost
const manifest = read('extension', 'manifest.json');
const localhostOnly = (manifest.match(/127\.0\.0\.1:\d+/g) ?? []);
check('E1.9 扩展 host_permissions 含 5 个 localhost 端口(8765-8769)', localhostOnly.length === 5,
  localhostOnly.join(' '));

// 10. 文档规模：worklog 数量反映工程活跃度
const docs = safeList(join(repo, 'docs'));
const worklogs = docs.filter(f => /^worklog-/.test(f));
check('E1.10 docs/ 下 worklog >= 60 篇', worklogs.length >= 60, `${worklogs.length} 篇`);

function safeList(dir) { try { return readdirSync(dir); } catch { return []; } }

console.log(`\n=== 结果: ${ok} PASS / ${fail} FAIL ===`);
process.exit(fail === 0 ? 0 : 1);
