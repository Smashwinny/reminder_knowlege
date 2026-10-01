# 烟雾测试：不联网、不用 API key，验证 langchain v1 的 Agent 核心循环
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from langchain.agents import create_agent

class FakeToolChatModel(GenericFakeChatModel):
    """补上 bind_tools：真实模型会把工具清单交给服务商，假模型直接记住即可。"""
    def bind_tools(self, tools, **kwargs):
        self._bound = tools
        return self

@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

# 假模型：按脚本轮流返回"工具调用"和"最终回答"，模拟真实 LLM 的行为
model = FakeToolChatModel(messages=iter([
    AIMessage(content="", tool_calls=[{"name": "add", "args": {"a": 2, "b": 3}, "id": "t1"}]),
    AIMessage(content="2 + 3 = 5"),
]))

agent = create_agent(model, tools=[add])
result = agent.invoke({"messages": [{"role": "user", "content": "请计算 2+3"}]})
for m in result["messages"]:
    print(f"[{type(m).__name__}] {m.content}")
