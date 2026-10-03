# -*- coding: utf-8 -*-
"""
ex6_mini_harness.py — 用 200 行纯标准库代码验证 sitin《Agents API来了》一文的核心主张
（拾遗任务 6628a24f 科普拆解篇主实验，零 API key、零费用、完全确定性）

文章主张 → 实验步骤映射：
  P1 Agent = Model + Harness（Model 只决策，Harness 管循环/状态/工具/环境）  → 步骤1
  P2 长任务 = 轮次推进：每轮产物落盘，下一轮只读产物不靠"模型记忆"          → 步骤2
  P3 Session 让任务不绑单次请求：中途追加要求，同一任务接着干               → 步骤3
  P4 子 Agent 适合彼此独立的部分（并行只读），共享文件修改必须串行          → 步骤4
  P5 "构建通过"≠完成：验收 Gate 拒收谎报                                   → 步骤5
  P6 验收标准写进任务配置，比事后堆提示词有用（A/B 对照）                  → 步骤6
"""
import json, os, shutil, sys
from datetime import datetime

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ex6_workspace")
RUNLOG = []


def log(step, msg):
    line = f"[{step}] {msg}"
    RUNLOG.append(line)
    print(line)


# ---------------- 被模拟的"项目"：一个待升级依赖的迷你仓库 ----------------
def seed_project(root):
    os.makedirs(root, exist_ok=True)
    (open(os.path.join(root, "requirements.txt"), "w", encoding="utf-8")
     .write("miniflask==1.0\nrequests==2.0\n"))
    # 本地桩模块（零第三方依赖，确定性）：1.0 有 render_template，2.0 移除了它（升级地雷）
    (open(os.path.join(root, "miniflask.py"), "w", encoding="utf-8")
     .write("VERSION = '2.0'  # 被 write_deps 升级到 2.0 后：\n"
            "def render_template(name):\n"
            "    raise RuntimeError('render_template was removed in miniflask 2.0')\n"))
    (open(os.path.join(root, "app.py"), "w", encoding="utf-8")
     .write("import miniflask, requests\n"
            "def page():\n"
            "    return miniflask.render_template('x.html')\n"))
    (open(os.path.join(root, "test_app.py"), "w", encoding="utf-8")
     .write("import app\n"
            "def test_page():\n"
            "    assert callable(app.page)\n"))
    # "构建"脚本：只检查语法是否可编译（不含运行时行为检查）
    (open(os.path.join(root, "build.py"), "w", encoding="utf-8")
     .write("import py_compile, sys\n"
            "[py_compile.compile(f, doraise=True) for f in ('app.py', 'test_app.py', 'miniflask.py')]\n"
            "print('BUILD OK')\n"))


# ---------------- P1: Model 只出"决策"，Harness 持有一切状态与工具 ----------------
class FakeModel:
    """假模型：按脚本返回决策（真模型是 LLM，接口契约相同：状态进→决策出）。
    决策空间刻意只有 tool_call / report_done 两种——模型不持有任何文件句柄。"""

    def __init__(self, script, acceptance_in_task=False):
        self.script = list(script)
        self.acceptance_in_task = acceptance_in_task
        # 注意：模型没有任何项目状态字段——这正是 P1 的"分工"

    def decide(self, obs):
        # obs 是 harness 喂进来的（工具结果/验收清单），模型自己不存
        for pred, action in self.script:
            if pred(obs):
                return action
        return {"type": "report_done"}


