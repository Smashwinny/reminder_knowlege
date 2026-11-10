#!/usr/bin/env bash
# Isolated user+mount+net namespace lab.
# Does not write host sysctls, does not change host interfaces, does not log private keys.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="${HERE}/netns-results.json"
LOG="${HERE}/netns-run.txt"
WG_GO="${WG_GO:-/tmp/wggo/wireguard-go/wireguard}"
export HERE OUT WG_GO

record_host() {
  echo "---- HOST SNAPSHOT ($1) ----"
  echo "TIME=$(date '+%Y-%m-%d %H:%M:%S %Z')"
  echo "IP_FORWARD=$(cat /proc/sys/net/ipv4/ip_forward)"
  echo "ADDR:"
  ip -br addr
  echo "ROUTE:"
  ip route
  echo "LINK_COUNT=$(ip -o link | wc -l)"
}

{
record_host BEFORE
echo "WG_GO=$WG_GO"
if [[ ! -x "$WG_GO" ]]; then
  echo "WARN: wireguard-go not at $WG_GO; E5 will try to build or skip"
fi

# The entire experiment lives inside this unshare. Host /run and host ifaces stay intact.
unshare --user --map-root-user --mount --net --pid --fork --kill-child -- bash -s << 'INNER'
set -euo pipefail
echo "INSIDE uid=$(id -u) pid=$$"
# Make a private /run so ip-netns and wireguard UAPI sockets work, without touching host /run.
mount -t tmpfs tmpfs /run
mkdir -p /run/netns /run/wireguard /tmp/lw05
echo 0 > /tmp/lw05/host_is_isolated_marker

# Snapshot inner default netns (should only have lo, possibly down)
echo "---- INNER ROOT NETNS ----"
ip -br addr || true
ip route || true

# Create three netns: office (A), router (R), visitor (B)
ip netns add office
ip netns add router
ip netns add visitor

# veth pairs: office--router, visitor--router
ip link add o-r type veth peer name r-o
ip link add v-r type veth peer name r-v
ip link set o-r netns office
ip link set r-o netns router
ip link set v-r netns visitor
ip link set r-v netns router

# Addressing: two /24s, same mask, different ranges (post: 办公网 / 访客网 pattern)
ip netns exec office bash -c '
  ip link set lo up
  ip addr add 192.168.10.20/24 dev o-r
  ip link set o-r up
  ip route add default via 192.168.10.1
'
ip netns exec visitor bash -c '
  ip link set lo up
  ip addr add 192.168.20.30/24 dev v-r
  ip link set v-r up
  ip route add default via 192.168.20.1
'
ip netns exec router bash -c '
  ip link set lo up
  ip addr add 192.168.10.1/24 dev r-o
  ip addr add 192.168.20.1/24 dev r-v
  ip link set r-o up
  ip link set r-v up
  # forwarding stays off first
  echo 0 > /proc/sys/net/ipv4/ip_forward
  echo ROUTER_FWD_START=$(cat /proc/sys/net/ipv4/ip_forward)
'

echo "---- ROUTES ----"
echo "OFFICE:"; ip netns exec office ip addr; ip netns exec office ip route
echo "VISITOR:"; ip netns exec visitor ip addr; ip netns exec visitor ip route
echo "ROUTER:"; ip netns exec router ip addr; ip netns exec router ip route

# TCP probe helper written to /tmp (no ping binary on this box)
cat > /tmp/lw05/probe.py << 'PY'
import socket, sys, time
mode, host, port = sys.argv[1], sys.argv[2], int(sys.argv[3])
timeout = float(sys.argv[4]) if len(sys.argv) > 4 else 1.5
if mode == "listen":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
    s.settimeout(30)
    open("/tmp/lw05/listener.ready", "w").write("ok")
    end = time.time() + 30
    while time.time() < end:
        try:
            c, addr = s.accept()
            data = c.recv(64)
            c.sendall(b"PONG:" + data)
            c.close()
        except socket.timeout:
            continue
        except Exception as e:
            print("listen-err", e)
            break
elif mode == "client":
    t0 = time.time()
    try:
        s = socket.create_connection((host, port), timeout=timeout)
        s.sendall(b"PING")
        data = s.recv(64)
        s.close()
        print(f"OK {data!r} rtt_ms={(time.time()-t0)*1000:.1f}")
        sys.exit(0)
    except Exception as e:
        print(f"FAIL {type(e).__name__}: {e} rtt_ms={(time.time()-t0)*1000:.1f}")
        sys.exit(1)
else:
    sys.exit(2)
PY

# Start underlay echo on visitor :9000
ip netns exec visitor python3 /tmp/lw05/probe.py listen 0.0.0.0 9000 &
LISTENER=$!
for i in 1 2 3 4 5 6 7 8 9 10; do
  [[ -f /tmp/lw05/listener.ready ]] && break
  sleep 0.1
done
echo "LISTENER_READY=$(cat /tmp/lw05/listener.ready 2>/dev/null || echo no)"

echo "==== E4A same-subnet office -> gateway 192.168.10.1 (no listen, use ARP/connect fail is ok); TCP to visitor should FAIL while forward=0 ===="
set +e
echo -n "E4_SAME_GW_TCP "; ip netns exec office python3 /tmp/lw05/probe.py client 192.168.10.1 9000 0.8
# gateway is not listening; that is expected FAIL. Also probe visitor.
echo -n "E4_CROSS_BEFORE "; ip netns exec office python3 /tmp/lw05/probe.py client 192.168.20.30 9000 1.0
E4_BEFORE=$?
set -e
echo "E4_CROSS_BEFORE_EXIT=$E4_BEFORE"
# Confirm we can reach visitor from the router itself (directly connected)
echo -n "E4_ROUTER_TO_VISITOR "; ip netns exec router python3 /tmp/lw05/probe.py client 192.168.20.30 9000 1.0

echo "==== E4B enable forwarding ONLY in router netns ===="
ip netns exec router bash -c 'echo 1 > /proc/sys/net/ipv4/ip_forward; echo ROUTER_FWD_NOW=$(cat /proc/sys/net/ipv4/ip_forward)'
# just in case rp_filter blocks, relax only in this netns
ip netns exec router bash -c 'echo 0 > /proc/sys/net/ipv4/conf/all/rp_filter; echo 0 > /proc/sys/net/ipv4/conf/r-o/rp_filter; echo 0 > /proc/sys/net/ipv4/conf/r-v/rp_filter' || true
sleep 0.2
set +e
echo -n "E4_CROSS_AFTER "; ip netns exec office python3 /tmp/lw05/probe.py client 192.168.20.30 9000 1.5
E4_AFTER=$?
echo "E4_CROSS_AFTER_EXIT=$E4_AFTER"
# reverse
echo -n "E4_REVERSE "; ip netns exec office true
# start a listener on office too for reverse
ip netns exec office python3 /tmp/lw05/probe.py listen 0.0.0.0 9001 &
sleep 0.3
echo -n "E4_REVERSE "; ip netns exec visitor python3 /tmp/lw05/probe.py client 192.168.10.20 9001 1.5
E4_REV=$?
echo "E4_REVERSE_EXIT=$E4_REV"
set -e

echo "E4_SUMMARY before=$E4_BEFORE after=$E4_AFTER reverse=$E4_REV (expect before!=0, after=0, reverse=0)"

# ========== E5 wireguard-go userspace tunnel ==========
echo "==== E5 wireguard-go overlay 10.66.0.0/24 ===="
if [[ ! -x "${WG_GO:-}" ]]; then
  echo "E5_SKIP no wireguard-go binary"
  echo "E5_STATUS=skip" > /tmp/lw05/e5.status
else
  python3 - << 'PY'
import os, secrets, subprocess, pathlib
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption

def keypair():
    priv = X25519PrivateKey.generate()
    priv_h = priv.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption()).hex()
    pub_h = priv.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw).hex()
    return priv_h, pub_h

