# DSH 插件个人学习用离线组件练习

这是自写教学夹具，不是上游完整测试套件、独立安全审核、真实DSH会话或模型审查。固定来源：repositories.json、provenance.json（完整URL+SHA+SHA256）。upstream内文件未改动。

前提：Python3、Node >=24.9.0；本次Node24.22.1。解压到新目录：
```bash
cd exercise
python3 run.py
```
六步全离线复跑，无需npm install、DSH、账户、密钥或模型。只写父目录experiment-log.md、results.json及fixtures/rewind/entry.json（练习JSON）。不会访问真实用户配置、代码/会话或账单。人工费率/汇率不代表市场报价。

network-guard.mjs只在本Node进程替换fetch/http/https/net/tls常用入口，任何尝试抛错并计数；不是系统防火墙，也不证明其他源码全都不联网。五个JS步骤本次计数均0。

## 许可
- upstream/dsh-rewind与dsh-cost-meter为MIT，完整LICENSE已附。
- upstream/review-feng/src/model-approval.mjs为非商业源码公开许可，非OSI开源；完整LICENSE已附。本包仅供个人非商业学习，不授权用于商业项目/产品/收费服务。商业使用需向权利人取得书面授权。
- 另两个包仅带身份manifest供复核，未执行其完整宿主代码。