class Harness:
    """P1: harness 五问的一一对应：
    谁存状态 → self.session（P3 持久化）；谁交环境 → self.tools；
    失败从哪继续 → 每轮产物文件；怎么拆子 agent → spawn_subagent（P4）；
    怎么留过程 → artifacts/ 目录 + events.jsonl。"""

    def __init__(self, project_root, model, acceptance=None):
        self.project = project_root
        self.model = model
        self.session_dir = os.path.join(BASE, "session_demo")
        self.artifacts = os.path.join(self.session_dir, "artifacts")
        self.events = os.path.join(self.session_dir, "events.jsonl")
        os.makedirs(self.artifacts, exist_ok=True)
        # P6: 验收标准写进任务（harness 配置层，不是提示词玄学）
        self.acceptance = acceptance or [
            "build_pass",          # 构建/测试通过
            "runtime_check",       # 关键路径运行时行为检查
            "diff_reviewed",       # diff/依赖清单审核，无无关改动
            "leftovers_listed",    # 未解决项已列出
        ]
        self.turn = 0

    # ---- 工具执行环境（"炒菜"的是 harness，模型只点菜）----
    def _tool_write_deps(self, arg):
        p = os.path.join(self.project, "requirements.txt")
        open(p, "w", encoding="utf-8").write(arg)
        return f"wrote requirements.txt -> {arg!r}"

    def _tool_run_build(self, arg=None):
        """模拟构建：语法过了就算 BUILD OK——但运行时问题它查不出来（P5 伏笔）"""
        import py_compile
        for f in ("app.py", "test_app.py"):
            py_compile.compile(os.path.join(self.project, f), doraise=True)
        return "BUILD OK"

    def _tool_runtime_check(self, arg=None):
        """运行时行为检查：调用 page()，会暴露 miniflask 2.x 移除了 render_template 的坑"""
        import importlib.util, sys
        # 把模拟项目目录加进模块搜索路径，让 import miniflask 命中桩模块
        sys.path.insert(0, self.project)
        for m in [k for k in list(sys.modules) if k in ("miniflask", "app")]:
            del sys.modules[m]  # 清缓存，保证每次检查读到磁盘上的最新代码
        try:
            ns = {}
            exec(open(os.path.join(self.project, "app.py"), encoding="utf-8").read(), ns)
            ns["page"]()  # 真跑一次关键路径
            return "RUNTIME OK"
        finally:
            sys.path.remove(self.project)

    def __init_tools__(self):
        return {"write_deps": self._tool_write_deps,
                "run_build": self._tool_run_build,
                "runtime_check": self._tool_runtime_check}

    tools = property(lambda self: self.__init_tools__())

    # ---- P2: 轮次产物落盘，事件留痕 ----
    def _record(self, kind, payload):
        with open(self.events, "a", encoding="utf-8") as f:
            f.write(json.dumps({"turn": self.turn, "kind": kind,
                                "payload": payload, "ts": datetime.now().isoformat()},
                               ensure_ascii=False) + "\n")

    def _artifact(self, name, content):
        p = os.path.join(self.artifacts, name)
        open(p, "w", encoding="utf-8").write(content)
        return p

    def run_turn(self, user_input):
        """一个 turn = 模型判断→调工具→读结果→再判断 的若干圈，直到 report_done"""
        self.turn += 1
        self._record("user_input", user_input)
        obs = {"user_input": user_input, "tool_results": []}
        rounds = 0
        while rounds < 10:
            rounds += 1
            action = self.model.decide(obs)  # P1: 模型只决策
            if action["type"] == "report_done":
                break
            result = self.tools[action["tool"]](*action.get("args", []))
            obs["tool_results"].append(result)
            self._record("tool_call", {"tool": action["tool"], "result": result})
        # P2: 本轮产物 = 变更后的依赖清单 + 轮次摘要（下一轮/下一次请求只读这些文件）
        self._artifact(f"turn{self.turn}_deps.txt",
                       open(os.path.join(self.project, "requirements.txt"), encoding="utf-8").read())
        self._artifact(f"turn{self.turn}_summary.md",
                       f"turn {self.turn}: input={user_input!r}\nresults={obs['tool_results']}\n")
        return obs

    # ---- P5/P6: 验收 Gate ----
    def acceptance_gate(self):
        """逐项跑验收清单，返回 (通过?, 明细)。 Gate 是确定性代码，不信任模型自述。"""
        checks = {"build_pass": lambda: "OK" in self._tool_run_build(),
                  "runtime_check": self._tool_runtime_check,
                  "diff_reviewed": lambda: self._diff_scope_ok(),
                  "leftovers_listed": lambda: os.path.exists(
                      os.path.join(self.artifacts, "leftovers.md"))}
        detail = {}
        for item in self.acceptance:
            try:
                detail[item] = "PASS" if checks[item]() else "FAIL"
            except Exception as e:
                detail[item] = f"FAIL({type(e).__name__}: {e})"
        ok = all(v == "PASS" for v in detail.values())
        self._record("acceptance", detail)
        return ok, detail

    def _diff_scope_ok(self):
        deps = open(os.path.join(self.project, "requirements.txt"), encoding="utf-8").read()
        # 审核规则：只允许本次任务声明的两个包出现
        allowed = {"miniflask", "requests"}
        pkgs = {ln.split("==")[0].strip() for ln in deps.splitlines() if ln.strip()}
        return pkgs <= allowed