a_priv, a_pub = keypair()
b_priv, b_pub = keypair()
base = pathlib.Path("/tmp/lw05/wgkeys")
base.mkdir(mode=0o700, exist_ok=True)
# private keys only here, never copied to the exercise log by this file
(base/"a.priv").write_text(a_priv)
(base/"b.priv").write_text(b_priv)
(base/"a.pub").write_text(a_pub)
(base/"b.pub").write_text(b_pub)
os.chmod(base/"a.priv", 0o600)
os.chmod(base/"b.priv", 0o600)
print("A_PUB="+a_pub)
print("B_PUB="+b_pub)
PY

  A_PUB=$(cat /tmp/lw05/wgkeys/a.pub)
  B_PUB=$(cat /tmp/lw05/wgkeys/b.pub)
  echo "A_PUB=$A_PUB"
  echo "B_PUB=$B_PUB"

  # Packet sniffer on the router: count UDP/51820 vs other, never decrypt
  cat > /tmp/lw05/sniff.py << 'PY'
import socket, struct, time, json, sys
iface = sys.argv[1]
duration = float(sys.argv[2])
outp = sys.argv[3]
s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
s.bind((iface, 0))
s.settimeout(0.3)
end = time.time() + duration
counts = {"udp_51820": 0, "other_udp": 0, "tcp": 0, "icmp": 0, "other": 0, "bytes_udp_51820": 0}
samples = []
while time.time() < end:
    try:
        data, addr = s.recvfrom(65535)
    except socket.timeout:
        continue
    # Ethernet 14 + IPv4
    if len(data) < 34:
        continue
    if data[12:14] != b"\x08\x00":
        continue
    ihl = (data[14] & 0x0F) * 4
    proto = data[23]
    ip = data[14:]
    if proto == 1:
        counts["icmp"] += 1
    elif proto == 6:
        counts["tcp"] += 1
    elif proto == 17:
        udp_off = 14 + ihl
        if len(data) >= udp_off + 4:
            sport, dport = struct.unpack("!HH", data[udp_off:udp_off+4])
            if sport == 51820 or dport == 51820:
                counts["udp_51820"] += 1
                counts["bytes_udp_51820"] += len(data)
                if len(samples) < 8:
                    src = ".".join(str(b) for b in data[26:30])
                    dst = ".".join(str(b) for b in data[30:34])
                    samples.append({"src": src, "dst": dst, "sport": sport, "dport": dport, "len": len(data)})
            else:
                counts["other_udp"] += 1
    else:
        counts["other"] += 1
