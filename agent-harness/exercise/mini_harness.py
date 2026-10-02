# -*- coding: utf-8 -*-
"""
mini_harness.py —— 30 行核心逻辑的迷你 Agent Harness（教学用）
演示 harness 的四个职责：契约 -> 日志 -> 廉价失败(重试) -> 日志变记忆
用法:
    python mini_harness.py run <任务名>          # 跑一个任务
    python mini_harness.py learn <任务名> <教训>  # 任务结束后把教训写进记忆
    python mini_harness.py log                   # 查看执行日志(JSONL)
"""
import json, subprocess, sys, time, datetime, pathlib

BASE = pathlib.Path(__file__).parent
CONTRACT = BASE / "contract.json"
LOG = BASE / "logs" / "run_log.jsonl"
MEMORY = BASE / "memory.md"
OUT = BASE / "output"
MODEL = "haiku"          # 模型可以换，harness 不变 —— 这就是 harness 工程的核心
MAX_RETRY = 2            # 失败廉价：最多重试 2 次


def log_event(event, **kw):
    LOG.parent.mkdir(exist_ok=True)
    rec = {"ts": datetime.datetime.now().isoformat(timespec="seconds"),
           "event": event, **kw}
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def load_contract():
    """职责1：契约。任务开始前先校验边界，防止模型悄悄换活儿。"""
    c = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert c["allowed_outputs"], "契约必须有 allowed_outputs"
    for p in c["allowed_outputs"]:
        OUT.mkdir(exist_ok=True)
    return c


def load_memory():
    """职责4：记忆。harness 每次醒来先把昨天学到的东西注入上下文。"""
    return MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else "(暂无记忆)"


def call_model(prompt):
    """职责3：工具环境。模型只通过这个口子触达世界——一切可审计。"""
    t0 = time.time()
    r = subprocess.run(
        ["claude", "-p", prompt, "--model", MODEL, "--output-format", "json",
         "--permission-mode", "acceptEdits"],  # 授予编辑权限；越界由契约+验证门兜底
        capture_output=True, text=True, encoding="utf-8", timeout=300,
        cwd=str(BASE), shell=True)
    dt = round(time.time() - t0, 1)
    if r.returncode != 0:
        raise RuntimeError(f"exit={r.returncode} stderr={r.stderr[:200]}")
    return json.loads(r.stdout), dt


def verify(contract, task_name):
    """职责5：验证与证据。模型说 DONE 不算数，产出物必须真实存在。"""
    target = OUT / f"{task_name}.md"
    if not target.exists() or target.stat().st_size < 10:
        raise RuntimeError(f"产出物缺失或过小: {target}")
    return target


def run(task_name):
    contract = load_contract()
    log_event("start", task=task_name, model=MODEL,
              contract_scope=contract["scope"])
    # 注意：Windows 下经 cmd.exe 传参，prompt 必须是单行（换行会截断）
    # 记忆注入前必须清洗空白——脏记忆(尾换行)会打破整个 harness（实验中真实踩过的坑4）
    clean_memory = " ".join(load_memory().split())
    prompt = (f"项目约定(必须遵守): {clean_memory} | "
              f"任务({contract['scope']}): {contract['tasks'][task_name]} | "
              f"把结果写入 output/{task_name}.md，然后只回复 DONE。")
    for attempt in range(1, MAX_RETRY + 2):
        try:
            result, dt = call_model(prompt)
            # 保存完整结果供审计（职责3：一切可审计）
            (LOG.parent / f"{task_name}_result.json").write_text(
                json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
            verify(contract, task_name)   # 说 DONE 不算数，产出物必须存在
            cost = result.get("total_cost_usd", 0)
            turns = result.get("num_turns", 0)
            log_event("success", task=task_name, attempt=attempt,
                      seconds=dt, cost_usd=cost, turns=turns)
            print(f"[OK] {task_name} attempt={attempt} {dt}s "
                  f"cost=${cost:.4f} turns={turns} output={OUT / (task_name + '.md')}")
            return
        except Exception as e:
            log_event("fail", task=task_name, attempt=attempt, error=str(e)[:160])
            print(f"[RETRY] {task_name} attempt={attempt} failed: {e}")
            time.sleep(2)
    raise SystemExit(f"[ABORT] {task_name} 重试 {MAX_RETRY} 次仍失败，见 {LOG}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "run":
        run(sys.argv[2])
    elif cmd == "learn":   # 职责4：把本次会话的教训固化为记忆（instinct 的雏形）
        MEMORY.touch()
        with open(MEMORY, "a", encoding="utf-8") as f:
            f.write(f"- [{sys.argv[2]}] {sys.argv[3]}\n")
        log_event("learn", task=sys.argv[2], lesson=sys.argv[3])
        print(f"[LEARNED] {sys.argv[3]} -> memory.md")
    elif cmd == "log":
        print(LOG.read_text(encoding="utf-8") if LOG.exists() else "(空)")
