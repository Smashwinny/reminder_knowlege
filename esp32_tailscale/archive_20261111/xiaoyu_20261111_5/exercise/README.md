# exercise：家庭网络、路由与用户态 WireGuard 教学实验

原创教学代码。不登录 Tailscale、不使用用户密钥、不修改宿主机全局转发或接口。

## 依赖

- Python 3.10+（只用标准库；`lab.py` 无需第三方包）
- `iproute2`（`ip`）
- 可选：`cryptography`（仅 `netns_lab.sh` 生成临时 X25519 密钥）
- 可选：在 pinned SHA 编译的 wireguard-go，供 E5 使用

```bash
# 本批实际使用的用户态 WireGuard（不要用本机/用户的 Tailscale 密钥）
# SHA b3bc704ef0ee21a36298601a9e1e5ff90377ac52
# git clone https://github.com/WireGuard/wireguard-go && git checkout b3bc704ef0ee21a36298601a9e1e5ff90377ac52
# go build -o wireguard .
# export WG_GO=/绝对路径/wireguard
```

## 运行

在 `exercise` 目录：

```bash
python3 lab.py env      # E1 只读 ip addr / ip route
python3 lab.py subnet   # E2 子网判定、RFC 分类、DHCP 状态机
python3 lab.py route    # E3 最长前缀匹配
python3 lab.py all      # E1–E3 + 自检，写 results.json

# E4–E5：在 user+mount+net 隔离命名空间中进行，结束后命名空间随 unshare 退出而消失
# 不写宿主机 /proc/sys/net/ipv4/ip_forward
bash netns_lab.sh
```

本云端没有 `ping` 二进制，跨网探测用 Python TCP echo（PONG:PING），不是 ICMP。这不影响“转发开关决定跨子网是否可达”的结论，只是探测协议不同。

## 本批真实结果（云端，2026-11-11 Asia/Shanghai）

见 `results.json`、`lab-run.txt`、`netns-results.json`、`netns-run.txt`。
最终记录的 E4/E5 运行时刻为 2026-11-11 01:19:22 Asia/Shanghai：

- 跨网在路由器转发=0 时超时失败（1003.8 ms）
- 转发=1 后 3.6 ms 成功，反向 4.4 ms
- wireguard-go 叠加地址 10.66.0.1 ↔ 10.66.0.2 用 5.4 ms 成功
- 路由器侧抓包：13 个 UDP/51820，0 个 TCP，0 个 ICMP
- 宿主机 ip_forward 实验前后都是 1（只读，未改）；接口仍为 lo / enp0s3 / docker0

临时私钥只写在隔离命名空间的 `/tmp/lw05/wgkeys`，结束后删除，不进入本目录。日志只保留公钥。

## 不是什么

不是 Tailscale 官方客户端测试，不是 ESP32 实机刷写，不是对作者固件的复现，也不是独立安全审计。