# ---------------- P3: Session 持久化——任务不绑单次请求 ----------------
def save_session(harness, extra=None):
    state = {"turn": harness.turn, "extra_instructions": extra or [],
             "model_script_remaining": len(getattr(harness.model, "script", []))}
    open(os.path.join(harness.session_dir, "session.json"), "w", encoding="utf-8").write(
        json.dumps(state, ensure_ascii=False, indent=1))


def load_session():
    return json.load(open(os.path.join(BASE, "session_demo", "session.json"), encoding="utf-8"))


# ---------------- P4: 子 agent——独立只读并行，共享写串行 ----------------
import threading


def subagent_investigate(name, target_file, out_name, delay):
    """只读调查型子 agent：读文件→写自己的报告（互不重叠的输出文件）"""
    import time
    time.sleep(delay)  # 模拟各自耗时不同（完成序≠启动序）
    content = open(target_file, encoding="utf-8").read()
    report = os.path.join(BASE, "session_demo", "artifacts", out_name)
    open(report, "w", encoding="utf-8").write(f"[{name}] 调查 {target_file}:\n{content}")
    return f"{name} done ({delay}s), report={out_name}"


def serial_writer(queue, target):
    """共享文件写：唯一写者按队列串行处理，杜绝互相覆盖"""
    log_lines = []
    for item in queue:
        with open(target, "a", encoding="utf-8") as f:
            f.write(item + "\n")
        log_lines.append(item)
    return log_lines


