# 实验 3：认识 Agent Loop —— create_agent 组装"模型+工具"的自动循环
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from langchain.agents import create_agent

class FakeToolChatModel(GenericFakeChatModel):
    """假模型需要补 bind_tools（真实模型会把工具清单交给服务商）。"""
    def bind_tools(self, tools, **kwargs):
        return self

@tool
def add(a: int, b: int) -> int:
    """计算两个整数的和。"""
    return a + b

# 剧本：第 1 轮模型决定调用工具，第 2 轮模型看到结果后给出最终回答
model = FakeToolChatModel(messages=iter([
    AIMessage(content="", tool_calls=[{"name": "add", "args": {"a": 128, "b": 64}, "id": "t1"}]),
    AIMessage(content="128 + 64 = 192。"),
]))

agent = create_agent(model, tools=[add])
result = agent.invoke({"messages": [{"role": "user", "content": "请帮我计算 128+64"}]})

print("=== Agent 内部消息流（共 %d 条）===" % len(result["messages"]))
for i, m in enumerate(result["messages"]):
    extra = f" -> 请求调用工具 {m.tool_calls}" if getattr(m, "tool_calls", None) else ""
    print(f"  {i+1}. [{type(m).__name__}] {m.content}{extra}")
