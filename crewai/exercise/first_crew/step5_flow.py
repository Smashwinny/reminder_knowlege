# -*- coding: utf-8 -*-
"""第五步实验：Flow —— 确定性的事件驱动流水线（对比 Crew 的自治）
运行: .venv/Scripts/python step5_flow.py
"""
import os

os.environ.setdefault("CREWAI_TELEMETRY_OPT_OUT", "true")

from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel


class AppState(BaseModel):
    topic: str = ""
    draft: str = ""


class WritingFlow(Flow[AppState]):

    @start()
    def receive_topic(self):
        self.state.topic = "crewAI 与 LangGraph 的区别"
        print(f"[start] 收到题目: {self.state.topic}")
        return self.state.topic

    @listen(receive_topic)
    def write_draft(self, topic: str):
        # Flow 里可以直接放"确定性代码"，不必事事问 LLM
        self.state.draft = f"《{topic}》写作大纲：1. 定位差异 2. 心智模型 3. 选型建议"
        print(f"[listen] 大纲已生成（纯 Python，零 token）")
        return self.state.draft

    @listen(write_draft)
    def polish(self, draft: str):
        print(f"[listen] 拿到大纲，这里可以再接一个 Crew 做 LLM 润色")
        return draft + "（本步为占位，未调用 LLM）"


flow = WritingFlow()
final = flow.kickoff()
print("\nFlow 最终输出:", final)
