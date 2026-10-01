# 实验 4：Agent 的自我纠错 —— 模型传错参数，框架自动把错误送回模型重试
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from langchain.agents import create_agent

class FakeToolChatModel(GenericFakeChatModel):
    def bind_tools(self, tools, **kwargs):
        return self

@tool
def divide(a: float, b: float) -> float:
    """计算 a 除以 b。b 必须是数字。"""
    return a / b

# 剧本：模型第一次手滑把除数传成字符串 -> 收到报错 -> 改对重试 -> 成功
model = FakeToolChatModel(messages=iter([
    AIMessage(content="", tool_calls=[{"name": "divide", "args": {"a": 100, "b": "zero"}, "id": "t1"}]),
    AIMessage(content="", tool_calls=[{"name": "divide", "args": {"a": 100, "b": 4}, "id": "t2"}]),
    AIMessage(content="100 ÷ 4 = 25"),
]))

agent = create_agent(model, tools=[divide])
result = agent.invoke({"messages": [{"role": "user", "content": "请计算 100 除以 4"}]})

print("=== 消息流（注意第 3 条：错误如何被送回模型）===")
for m in result["messages"]:
    print(f"  [{type(m).__name__}] {repr(m.content)[:150]}")
