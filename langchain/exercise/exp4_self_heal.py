# 实验 4：Agent 的自我纠错 —— 工具报错后，框架把错误送回模型重试
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from langchain.agents import create_agent

class FakeToolChatModel(GenericFakeChatModel):
    def bind_tools(self, tools, **kwargs):
        return self

@tool
def divide(a: float, b: float) -> float:
    """计算 a 除以 b。"""
    if b == 0:
        raise ValueError("除数不能为 0，请换一个非零除数重试")
    return a / b

# 剧本：模型先犯错(除以0) -> 收到错误信息 -> 改参数重试 -> 成功回答
model = FakeToolChatModel(messages=iter([
    AIMessage(content="", tool_calls=[{"name": "divide", "args": {"a": 100, "b": 0}, "id": "t1"}]),
    AIMessage(content="", tool_calls=[{"name": "divide", "args": {"a": 100, "b": 4}, "id": "t2"}]),
    AIMessage(content="100 ÷ 4 = 25。"),
]))

agent = create_agent(model, tools=[divide])
result = agent.invoke({"messages": [{"role": "user", "content": "请计算 100 除以 4"}]})

print("=== 消息流 ===")
for m in result["messages"]:
    print(f"  [{type(m).__name__}] {repr(m.content)[:120]}")
