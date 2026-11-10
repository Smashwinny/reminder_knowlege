# 合入建议（候选，不自行合入）

公开查重快照：Smashwinny/reminder_knowlege main `a8674777e18302b8804b137212b1396cbfe5a747`。已读总览、agent-kernel、archify、源码取证图、事实与判断分离、固定版本中的跨文件时间漂移；学习其卡片、醒目重点、SVG、自证边界的风格，改用用户要求的青蓝橙。

## 建议新增项目笔记
`vault/项目笔记/pi-architecture.md`：不新增同义“Agent循环/MCP/Skills”概念。记录 Pi 四快照依赖图、0.84.2 的 client/protocol 与内置 MCP/codemode 边界、1.2.0 实验栈清理、默认安装遥测分层、当前 main 新 SHA。关联 [[项目笔记/agent-kernel]]、[[沙箱与审批正交]]、[[源码取证图]]。

## 已有概念只补案例
- [[源码取证图]]：manifest 生产依赖闭包不是源码 import 图或网络运行图。0.84.2 与 1.2.0 均闭包 7，但节点不同。
- [[固定版本中的跨文件时间漂移]]：旧审计 SHA 65c43bb5 不能永久称当前；main 已到 b30d54b8，产品仍 1.5.2。1.2.0 “未发布”说明不能抹去 0.84.2 npm ./client 实物。
- [[事实与判断分离]]：真实纯函数 10 用例 + 真实编译方法/mock 5 分支，只证明该组件契约，不证明完整 CLI 或服务端隐私。
- [[沙箱与审批正交]]：QuickJS 限制脚本直接 API，不替宿主 tools/extension 提供 OS 权限边界；0.84.2 的 No permission popups 与当前安全文档分别引用。

## 新增真实证据
六步主实验已在本 worker 云端专用目录真实执行，全退出 0；详见 experiment-log.md 与 exercise/results.json。原先独立审计的实验仅为设计，本次实际运行单独记账，不倒改旧报告。PDF 共 14 页，实际 Chrome 打印并逐页 Read 检查。

## 合入前仍需人工/协调者决定
用户任务勾选、vault 合入、网站标签、Git 发布均未执行。用户本机版本只按其陈述；真实模型/MCP/CLI、账号与服务端留存未验证。不建议为完成学习而自动升级旧版。
