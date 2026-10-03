"""补充实验：SelfConsistency 在 3B 小模型上的真实表现。

主实验发现：应用题场景下 3B 模型的 5 条采样会"集体偷懒"（全部输出
同一个占位答案 x），温度 0.8 也分不出多样性——这正是小模型 + 长推理
的典型失败。换用单步乘法题（推理链短、错误随机），观察多数表决是否
能纠正单次直答的随机错误。结果追加到 results.txt。
"""

from __future__ import annotations

import io
import sys
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from agentic_architectures.architectures import SelfConsistency
from agentic_architectures.llm.factory import get_llm

OUT = io.open("results.txt", "a", encoding="utf-8")


def log(msg: str = "") -> None:
    print(msg)
    OUT.write(msg + "\n")
    OUT.flush()


# (题目, 正确答案) —— 两位数乘法，3B 模型单次正确率约 50-70%
MUL_TASKS = [
    ("What is 87 * 69?", "6003"),
    ("What is 93 * 78?", "7254"),
    ("What is 76 * 49?", "3724"),
    ("What is 58 * 83?", "4814"),
    ("What is 247 * 38?", "9386"),
]


def main() -> None:
    log("")
    log("=" * 72)
    log("补充实验：单步乘法上的 SelfConsistency（5 票表决 vs 单次直答）")
    log("=" * 72)
    # num_predict 封顶：防止小模型在难题上无限生成（本库 get_llm 透传给 ChatOllama）
    llm = get_llm(num_predict=900)
    arch = SelfConsistency(n_samples=5, sample_temperature=0.8, llm=get_llm(num_predict=900))
    correct_arch = correct_naive = 0
    for task, answer in MUL_TASKS:
        t0 = time.time()
        res = arch.run(task)
        naive = llm.invoke(task + "\nAnswer with ONLY the final number.").content.strip()
        ok_arch = answer in res.output.replace(",", "").replace(".0", "")
        ok_naive = answer in naive.replace(",", "").replace(".0", "")
        correct_arch += ok_arch
        correct_naive += ok_naive
        tally = res.metadata.get("tally", {})
        log(f"\n[题] {task}  标准答案={answer}")
        log(f"    单次直答={naive[:30]!r} {'✓' if ok_naive else '✗'} | "
            f"多数表决={res.output[:30]!r} {'✓' if ok_arch else '✗'} [{time.time()-t0:.1f}s]")
        log(f"    表决分布 tally={tally} | 一致度={res.metadata.get('agreement_fraction'):.2f}")
    log(f"\n[汇总] 单次直答 {correct_naive}/{len(MUL_TASKS)}，"
        f"SelfConsistency {correct_arch}/{len(MUL_TASKS)}")
    OUT.close()


if __name__ == "__main__":
    main()