open(outp, "w").write(json.dumps({"counts": counts, "samples": samples}, indent=2))
print(json.dumps({"counts": counts, "n_samples": len(samples)}))
PY

  configure_wg() {
    local ns="$1" ifname="$2" privfile="$3" lport="$4" peerpub="$5" endpoint="$6" allowed="$7" addr="$8"
    # start daemon in netns; interface name = ifname
    ip netns exec "$ns" bash -c "mkdir -p /run/wireguard; LOG_LEVEL=error '$WG_GO' '$ifname'" &
    # wait for UAPI socket
    for i in $(seq 1 50); do
      if ip netns exec "$ns" test -S "/run/wireguard/${ifname}.sock"; then
        break
      fi
      sleep 0.1
    done
    ip netns exec "$ns" test -S "/run/wireguard/${ifname}.sock"
    local priv
    priv=$(cat "$privfile")
    # UAPI set
    ip netns exec "$ns" python3 - << PY
import socket
req = """set=1
private_key=${priv}
listen_port=${lport}
replace_peers=true
public_key=${peerpub}
endpoint=${endpoint}
allowed_ip=${allowed}

"""
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect("/run/wireguard/${ifname}.sock")
s.sendall(req.encode())
# read until empty line or timeout
s.settimeout(2)
data = b""
try:
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk
        if b"\n\n" in data:
            break
except Exception:
    pass
print("UAPI_${ns}_RESP=" + data.decode(errors="replace").replace("\n", " | "))
s.close()
PY
    ip netns exec "$ns" bash -c "
      ip addr add ${addr} dev ${ifname}
      ip link set ${ifname} up
      ip route add ${allowed} dev ${ifname}
      ip addr show ${ifname}
      ip route
    "
  }

  configure_wg office wga /tmp/lw05/wgkeys/a.priv 51820 "$B_PUB" 192.168.20.30:51820 10.66.0.2/32 10.66.0.1/32
  configure_wg visitor wgb /tmp/lw05/wgkeys/b.priv 51820 "$A_PUB" 192.168.10.20:51820 10.66.0.1/32 10.66.0.2/32

  # overlay listener on visitor 10.66.0.2:9100
  ip netns exec visitor python3 /tmp/lw05/probe.py listen 10.66.0.2 9100 &
  sleep 0.4

  # sniff on router r-o while probing overlay
  ip netns exec router python3 /tmp/lw05/sniff.py r-o 4 /tmp/lw05/sniff.json &
  SNIFF=$!
  sleep 0.3
  set +e
  echo -n "E5_OVERLAY "; ip netns exec office python3 /tmp/lw05/probe.py client 10.66.0.2 9100 2.0
  E5=$?
  echo "E5_OVERLAY_EXIT=$E5"
  wait $SNIFF || true
  set -e
  if [[ -f /tmp/lw05/sniff.json ]]; then echo -n "SNIFF_JSON="; tr "\n" " " < /tmp/lw05/sniff.json; echo; else echo SNIFF_JSON=missing; fi
  echo "E5_STATUS=$E5" > /tmp/lw05/e5.status

  # shred private keys inside the namespace (files vanish with unshare anyway)
  if command -v shred >/dev/null; then
    shred -u /tmp/lw05/wgkeys/a.priv /tmp/lw05/wgkeys/b.priv || rm -f /tmp/lw05/wgkeys/a.priv /tmp/lw05/wgkeys/b.priv
  else
    rm -f /tmp/lw05/wgkeys/a.priv /tmp/lw05/wgkeys/b.priv
  fi
