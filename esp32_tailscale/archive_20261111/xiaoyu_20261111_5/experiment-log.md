# experiment-log（真实输出与边界）

实验主机：Grok Bot 云端 Linux 盒子，不是用户本机，不能访问用户 F 盘。时区 Asia/Shanghai。
未登录 Tailscale，未使用用户密钥，未购买服务，未修改宿主机安全设置。宿主机 `/proc/sys/net/ipv4/ip_forward` 只读（值为 1），从未写入。

## E1–E3、E6（2026-11-11 01:18:34 Asia/Shanghai）

命令：`python3 lab.py all`，退出码 0。完整标准输出见 `exercise/lab-run.txt`，机器可读结果见 `exercise/results.json`。

- Python 3.13.5，iproute2-6.15.0。
- `ip -br addr`：lo 127.0.0.1/8；enp0s3 172.30.0.2/24；docker0 172.17.0.1/16（DOWN/linkdown）。
- `ip route`：default via 172.30.0.1 dev enp0s3；172.30.0.0/24 直连；172.17.0.0/16 经 docker0 且 linkdown。
- E2：9 条成员关系断言全部通过。100.90.0.1 分类为 RFC6598-CGNAT-shared，不是 RFC1918。192.168.1.0/24 地址数 256，可分配 .1–.254，网关占 1 个后余 253。DHCP 状态机：保留拿到 192.168.1.30，动态拿到 192.168.1.100。
- E3：查表结果与断言一致；/25 优于同时存在的 /24。
- E6：`ok: true`。这是同一份教学代码自检，不是独立审核。

## E4–E5 最终成功记录（2026-11-11 01:19:22 Asia/Shanghai）

命令：`bash netns_lab.sh`，退出码 0。完整输出见 `exercise/netns-run.txt`，摘要见 `exercise/netns-results.json`。拓扑在 `unshare --user --map-root-user --mount --net --pid --fork` 内搭建，挂载私有 tmpfs 到该命名空间的 `/run`，用完删除 netns。宿主机接口实验前后仍为 lo / enp0s3 / docker0，共 3 条链路；host `ip_forward` 前后都是 1。

拓扑：office 192.168.10.20/24 默认经 192.168.10.1；visitor 192.168.20.30/24 默认经 192.168.20.1；router 两端 .1。本环境无 `ping` 二进制，探测为 Python TCP echo（`PONG:PING`）。

- 转发关闭（仅 router netns 内 `ip_forward=0`）：office→visitor:9000 `FAIL TimeoutError`，1003.8 ms，退出码 1。
- 对照：router→visitor:9000 `OK`，3.2 ms（服务存活，问题在跨网）。
- office 访问 router:9000 为 Connection refused（网关可达但未监听），2.6 ms，说明同网连通。
- 仅在 router netns 写入 `ip_forward=1` 后：office→visitor `OK` 3.6 ms；visitor→office:9001 `OK` 4.4 ms。

E5：编译并运行 wireguard-go `b3bc704ef0ee21a36298601a9e1e5ff90377ac52`。进程启动时打印“内核已有一等 WireGuard 支持”，本批仍使用用户态进程。临时 X25519 密钥只存在隔离目录，结束后删除。最终公钥（可公开）：

- A：`324eb81916b6d7d82cf4d2040c2270d4231f111f3bd6e6ed8ade19dfe6d62f5e`
- B：`4af3c50904d5b20818747014b71c9dc56b20bcd07bf5ecd3b1e36e7cbf91e248`

UAPI 两端 `errno=0`。office 访问 10.66.0.2:9100 `OK`，5.4 ms。路由器 r-o 抓包约 4 秒：13 个 UDP/51820，1842 字节，0 TCP，0 ICMP；样本地址为 192.168.10.20 ↔ 192.168.20.30 的 51820 端口。内层 TCP 没有出现在路由器抓包里。

## 中途失败（如实记录，不把失败说成成功）

1. 第一次 E5（约 2026-11-11 01:18:34–01:18:41）：office 与 visitor 都创建名为 `wg0` 的接口，但共享该 unshare 的 `/run/wireguard/wg0.sock`，visitor 侧出现 `UAPI listen error: unix socket in use`，`Cannot find device "wg0"`，叠加探测超时（2004.7 ms）。该次 E4 已经成功。随后改为接口名 `wga`/`wgb` 重跑。
2. 中间一次（约 01:18:54）E4 与 E5 均已成功（叠加 5.4 ms，抓包 12 个 UDP/51820），但日志摘要脚本引号转义错误，进程在写 `SNIFF_JSON` 时以退出码 1 结束，宿主机接口仍然干净。修复脚本后于 01:19:22 完整重跑，作为交付记录。
3. `ip netns` 直接在宿主机执行会因不能写 `/run/netns` 而失败。解决办法是在 user+mount 命名空间里把 tmpfs 挂到 `/run`，只影响该隔离环境。
4. 本环境没有 `ping`、`tcpdump`、`wg`、`sysctl` 二进制。分别用 Python TCP echo、AF_PACKET 抓包、wireguard-go UAPI、以及读写 `/proc/sys` 替代。这些是工具替代，不是实验失败。
5. ESP-IDF 在线 Wi-Fi 驱动 HTML 多次 TLS 中断或仅得到跳转页；改从 GitHub 固定 v6.1 读取 `esp_netif.h` 与 ESP-NETIF 文档。`wifi-driver/index.rst` 只是 toctree（263 字节），不是完整驱动正文。

## 明确未做

- ESP32 / M5Stack StopWatch 实机、作者未公开固件、眨眼/闭眼规则实测。
- 登录 Tailscale、DERP、协调服务器、预授权密钥。
- 在宿主机或用户网络上开启或关闭转发、安装 VPN、修改防火墙。
- 把作者家中的 Mac mini、手机热点或 Shadowrocket 配置拿来复现。
