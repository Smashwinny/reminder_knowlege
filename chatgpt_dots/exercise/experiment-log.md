# ChatGPT Dots · 实验日志（task 364686bf-d56b-4795-84a3-5b0b04a17e1f）

初跑：2026-10-28；审核修订：2026-11-22。
性质：当前官方产品机制 + 本地持久交接协议。无 Dot 权限，未连接任何电脑。

## 当前官方复核与旧口径纠正

2026-11-22 读取：
- https://learn.chatgpt.com/docs/dots
- https://learn.chatgpt.com/docs/dots/computers-and-apps

确认：每个 dot 有云端电脑/浏览器，个人设备离线时云端工作可继续；本机使用时须在线且 ChatGPT 应用开启，云浏览器不继承个人浏览器登录。渠道、插件和电脑权限分别管理。

纠正：
1. 当前不是只用 GPT-6 Astra；不同任务部分可用不同前沿模型，GPT-6.1 Terra 正在加入。
2. 可连接多台个人电脑；是“每个线程一次一台”，不是账户只能连接一台。
3. 当前只描述 takeover/return control 和云端状态保留，没有文档化快照创建、恢复或回滚。
4. Enterprise/Edu/Healthcare 合格工作区可用；2026-11-18 起默认开启，除非退出。首月仍是扩展额度，不是全免。

## 初稿实验问题

原状态机只有内存 history，却输出“会话快照已存”“状态落盘可审计”“从快照恢复”。这些动作没有代码或文件证据，且被写成接近官方实现。原“一次一台=隔离答案”和仓库“ready 可 release/过期即停止”口径也已纠正。

## 修订后的真实复跑

新版 `HandoffMachine` 使用真实 snapshot 字典，每次转换原子写 JSON，支持重载并校验状态。实际命令：

```bash
python -I chatgpt_dots/exercise/handoff_state_machine.py
python -I chatgpt_dots/exercise/test_handoff_state_machine.py
```

生成 `handoff-audit-v2.json`：4 步交接后重载，状态/历史/快照一致；红线后 STOPPED 再重载仍保持。8 项 unittest 全部通过：完整交接、真实快照、JSON 重载、人工态红线、接管请求红线、非法接管、无快照交还、未知保存状态。

快照、红线和 JSON 落盘全部标为本地自写协议，不是 Dots 官方功能证明。

## PDF 与边界

修订 HTML 后新增 v2 PDF，共 10 页；Windows.Data.Pdf 全部逐页渲染联系表审核：封面/Q1→Q2…Q10→能力/总结→来源，无裁切或空白页。原 PDF 保留，manifest 指向 v2；SHA-256 `c6c33a367b600a2bb2c3fbd5860bac4bfb6202532c13b6513d47430580e8ade8`。未实机验证 Dots、电脑连接、Blender、账单或硬件配置。
