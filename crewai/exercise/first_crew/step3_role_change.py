# -*- coding: utf-8 -*-
"""第三步实验：改角色设定，看输出风格变化
只改 researcher 的 role/backstory，其余与 step2_crew.py 相同。
运行: .venv/Scripts/python step3_role_change.py
"""
import os
import sys

os.environ.setdefault("CREWAI_TELEMETRY_OPT_OUT", "true")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from crewai import Agent, Task, Crew, Process, LLM

llm = LLM(
    model="anthropic/glm-4.6",
    base_url=os.environ["ANTHROPIC_BASE_URL"],
    api_key=os.environ["ANTHROPIC_AUTH_TOKEN"],
    temperature=0.7,
)

researcher = Agent(
    role="武侠小说家",
    goal="用 3 个要点讲清楚 {topic} 是什么、解决什么问题，每个要点都要用一个武侠比喻",
    backstory="你在江湖上写了二十年武侠，任何概念到你嘴里都要比划成招式。",
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
    description="研究 {topic}，输出 3 个要点，每点一句话并配一个武侠比喻。",
    expected_output="3 个要点，每点不超过 40 字。",
    agent=researcher,
)

t2 = Task(
    description="基于研究员的要点写一段面向新手的介绍。",
    expected_output="200 字以内的中文介绍段落。",
    agent=writer,
    context=[t1],
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
