# -*- coding: utf-8 -*-
"""
我的第一个 AI 智能体:LLM + 工具(Tool)的最小组合。
工具由我们自己用普通 Python 函数定义,LLM 自己决定什么时候调用。
"""
import os
import math
from datetime import datetime

from agno.agent import Agent
from agno.models.anthropic import Claude

MODEL_PARAMS = dict(
    id="glm-4.6",
    api_key=os.environ["ANTHROPIC_AUTH_TOKEN"],
    client_params={"base_url": os.environ["ANTHROPIC_BASE_URL"]},
)


# ---- 工具 1:查当前时间 ----
def now_time() -> str:
    """返回当前日期时间"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ---- 工具 2:计算器 ----
def calculator(expression: str) -> str:
    """计算一个数学表达式,例如 2**10 + sqrt(144)"""
    allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("_")}
    result = eval(expression, {"__builtins__": {}}, allowed)  # 只开放 math,禁止其他内建
    return str(result)


agent = Agent(
    name="小助手",
    model=Claude(**MODEL_PARAMS),
    tools=[now_time, calculator],
    instructions=[
        "你是一个严谨的助手。",
        "遇到需要计算的问题必须调用 calculator 工具,不要心算。",
        "遇到'现在/今天/几点'类问题必须调用 now_time 工具。",
        "回答用中文,并说明你用了哪个工具。",
    ],
    markdown=True,
)

# 问题 1:需要计算器
print("=" * 60)
print("问题 1:光在真空中一年走多少公里?(用 3e5 km/s 算)")
agent.print_response("光速约每秒 3e5 公里,一年有 365 天,光一年能走多少公里?用科学计数法回答。",
                     show_tool_calls=True)

# 问题 2:需要时钟
print("=" * 60)
print("问题 2:现在几点了?")
import time
time.sleep(20)  # 避免触发 API 限流(429)
agent.print_response("现在几点了?今天还能赶上晚饭吗?", show_tool_calls=True)
