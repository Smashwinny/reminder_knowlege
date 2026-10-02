# -*- coding: utf-8 -*-
"""
随记录入管家 · 保存脚本（微信随记机器人实验的核心）
复刻文章《微信聊天框还能这么用？发段文字，自动存进 Obsidian 笔记》中
「创建、接好一个负责保存和 Git 同步的脚本」这一职责。

规则要点（与文章一键配置提示词一致）：
- 一条纯文本 = 一条独立随记，正文原样保留（空格/标点/换行），不总结不润色
- 只另外生成一个简短标题；文件名不重复、不覆盖旧笔记
- 写入后核对原文（复读校验），只提交本条笔记，再拉取合并 + 推送
- 同步冲突保留文件并报告，不强推、不丢弃已有改动
- 成功只回复：保存并同步成功。
- 已保存但推送失败回复：已保存，同步失败：<原因>

用法：
  python save_note.py --msg-file msg.txt            # 纯文本随记
  python save_note.py --type voice                  # 模拟语音消息 → 应被拒绝
"""
import argparse
import datetime
import os
import re
import subprocess
import sys

VAULT = os.path.dirname(os.path.abspath(__file__))          # 主机端笔记库（这里 = host_vault）
INBOX = os.path.join(VAULT, "inbox")                        # 随记子目录


def run(cmd, cwd=None):
    """跑 git 命令；返回 (ok, 输出)"""
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.returncode == 0, (r.stdout + r.stderr).strip()


def refuse(kind: str):
    """非纯文本消息：不保存，只提示（对应文章规则）"""
    print(f"[拒绝] 收到 {kind} 消息：请发送一条纯文本随记。")
    sys.exit(2)


def make_title(body: str) -> str:
    """只另外生成一个简短、中性的概括标题（取首行前 12 个字，清洗路径非法字符）"""
    first = body.strip().splitlines()[0] if body.strip() else "随记"
    first = re.sub(r"[\\/:*?\"<>|#\[\]]", "", first).strip()
    return (first[:12] or "随记")


def note_path_for(title: str) -> str:
    """文件名避免重复，不覆盖旧笔记：时间戳前缀 + 撞名追加序号"""
    stamp = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    base = f"{stamp}-{title}"
    p = os.path.join(INBOX, base + ".md")
    n = 2
    while os.path.exists(p):
        p = os.path.join(INBOX, f"{base}-{n}.md")
        n += 1
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--msg-file", help="纯文本消息文件（模拟微信收到的一条文字）")
    ap.add_argument("--type", default="text",
                    choices=["text", "voice", "image", "video", "file"],
                    help="消息类型，非 text 一律拒绝保存")
    ap.add_argument("--channel", default="wechat-clawbot")
    args = ap.parse_args()

    if args.type != "text":
        refuse(args.type)
    if not args.msg_file:
        print("[失败] 缺少 --msg-file"); sys.exit(1)

    with open(args.msg_file, encoding="utf-8") as f:
        body = f.read()
    if not body.strip():
        print("[失败] 空消息不保存"); sys.exit(1)

    title = make_title(body)
    path = note_path_for(title)
    now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")

    # 1) 写入 Markdown（front-matter 管标题/来源，正文原样，一个字不动）
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("---\n")
        f.write(f"title: {title}\n")
        f.write(f"captured: {now}\n")
        f.write(f"source: {args.channel}-随记\n")
        f.write("---\n\n")
        f.write(body)
        if not body.endswith("\n"):
            f.write("\n")

    # 2) 复读校验：正文必须与原文逐字节一致（不改错字、不总结、不润色）
    with open(path, encoding="utf-8", newline="") as f:
        saved = f.read()
    if body not in saved:
        print("[失败] 复读校验未通过，已删除坏文件"); os.remove(path); sys.exit(1)

    # 3) 只提交本条笔记 → 拉取合并 → 推送（冲突保留文件并报告，不强推）
    ok, out = run(["git", "add", "--", os.path.relpath(path, VAULT)], VAULT)
    ok, out = run(["git", "commit", "-m", f"随记: {title}"], VAULT)
    if not ok and "nothing to commit" not in out:
        print(f"[失败] git commit 失败：{out}"); sys.exit(1)
    ok, out = run(["git", "pull", "--rebase", "--autostash"], VAULT)
    if not ok:
        print(f"已保存，同步失败：pull 冲突，文件已保留，请人工处理\n{out}"); sys.exit(3)
    ok, out = run(["git", "push"], VAULT)
    if not ok:
        print(f"已保存，同步失败：{out}"); sys.exit(3)

    # 4) 成功：固定回复（对应 Hermes Agent 收到文字后的固定话术）
    print("保存并同步成功。")
    print(f"  笔记: {os.path.relpath(path, VAULT)}")
    print(f"  标题: {title}")
    print(f"  正文: {len(body)} 字符，逐字节校验通过")


if __name__ == "__main__":
    main()