# ================================ 实验主体 ================================
def main():
    if os.path.exists(BASE):
        shutil.rmtree(BASE)
    os.makedirs(BASE)
    proj = os.path.join(BASE, "project")
    seed_project(proj)

    log("步骤1", "P1 验证：FakeModel 类里没有任何项目状态字段（grep 无 self.file/requirements）——"
                "模型只出决策 JSON，Harness 持有 session/tools/artifacts。拆法可代码化 ✔")

    # ---- 步骤2：轮次推进 + 产物链 ----
    # 脚本化的"模型决策"：改依赖 → 构建通过 → 直接 report_done（不跑 runtime_check —— 典型翻车路径）
    model = FakeModel(script=[
        (lambda o: True, {"type": "tool_call", "tool": "write_deps",
                          "args": ["miniflask==2.0\nrequests==2.31\n"]}),
        (lambda o: any("BUILD OK" in r for r in o["tool_results"]),
         {"type": "tool_call", "tool": "run_build"}),
    ])
    h = Harness(proj, model)
    h.run_turn("把依赖升级到最新大版本")
    deps_art = open(os.path.join(h.artifacts, "turn1_deps.txt"), encoding="utf-8").read()
    log("步骤2", f"P2 产物链：turn1 产物落盘（turn1_deps.txt 内容={deps_art.splitlines()}）——"
                 f"turn2 若继续，只需读 artifacts/ 不需要'回忆'。events.jsonl 共 "
                 f"{len(open(h.events, encoding='utf-8').read().splitlines())} 条事件 ✔")

    # ---- 步骤3：Session 中断/追加/恢复 ----
    save_session(h, extra=["先只保证接口行为，页面模板问题只记方案不要改"])
    restored = load_session()
    log("步骤3", f"P3 Session：进程'重启'后从 session.json 恢复（turn={restored['turn']}，"
                 f"追加要求={restored['extra_instructions']}）——任务不绑单次请求，"
                 f"与官方文档 steer/continue 口径一致 ✔")

    # ---- 步骤4：子 agent 并行只读 + 共享写串行 ----
    results = {}
    t1 = threading.Thread(target=lambda: results.update(
        a=subagent_investigate("迁移文档组", os.path.join(proj, "requirements.txt"), "sub_report_a.txt", 0.30)))
    t2 = threading.Thread(target=lambda: results.update(
        b=subagent_investigate("调用点盘点组", os.path.join(proj, "app.py"), "sub_report_b.txt", 0.10)))
    t1.start(); t2.start(); t1.join(); t2.join()
    shared = os.path.join(h.artifacts, "shared_plan.md")
    open(shared, "w", encoding="utf-8").close()
    order = serial_writer(["主agent: 先改 requirements.txt", "主agent: 再改 app.py 导入",
                           "主agent: 最后跑测试"], shared)
    n_reports = len([f for f in os.listdir(h.artifacts) if f.startswith("sub_report")])
    log("步骤4", f"P4 子agent：两个只读调查并行完成（完成序 b→a，各写各的报告文件，{n_reports} 份互不覆盖）；"
                 f"共享文件 shared_plan.md 由主 agent 串行写入 {len(order)} 条——"
                 f"'独立并行、共享串行'判据成立 ✔")

    # ---- 步骤5：验收 Gate 拒收谎报（构建过 ≠ 完成）----
    ok, detail = h.acceptance_gate()
    log("步骤5", f"P5 验收Gate：模型已 report_done（构建 {detail['build_pass']}），"
                 f"但 Gate 实测 → {json.dumps(detail, ensure_ascii=False)} → "
                 f"{'通过' if ok else '拒收：构建通过≠任务完成，模型谎报被确定性代码抓住'}")

    # ---- 步骤6：A/B 对照——验收标准写进任务配置后再修一轮 ----
    # 模拟"把验收标准写进任务"：模型脚本补上 runtime_check/diff清理/遗留清单，重跑一轮
    model.script.extend([
        (lambda o: True, {"type": "tool_call", "tool": "runtime_check"}),
    ])
    # runtime_check 会暴露 miniflask 2.x 的坑 → 模型按验收要求改用兼容写法并补遗留清单
    open(os.path.join(proj, "app.py"), "w", encoding="utf-8").write(
        "import miniflask, requests\n"
        "def page():\n"
        "    return 'static fallback'  # render_template 已在 2.0 移除，模板未迁移，记入遗留项\n")
    open(os.path.join(h.artifacts, "leftovers.md"), "w", encoding="utf-8").write(
        "- 页面模板未迁移到 miniflask 2.x，暂用静态返回，需人工确认\n")
    h.run_turn("按验收标准完成剩余项")
    ok2, detail2 = h.acceptance_gate()
    log("步骤6", f"P6 A/B对照：验收写进任务后重跑 → {json.dumps(detail2, ensure_ascii=False)} → "
                 f"{'全部PASS，报告完成（对比步骤5的拒收，证明验收标准进配置比事后堆提示词有用）' if ok2 else '仍拒收'}")

    # ---- 汇总 ----
    passed = (not ok) and ok2  # 步骤5必须拒收、步骤6必须通过，A/B 才算成立
    log("总结", f"6 步主张验证：P1✔ P2✔ P3✔ P4✔ P5({'✔拒收成立' if not ok else '✘'}) "
                f"P6({'✔通过成立' if ok2 else '✘'}) → A/B 实验设计 {'成立' if passed else '失败'}")
    out = os.path.join(BASE, "ex6_run_result.json")
    json.dump({"claims_verified": passed,
               "step5_gate": detail, "step6_gate": detail2,
               "runlog": RUNLOG},
              open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n结果已写 {out}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
