# -*- coding: utf-8 -*-
"""第四步实验：给 agent 发一件工具（自定义 BaseTool）
运行: .venv/Scripts/python step4_tool.py
"""
import os

os.environ.setdefault("CREWAI_TELEMETRY_OPT_OUT", "true")

from crewai import Agent, Task, Crew, LLM
from crewai.tools import BaseTool

# 一件"假数据库"工具：不联网，固定返回菜价表
class MenuTool(BaseTool):
    name: str = "canteen_menu_query"
    description: str = "查询今天食堂菜单和价格。输入菜名或'全部'。"

    def _run(self, query: str = "全部") -> str:
        menu = {
            "红烧肉": 12, "番茄炒蛋": 8, "清炒时蔬": 6, "糖醋里脊": 13,
        }
        if query in menu:
            return f"{query}: {menu[query]} 元"
        return "; ".join(f"{k} {v}元" for k, v in menu.items())


llm = LLM(
    model="anthropic/glm-4.6",
    base_url=os.environ["ANTHROPIC_BASE_URL"],
    api_key=os.environ["ANTHROPIC_AUTH_TOKEN"],
)

helper = Agent(
    role="食堂推荐官",
    goal="根据菜单帮同学推荐 10 元预算内最划算的搭配",
    backstory="你在食堂工作了五年，闭着眼知道哪个窗口好吃。",
    llm=llm,
    tools=[MenuTool()],
    verbose=True,
)

task = Task(
    description="先查今天的菜单，再推荐一份 10 元预算内的搭配，说明理由。",
    expected_output="推荐搭配 + 一句话理由。",
    agent=helper,
)

crew = Crew(agents=[helper], tasks=[task])
result = crew.kickoff()
print("\n最终产出：", result.raw)
