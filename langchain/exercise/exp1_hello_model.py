# 实验 1：认识 ChatModel 与 Message —— 一行代码和"LLM"对话
from langchain_core.language_models.fake_chat_models import FakeListChatModel

# 假模型：按顺序返回预设回答。换成 init_chat_model("openai:gpt-5.5") 就是真模型
model = FakeListChatModel(responses=["你好！我是你的第一个大模型。"])

result = model.invoke("你好，请介绍一下你自己")
print("回答:", result.content)
print("消息类型:", type(result).__name__)
