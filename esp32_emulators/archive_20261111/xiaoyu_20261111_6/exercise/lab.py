#!/usr/bin/env python3
"""ESP 模拟器选型教学实验：可在无 QEMU/esp-emu 的环境下复现。

本程序只做环境记录、芯片对照表、Flash 镜像拼接/填充和分区表解析。
它不启动模拟器，也不能把作者或本批的串口日志当成自己跑出来的结果。
"""
from __future__ import annotations

import argparse
import json
import platform
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "results"
MAGIC_ESP = 0xE9
PTABLE_MAGIC = b"\xAA\x50"
ALLOWED_QEMU_SIZES = (2, 4, 8, 16)  # MiB, from Espressif QEMU C3 docs


def env() -> dict:
    info = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "scope": "teaching helpers only; this program does not launch emulators",
    }
    print(json.dumps(info, indent=2, ensure_ascii=False))
    return info


def matrix() -> dict:
    """对照表来自本批固定的一手 README / CLI，不是星标广告。"""
    rows = [
        {
            "name": "Velxio",
            "repo": "davidmonterocrespo24/velxio",
            "license": "AGPL-3.0 + commercial option",
            "engine": "ESP 系列在服务器/自建实例上跑 QEMU，引脚和串口推回网页",
            "chips": ["esp32", "esp32-s3", "esp32-c3", "esp32-c6 (hosted / velxio.dev; 自建镜像文档写明不包含)"],
            "classic_esp32": "yes (self-host and hosted)",
            "open_source": "yes (AGPL frontend/backend)",
            "web": "canvas + code editor",
            "notes": "AVR/RP2040 可纯浏览器；STM32/Pi Linux/部分合作厂商板仅线上或付费桌面版",
        },
        {
            "name": "esp32sim",
            "repo": "mikroverk/esp32sim",
            "license": "MIT (core); demo assets keep their own licenses",
            "engine": "自研 Rust 模拟器，从芯片 mask ROM 启动",
            "chips": ["esp32-s3 (mature)", "esp32c3 (draft)", "esp32c6 (draft)", "esp32 classic (early)", "esp32-p4 (draft, repo main)"],
            "classic_esp32": "yes (early)",
            "open_source": "yes (MIT)",
            "web": "https://mikroverk.github.io/esp32sim/ (no sockets, no native JIT)",
            "notes": "S3 最成熟；需要单独下载 espressif/esp-rom-elfs",
        },
        {
            "name": "esp-emulator",
            "repo": "espressif/esp-emulator",
            "license": "Apache-2.0 LICENSE file next to binary releases; core source not published as of issue #10",
            "engine": "Rust 二进制模拟器，内嵌常用 ROM ELF，部分 ROM 函数拦截",
            "chips": ["esp32c3", "esp32c5", "esp32c6", "esp32h2", "esp32p4", "esp32s3", "esp32s31 (early)"],
            "classic_esp32": "no",
            "open_source": "undecided (official reply 2026-09-07); helper scripts published",
            "web": "https://espressif.github.io/esp-emulator/ ; page itself has no internet, needs esp-emu-relay",
            "notes": "官方第三个产品；与 espressif/qemu 不是同一个仓库",
        },
        {
            "name": "espressif/qemu",
            "repo": "espressif/qemu",
            "license": "QEMU as a whole is GPL-2.0 (see LICENSE/COPYING)",
            "engine": "QEMU fork with Espressif machine types",
            "chips_xtensa": ["esp32", "esp32s3"],
            "chips_riscv": ["esp32c3", "esp32c5", "esp32c6", "esp32c61", "esp32h2", "esp32h4", "esp32p4"],
            "classic_esp32": "yes",
            "open_source": "yes (QEMU fork, source released)",
            "web": "no first-party web UI in this repo",
            "notes": "需要 2/4/8/16MB 的 raw flash 镜像；C3 文档要求 -icount",
        },
    ]
    out = {
        "rows": rows,
        "post_star_snapshot": {"velxio": "3.3k", "esp32sim": "364", "esp-emulator": "190", "as_of": "author post 2026-10-19"},
        "stars_read_2026_11_11": {"velxio": 3679, "esp32sim": 1126, "esp-emulator": 536, "qemu": 367},
        "scope": "documentation matrix, not a benchmark",
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return out


def _check_magic(data: bytes, offset: int = 0) -> int | None:
    if len(data) <= offset:
        return None
    return data[offset]


def merge_c3(bootloader: bytes, ptable: bytes, app: bytes, size: int = 4 * 1024 * 1024) -> bytes:
    """ESP32-C3 默认布局：bootloader@0x0, ptable@0x8000, app@0x10000。"""
    if bootloader[0] != MAGIC_ESP:
        raise ValueError("bootloader missing 0xE9 magic")
    if app[0] != MAGIC_ESP:
        raise ValueError("app missing 0xE9 magic")
    if not ptable.startswith(PTABLE_MAGIC):
        raise ValueError("partition table missing 0xAA50 magic")
    img = bytearray(bytes([0xFF]) * size)
    for off, blob, name in ((0x0, bootloader, "boot"), (0x8000, ptable, "ptable"), (0x10000, app, "app")):
        if off + len(blob) > size:
            raise ValueError(f"{name} overflows flash image")
        img[off : off + len(blob)] = blob
    return bytes(img)


def merge_classic(bootloader: bytes, ptable: bytes, app: bytes, size: int = 4 * 1024 * 1024) -> bytes:
    """经典 ESP32 默认布局：bootloader@0x1000, ptable@0x8000, app@0x10000。"""
    if bootloader[0] != MAGIC_ESP or app[0] != MAGIC_ESP:
        raise ValueError("ESP image magic 0xE9 missing")
    if not ptable.startswith(PTABLE_MAGIC):
        raise ValueError("partition table missing 0xAA50 magic")
    img = bytearray(bytes([0xFF]) * size)
    for off, blob, name in ((0x1000, bootloader, "boot"), (0x8000, ptable, "ptable"), (0x10000, app, "app")):
        if off + len(blob) > size:
            raise ValueError(f"{name} overflows flash image")
        img[off : off + len(blob)] = blob
    return bytes(img)


def pad_to_allowed(data: bytes) -> tuple[bytes, str]:
    size = len(data)
    mib = size / (1024 * 1024)
    if size in {n * 1024 * 1024 for n in ALLOWED_QEMU_SIZES}:
        return data, "already-allowed"
    # smallest allowed size that fits
    for n in ALLOWED_QEMU_SIZES:
        target = n * 1024 * 1024
        if size <= target:
            return data + bytes([0xFF]) * (target - size), f"padded-to-{n}MiB"
    raise ValueError(f"image larger than 16MiB: {size}")


def qemu_size_ok(n: int) -> bool:
    return n in {x * 1024 * 1024 for x in ALLOWED_QEMU_SIZES}


def parse_ptable(data: bytes, offset: int = 0x8000, max_entries: int = 16) -> list[dict]:
    entries = []
    blob = data[offset:]
    for i in range(max_entries):
        rec = blob[i * 32 : (i + 1) * 32]
        if len(rec) < 32:
            break
        if rec[:2] == b"\xFF\xFF":
            break
        if rec[:2] != PTABLE_MAGIC:
            break
        typ, subtype = rec[2], rec[3]
        part_offset = int.from_bytes(rec[4:8], "little")
        length = int.from_bytes(rec[8:12], "little")
        label = rec[12:28].split(b"\x00", 1)[0].decode("ascii", "replace")
        entries.append(
            {
                "index": i,
                "label": label,
                "type": typ,
                "subtype": subtype,
                "offset": part_offset,
                "length": length,
            }
        )
    return entries


def flash(write: bool = False) -> dict:
    """用合成但格式合法的小镜像演示 merge / pad / 分区解析。"""
    # Minimal ESP image header: magic, 1 segment, unused rest. Not bootable.
    def fake_esp(payload_len: int = 16) -> bytes:
        hdr = bytes([MAGIC_ESP, 1, 0, 0]) + b"\x00" * 12
        return hdr + bytes([0xA5]) * payload_len

    def fake_ptable() -> bytes:
        def entry(label: str, typ: int, subtype: int, off: int, length: int) -> bytes:
            rec = PTABLE_MAGIC + bytes([typ, subtype])
            rec += off.to_bytes(4, "little") + length.to_bytes(4, "little")
            rec += label.encode("ascii").ljust(16, b"\x00")
            rec += b"\x00" * 4  # flags
            assert len(rec) == 32
            return rec

        return (
            entry("nvs", 1, 2, 0x9000, 0x6000)
            + entry("phy_init", 1, 1, 0xF000, 0x1000)
            + entry("factory", 0, 0, 0x10000, 0x100000)
        )

    boot, ptable, app = fake_esp(32), fake_ptable(), fake_esp(64)
    raw_small = merge_c3(boot, ptable, app, size=0x20000)  # 128KiB, invalid for QEMU
    padded, how = pad_to_allowed(raw_small)
    classic = merge_classic(boot, ptable, app, size=4 * 1024 * 1024)
    parsed = parse_ptable(padded)
    out = {
        "raw_small_bytes": len(raw_small),
        "qemu_accepts_raw_small": qemu_size_ok(len(raw_small)),
        "pad": how,
        "padded_bytes": len(padded),
        "qemu_accepts_padded": qemu_size_ok(len(padded)),
        "classic_bytes": len(classic),
        "classic_bootloader_offset": 0x1000,
        "classic_boot_magic": _check_magic(classic, 0x1000),
        "c3_boot_magic": _check_magic(padded, 0x0),
        "ptable": parsed,
        "scope": "synthetic valid headers; not a bootable IDF firmware",
    }
    if write:
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "flash-summary.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
        (OUT / "synthetic-c3-padded.bin").write_bytes(padded)
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return out


def observed() -> dict:
    """本批真实串口中记下的对照数字。不是本函数重新测速或重新启动模拟器。"""
    out = {
        "same_c3_hello_elf_prefix": "4812b1c53",
        "same_c3_hello_heap": 331296,
        "c3_revision": {"esp-emu": "v0.3", "qemu": "v0.3", "esp32sim": "v0.4"},
        "c3_flash_chip": {"esp-emu": "gd", "qemu": "gd", "esp32sim": "generic"},
        "gpio_button_ready_level": {"esp-emu_with_pullup_part": 1, "qemu_no_button_model": 0},
        "classic_revision": {"qemu": "v0.0", "esp32sim": "v2.0"},
        "classic_hello_heap": 303972,
        "classic_xtal_warning_on_esp32sim": True,
        "esp_emu_rejects_chip_esp32": True,
        "scope": "copied from this batch's captured logs; re-run emulators to refresh",
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return out


def verify() -> dict:
    e = env()
    m = matrix()
    f = flash(write=True)
    o = observed()
    checks = {
        "matrix_has_four_tools": len(m["rows"]) == 4,
        "classic_missing_only_on_esp_emu": (
            m["rows"][2]["classic_esp32"] == "no" and m["rows"][1]["classic_esp32"].startswith("yes")
        ),
        "raw_rejected": f["qemu_accepts_raw_small"] is False,
        "padded_accepted": f["qemu_accepts_padded"] is True and f["padded_bytes"] == 2 * 1024 * 1024,
        "ptable_three_entries": [x["label"] for x in f["ptable"]] == ["nvs", "phy_init", "factory"],
        "factory_at_0x10000": f["ptable"][2]["offset"] == 0x10000,
        "magics": f["c3_boot_magic"] == MAGIC_ESP and f["classic_boot_magic"] == MAGIC_ESP,
        "gpio_contrast_recorded": o["gpio_button_ready_level"]["esp-emu_with_pullup_part"]
        != o["gpio_button_ready_level"]["qemu_no_button_model"],
    }
    failed = [k for k, v in checks.items() if not v]
    if failed:
        raise SystemExit(f"verify failed: {failed}")
    result = {"groups_passed": len(checks), "checks": checks, "python": e["python"],
              "scope": "author-written deterministic checks, not independent audit or upstream tests"}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "verify.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("cmd", choices=["env", "matrix", "flash", "observed", "verify"])
    args = p.parse_args(argv)
    {"env": env, "matrix": matrix, "flash": lambda: flash(write=True), "observed": observed, "verify": verify}[args.cmd]()
    return 0


if __name__ == "__main__":
    sys.exit(main())