fi

# export a machine-readable summary for the parent
python3 - << PY
import json, os, pathlib
p = pathlib.Path("/tmp/lw05")
summary = {
  "e4_cross_before_exit": int(os.environ.get("E4_BEFORE", "-1") or -1),
}
print("INNER_DONE")
PY

# cleanup netns explicitly before unshare exits
ip netns del office || true
ip netns del visitor || true
ip netns del router || true
echo "INNER_CLEANED netns_list=$(ip netns list | tr '\n' ' ')"
INNER

record_host AFTER
echo "LAB_FINISHED"
} 2>&1 | tee "$LOG"

# Parse log into json (no private keys should be present)
python3 - << 'PY'
import json, re, pathlib
here = pathlib.Path(__file__).resolve().parent if False else pathlib.Path("/workspace/learn-batch/05-esp32-tailscale/exercise")
log = (here/"netns-run.txt").read_text(errors="replace")
# refuse to keep private key material if any leaked
for bad in ["private_key=", "a.priv", "BEGIN PRIVATE"]:
    if re.search(r"private_key=[0-9a-f]{64}", log, re.I):
        log = re.sub(r"private_key=[0-9a-fA-F]+", "private_key=<redacted>", log)
        (here/"netns-run.txt").write_text(log)

def grab(pat, default=None):
    m = re.search(pat, log, re.M)
    return m.group(1) if m else default

def grab_line(prefix):
    for line in log.splitlines():
        if line.startswith(prefix):
            return line
    return None

import os
from datetime import datetime, timezone, timedelta
SH = timezone(timedelta(hours=8))

def host_block(which):
    parts = log.split("---- HOST SNAPSHOT")
    for p in parts:
        if p.strip().startswith(f"({which})"):
            return p.split("----")[0] if False else p
    return ""

before = log.split("---- HOST SNAPSHOT (BEFORE) ----")[1].split("----")[0] if "HOST SNAPSHOT (BEFORE)" in log else ""
# simpler: extract IP_FORWARD lines in order
fwds = re.findall(r"IP_FORWARD=(\d+)", log)
# first is before, last is after (host). Ignore inner ones? Inner script doesn't print IP_FORWARD= with that exact host format except record_host.
# record_host prints IP_FORWARD=  twice (before/after). Inner prints ROUTER_FWD_*.
host_fwds = fwds  # should be 2

j = {
    "when": datetime.now(SH).strftime("%Y-%m-%d %H:%M:%S %Z"),
    "e4_cross_before_line": grab_line("E4_CROSS_BEFORE "),
    "e4_cross_after_line": grab_line("E4_CROSS_AFTER "),
    "e4_reverse_line": grab_line("E4_REVERSE "),
    "e4_cross_before_exit": grab(r"E4_CROSS_BEFORE_EXIT=(\d+)"),
    "e4_cross_after_exit": grab(r"E4_CROSS_AFTER_EXIT=(\d+)"),
    "e4_reverse_exit": grab(r"E4_REVERSE_EXIT=(\d+)"),
    "e5_overlay_line": grab_line("E5_OVERLAY "),
    "e5_overlay_exit": grab(r"E5_OVERLAY_EXIT=(\d+)"),
    "a_pub": grab(r"^A_PUB=([0-9a-f]+)$"),
    "b_pub": grab(r"^B_PUB=([0-9a-f]+)$"),
    "host_ip_forward_before": host_fwds[0] if host_fwds else None,
    "host_ip_forward_after": host_fwds[-1] if host_fwds else None,
    "router_fwd_start": grab(r"ROUTER_FWD_START=(\d+)"),
    "router_fwd_now": grab(r"ROUTER_FWD_NOW=(\d+)"),
    "sniff": None,
    "host_unchanged_forward": None,
}
m = re.search(r"SNIFF_JSON=(\{.*\})", log)
if not m:
    m = re.search(r"SNIFF=(\{.*\})", log)
if m:
    try:
        j["sniff"] = json.loads(m.group(1))
    except Exception as e:
        j["sniff_raw"] = m.group(1)[:2000]
        j["sniff_err"] = str(e)
j["host_unchanged_forward"] = j["host_ip_forward_before"] == j["host_ip_forward_after"]
(here/"netns-results.json").write_text(json.dumps(j, ensure_ascii=False, indent=2)+"\n")
print("WROTE", here/"netns-results.json")
print(json.dumps(j, ensure_ascii=False, indent=2))
PY
