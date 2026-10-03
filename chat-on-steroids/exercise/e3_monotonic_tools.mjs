#!/usr/bin/env node
/**
 * 实验 E3：复现"工具暴露单调性"权限模型
 * 原型：repo/src/main/mcp/kernel.ts —— MCP 端点运行期间工具面是单调的：
 *   · 权限开启时工具才首次注册进 schema；
 *   · 权限中途被撤销时【工具名仍在 schema 里】（防止 ChatGPT 侧缓存的工具快照失效），
 *     但 handler 实时校验当前权限，返回 TOOL_DISABLED；
 *   · readOnlyHint=true 的工具被模型视为只读，不弹确认框。
 * 运行：node e3_monotonic_tools.mjs
 */

// ---- 最小工具注册表（仿 kernel.ts 的 buildServer 思路） ----
const permissions = { read: true, applyPatch: true, execCommand: false }; // exec 默认关

const TOOL_DEFS = {
  read:        { readOnlyHint: true,  handler: () => ({ content: 'file contents...' }) },
  apply_patch: { readOnlyHint: false, handler: () => ({ content: 'patch applied' }) },
  exec_command:{ readOnlyHint: false, handler: () => ({ content: 'command output' }) },
};

// buildServer：只有权限开启的工具才进入暴露面（快照）
function buildServerSnapshot(perms) {
  return Object.keys(TOOL_DEFS).filter(name => {
    const p = { read: 'read', apply_patch: 'applyPatch', exec_command: 'execCommand' }[name];
    return perms[p];
  });
}

// 运行期调用：handler 每次实时校验当前权限 —— 撤销后仍注册着，但拒绝执行
const TOOL_DISABLED = Symbol('TOOL_DISABLED');
function callTool(snapshot, name, args) {
  if (!snapshot.includes(name)) return { error: 'TOOL_NOT_IN_SNAPSHOT', name };
  const p = { read: 'read', apply_patch: 'applyPatch', exec_command: 'execCommand' }[name];
  if (!permissions[p]) return { error: 'TOOL_DISABLED', name,
    detail: '工具仍在快照中（快照不变），但当前权限已关闭，handler 拒绝执行' };
  return TOOL_DEFS[name].handler(args);
}

let ok = 0, fail = 0;
const check = (name, pass, detail) => {
  console.log(`${pass ? 'PASS' : 'FAIL'}  ${name}${detail ? '  -> ' + detail : ''}`);
  pass ? ok++ : fail++;
};

console.log('=== E3: 工具暴露单调性 ===\n');

// 阶段1：read + apply_patch 开，exec 关
let snapshot = buildServerSnapshot(permissions);
console.log(`初始快照: [${snapshot.join(', ')}]`);
check('E3.1 exec_command 权限关闭 -> 不出现在快照', !snapshot.includes('exec_command'));
check('E3.2 read 可正常执行', !callTool(snapshot, 'read').error);
check('E3.3 调未注册的 exec -> TOOL_NOT_IN_SNAPSHOT', callTool(snapshot, 'exec_command').error === 'TOOL_NOT_IN_SNAPSHOT');

// 阶段2：中途开启 exec（端点不重启，快照重建、暴露面扩大）
permissions.execCommand = true;
snapshot = buildServerSnapshot(permissions);
console.log(`\n开启 exec 后快照: [${snapshot.join(', ')}]`);
check('E3.4 权限开启后 exec 立即可用', !callTool(snapshot, 'exec_command').error);

// 阶段3：中途撤销 apply_patch —— 关键：快照里名字还在，handler 却拒绝
permissions.applyPatch = false;
console.log(`\n撤销 apply_patch 权限（快照不重建，模拟 ChatGPT 侧缓存不变）: [${snapshot.join(', ')}]`);
const r = callTool(snapshot, 'apply_patch');
check('E3.5 快照仍包含 apply_patch（保护客户端工具缓存）', snapshot.includes('apply_patch'));
check('E3.6 实际调用返 TOOL_DISABLED（handler 实时校验）', r.error === 'TOOL_DISABLED', r.detail ?? '');

// readOnlyHint 语义：只读工具不需要每次确认
const needConfirm = Object.entries(TOOL_DEFS).filter(([, d]) => !d.readOnlyHint).map(([n]) => n);
check('E3.7 需确认的工具 = apply_patch/exec_command（readOnlyHint=false）',
  needConfirm.join(',') === 'apply_patch,exec_command', `免确认: read`);

console.log(`\n=== 结果: ${ok} PASS / ${fail} FAIL ===`);
process.exit(fail ? 1 : 0);
