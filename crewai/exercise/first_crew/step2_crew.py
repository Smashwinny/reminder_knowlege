# -*- coding: utf-8 -*-
"""第一步实验：两 agent 顺序流水线（研究员 -> 撰稿人）
运行: .venv/Scripts/python step2_crew.py
需要环境变量: ANTHROPIC_BASE_URL / ANTHROPIC_AUTH_TOKEN
"""
import os

os.environ.setdefault("CREWAI_TELEMETRY_OPT_OUT", "true")

from crewai import Agent, Task, Crew, Process, LLM

# 通过 litellm 接入 Anthropic 兼容中转（Z.ai GLM）
llm = LLM(
    model="anthropic/glm-4.6",
    base_url=os.environ["ANTHROPIC_BASE_URL"],
    api_key=os.environ["ANTHROPIC_AUTH_TOKEN"],
    temperature=0.7,
)

researcher = Agent(
    role="资深技术研究员",
    goal="用 3 个要点讲清楚 {topic} 是什么、解决什么问题",
    backstory="你做了十年技术调研，最擅长把复杂概念压缩成大白话。",
    llm=llm,
    verbose=True,
)

writer = Agent(
    role="科普作者",
    goal="把研究员的要点改写成一段 200 字以内、高中生能看懂的介绍",
    backstory="你是知名科普专栏作者，讨厌术语堆砌。",
    llm=llm,
    verbose=True,
)

t1 = Task(
    description="研究 {topic}，输出 3 个要点，每点一句话。",
    expected_output="3 个要点，每点不超过 40 字。",
    agent=researcher,
)

t2 = Task(
    description="基于研究员的要点写一段面向新手的介绍。",
    expected_output="200 字以内的中文介绍段落。",
    agent=writer,
    context=[t1],  # 撰稿人能看到 t1 的结果
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[t1, t2],
    process=Process.sequential,
    verbose=True,
)

result = crew.kickoff(inputs={"topic": "多智能体协作"})
print("\n" + "=" * 60)
print("最终产出：")
print(result.raw)
