> 公开归档版说明：下文是原完整实验包的历史README。本轮已移除第三方源码，请先阅读项目根目录[ARCHIVE_DEPENDENCIES.md](../ARCHIVE_DEPENDENCIES.md)。本轮未恢复依赖或重跑，不代表当前目录直接可运行。

# LCU状态化MCP练习（自编模拟，不是真实运行时）

访问日期：2026-11-11 Asia/Shanghai。协议固定MCP 2025-11-25 stdio子集。依赖本机Node（本轮24.22.1）与Python3标准库（本轮3.13.5），无第三方包。Python仅用于本练习，不是当前LCU依赖。

## 一次复现
```bash
cd /workspace/learn-batch/02-lcu/exercise
python3 demo.py baseline
python3 demo.py protocol
python3 demo.py state
python3 demo.py reset
python3 demo.py negative
python3 demo.py upstream
node --test vendor/adapters/test/host-guard.test.mjs
```
解压ZIP后先进入解压出的exercise目录再运行其余命令即可；baseline的上游一致性检查需原项目根的upstream快照，便携解压时用以下离线校验替代，不下载原始运行时：
```bash
python3 verify_vendor.py
```
其他5组和node测试只依赖ZIP内容。results是本轮生成证据，重跑会覆盖同名结果，不要把用户数据放进去。

## 对应来源与许可
- `mock_mcp.mjs`：自编JSON-RPC服务与内存桌面夹具；借鉴LCU公开的双工具/保留状态设计，不复制OpenAI代码或指令，不实现官方cua API兼容。
- `demo.py`：自编协议驱动与41个命名检查，真实spawn子进程；部分为源文件/文档断言，不是41次真实桌面操作。
- `vendor/tests/mcp_client.py`：上游tests/mcp_client.py原样副本，用其Client调用本模拟器；显式指定2025-11-25而非其默认旧版本。
- `vendor/adapters/host-guard.mjs`和`vendor/adapters/test/host-guard.test.mjs`：上游原样MIT代码/测试。测试注入进程表、bundle ID与环境对象；包含关闭护栏的纯对象分支检查，但没有更改实际进程环境或用户安全设置。
- 上述vendor来自 https://github.com/amontlabs/lcu/tree/a7e30c1862707214dfe748d410854771ab4f4494 ，LCU版权/许可保留于vendor/LICENSE。官方ChatGPT应用/运行时/指令不是MIT授权的一部分；本包未分发。

## 关键限制
- `node:vm`不是安全沙箱。只用随包受信任的固定代码，不向模型或外部输入开放、不注册到用户宿主。
- 仅同步JS；不支持顶层await、模块加载、异步Promise、原版completion_summary形式、图片content、HTTP、elicitation、宿主session/turn与turn_ended。未实现完整MCP合规/版本协商，模拟器遇到其他协议版本明确拒绝。
- 假记事本只有内存字符串与保存标记，不写真实文档。截图接口仅返回actualCapture=false的元数据，没有屏幕像素。模拟白名单/坐标检查不是生产安全机制。
- reset只清JS变量，不撤销模拟文档副作用；失败后的盲重试示例故意产生ABB。新进程有独立夹具，不能据此声称真实桌面会话物理隔离。
- 未安装/启动ChatGPT、未登录或使用账号/密钥、未接触真实桌面/审批/网站。所有原版运行时、宿主集成与GUI效果待验证。
