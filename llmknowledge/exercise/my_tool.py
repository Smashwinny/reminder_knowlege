# -*- coding: utf-8 -*-
"""
改造实验:给智能体加一个自己发明的工具 —— 掷骰子。
体会"工具就是普通 Python 函数,LLM 负责决定何时调用"这句话。
"""
import os
import random

from agno.agent import Agent
from agno.models.anthropic import Claude

MODEL_PARAMS = dict(
    id="glm-4.6",
    api_key=os.environ["ANTHROPIC_AUTH_TOKEN"],
    client_params={"base_url": os.environ["ANTHROPIC_BASE_URL"]},
)


def roll_dice(sides: int = 6, times: int = 1) -> str:
    """掷一个骰子:sides 是面数,times 是次数,返回每次的点数"""
    rolls = [random.randint(1, sides) for _ in range(times)]
    return f"掷了 {times} 个 {sides} 面骰,结果:{rolls},总和 {sum(rolls)}"


agent = Agent(
    name="骰子管家",
    model=Claude(**MODEL_PARAMS),
    tools=[roll_dice],
    instructions=["你是桌游裁判,涉及随机数的问题必须调用 roll_dice 工具,禁止自己编造随机数。"],
)

agent.print_response("我们玩大富翁,帮我掷 2 个六面骰,再帮我掷 1 个二十面骰决定先攻。", show_tool_calls=True)
