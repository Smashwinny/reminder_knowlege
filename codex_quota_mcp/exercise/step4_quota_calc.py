# -*- coding: utf-8 -*-
"""实验第 4 步：额度账算术——旧工作流 vs 邪修工作流，一年省多少。

文章给的数字：
  - Ultra 分析规划一次 ≈ 烧掉 Codex 周额度的 10%
  - 邪修方案下执行任务只烧周额度约 4%（规划挪到网页版 GPT-6 Pro，Codex 侧 0）
  - $200 Pro 会员：Codex 周额度 100%，网页版每周另有 200 次 GPT-6 Pro（$100 档 50 次）
  - 作者三个 $200 账号轮换 = 每月 $600
"""
import json

WEEKLY = 100.0          # Codex 周额度 100%
OLD_PLAN = 10.0         # Ultra 规划一次 %
OLD_EXEC = 4.0          # 执行一次 %
NEW_EXEC = 4.0          # 邪修：只付执行
PRO_CALLS_200 = 200     # 网页版 GPT-6 Pro 每周次数（$200 档）
PRO_CALLS_100 = 50      # $100 档
MONTHS = 12
WEEKS_PER_MONTH = 4.33

def weekly_capacity(exec_pct, plan_pct=0.0):
    """每周能完成的优化任务数 = floor(周额度 / 每任务消耗)"""
    per_task = plan_pct + exec_pct
    return int(WEEKLY // per_task), per_task

rows = []
old_n, old_per = weekly_capacity(OLD_EXEC, OLD_PLAN)
new_n, new_per = weekly_capacity(NEW_EXEC)
rows.append(("旧工作流", "Ultra 规划+执行全在 Codex", old_per, old_n))
rows.append(("邪修工作流", "网页版 Pro 规划(0% Codex)+Codex 执行", new_per, new_n))

print("=" * 76)
print(f"{'方案':<10} {'说明':<34} {'每任务耗%':>9} {'周吞吐(任务)':>12}")
print("-" * 76)
for name, desc, per, n in rows:
    print(f"{name:<10} {desc:<34} {per:>8.0f}% {n:>12}")

gain = new_n / old_n
print("-" * 76)
print(f"同一账号每周吞吐提升 {gain:.1f} 倍；等价于同样的活，Codex 额度只花 1/{gain:.1f}")

# 账单视角：作者三账号 $600/月。假设业务需要 60 任务/周
DEMAND = 60
old_accounts = -(-DEMAND // old_n)   # ceil
new_accounts = -(-DEMAND // new_n)
old_cost = old_accounts * 200 * MONTHS
new_cost = new_accounts * 200 * MONTHS
print(f"\n业务需求按每周 {DEMAND} 个优化任务算（三账号 $600/月实况）：")
print(f"  旧工作流需要 {old_accounts} 个 $200 账号轮换，一年 ${old_cost:,}")
print(f"  邪修后需要 {new_accounts} 个 $200 账号轮换，一年 ${new_cost:,}")
print(f"  一年省 ${old_cost - new_cost:,}（省 {100 * (old_cost - new_cost) / old_cost:.0f}%）")

# 网页版侧新账：规划要吃 Pro 对话次数
plan_calls = DEMAND
print(f"\n网页版侧：每周规划 {DEMAND} 次，$200 档 {PRO_CALLS_200} 次/{'周'} 够用（余 {PRO_CALLS_200 - plan_calls}），"
      f"$100 档 {PRO_CALLS_100} 次不够（缺 {plan_calls - PRO_CALLS_100} 次）")
print("=" * 76)
print(json.dumps({"old_tasks_per_week": old_n, "new_tasks_per_week": new_n,
                  "speedup": round(gain, 2), "yearly_saving_usd": old_cost - new_cost},
                 ensure_ascii=False))
