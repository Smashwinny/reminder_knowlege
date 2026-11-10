# ESP32、家庭网络与 Tailscale：2026-11-11 收尾归档

本页汇总机器人停止学习前已经产出的材料。归档检查不等于重新完成真实服务、硬件或生产环境验证；请以各项限制及原始实验日志为准。

原始交付包已在本地保留；公开目录仅收录经筛选的教材、原创练习、来源说明和必要结果。第三方完整源码、抓取全文及重复压缩包不随本次提交发布。

## 小钰 · ESP32、家庭网络与 Tailscale

- 来源：[https://x.com/0xNathanWalk/status/2112539228278239708](https://x.com/0xNathanWalk/status/2112539228278239708)
- 归档状态：**待验证（模拟/组件实验，真实硬件或服务未验证）**
- 完整学习验收：本轮未新增完整学习验收，也未更改 Reminder 任务完成状态。

验证范围与缺项：

- # experiment-log（真实输出与边界）  实验主机：Grok Bot 云端 Linux 盒子，不是用户本机，不能访问用户 F 盘。时区 Asia/Shanghai。 未登录 Tailscale，未使用用户密钥，未购买服务，未修改宿主机安全设置。宿主机 `/proc/sys/net/ipv4/ip_forward` 只读（值为 1），从未写入。 
- ## 中途失败（如实记录，不把失败说成成功）  1. 第一次 E5（约 2026-11-11 01:18:34–01:18:41）：office 与 visitor 都创建名为 `wg0` 的接口，但共享该 unshare 的 `/run/wireguard/wg0.sock`，visitor 侧出现 `UAPI listen error: unix socket in use`，`Cannot find device "wg0"`，叠加探测超时（2004.7 ms）。该次 E4 已经成功。随后改为接口名 `wga`/`wgb` 重跑。 2. 中间一次（约 01:18:54）E4 与 E5 均已成功（叠加 5.4 ms，抓包 12 个 UDP/51820），但日志摘要脚本引号转义错误，进程在写 `SNIFF_JSON` 时以退出码 1 结束，宿主机接口仍然干净。修复脚本后于 01:19:22 完整重跑，作为交付记录。 3. `ip netns` 直接在宿主机执行会因不能写 `/run/netns` 而失败。解决办法是在 user+mount 命名空间里把 tmpfs 挂到 `/run`，只影响该隔离环境。 4. 本环境没有 `ping`、`tcpdump`、`wg`、`sysctl` 二进制。分别用 Python TCP echo、AF_PACKET 抓包、wireguard-go UAPI、以及读写 `/proc/sys` 替代。这些是工具替代，不是实验失败。 5. ESP-IDF 在线 Wi-Fi 驱动 HTML 多次 TLS 中断或仅得到跳转页；改从 GitHub 固定 v6.1 读取 `esp_netif.h` 与 ESP-NETIF 文档。`wifi-driver/index.rst` 只是 toctree（263 字节），不是完整驱动正文。 

阅读与实验入口：

- [experiment-log.md](xiaoyu_20261111_5/experiment-log.md)
- [knowledge-proposal.md](xiaoyu_20261111_5/knowledge-proposal.md)
- [sources.md](xiaoyu_20261111_5/sources.md)
- [家庭网络与加密叠加-增量学习指南.html](xiaoyu_20261111_5/%E5%AE%B6%E5%BA%AD%E7%BD%91%E7%BB%9C%E4%B8%8E%E5%8A%A0%E5%AF%86%E5%8F%A0%E5%8A%A0-%E5%A2%9E%E9%87%8F%E5%AD%A6%E4%B9%A0%E6%8C%87%E5%8D%97.html)
- [家庭网络与加密叠加-增量学习指南.pdf](xiaoyu_20261111_5/%E5%AE%B6%E5%BA%AD%E7%BD%91%E7%BB%9C%E4%B8%8E%E5%8A%A0%E5%AF%86%E5%8F%A0%E5%8A%A0-%E5%A2%9E%E9%87%8F%E5%AD%A6%E4%B9%A0%E6%8C%87%E5%8D%97.pdf)

其余原创练习文件见 [xiaoyu_20261111_5](xiaoyu_20261111_5/)。
原实验日志保留写作时的状态；补收媒体后的当前归档状态以本页和 media 索引为准。

## 整理说明

同一项目的不同机器人材料按子目录保留，来源与状态逐项记录；内容相近并不等于证据相同。需要原始网页快照或固定版本上游依赖的练习，在取得公开来源后才能重跑，本轮没有为补齐归档启动实验。
