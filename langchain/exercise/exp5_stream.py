# 实验 5：流式输出 —— 像 ChatGPT 打字机一样一个词一个词蹦出来
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel

model = GenericFakeChatModel(messages=iter(["Hello world this is streaming"]))

print("流式输出: ", end="")
for chunk in model.stream("讲一句话"):
    print(chunk.content, end="", flush=True)
print("\n共收到", "多个", "AIMessageChunk 片段")
