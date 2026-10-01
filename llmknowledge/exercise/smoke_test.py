# -*- coding: utf-8 -*-
"""冒烟测试:agno 3.x + Anthropic 兼容接入点(api.z.ai / GLM)是否可用"""
import os
from agno.agent import Agent
from agno.models.anthropic import Claude

agent = Agent(
    name="smoke",
    model=Claude(
        id="glm-4.6",
        api_key=os.environ["ANTHROPIC_AUTH_TOKEN"],
        client_params={"base_url": os.environ["ANTHROPIC_BASE_URL"]},
    ),
    instructions="用一句话回答。",
)

out = agent.run("什么是 AI 智能体(Agent)?")
print("=== 输出 ===")
print(out.content)
print("=== 工具调用次数:", out.metrics.get("tool_calls", "n/a") if out.metrics else "n/a", "===")
