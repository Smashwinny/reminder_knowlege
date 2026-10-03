# -*- coding: utf-8 -*-
# 微调后验证：基座 + LoRA adapter 叠加，问与基线完全相同的问题
# 用法: USE_MODELSCOPE=1 ./venv/Scripts/python.exe exercise/after_chat.py
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from llamafactory.chat import ChatModel

QUESTIONS = [
    "你是谁？",
    "你叫什么名字？",
    "你是通义千问吗？",
    "用一句话总结你的来历",
    "你支持哪些语言？",
]

def main():
    chat_model = ChatModel({
        "model_name_or_path": "Qwen/Qwen2.5-1.5B-Instruct",
        "adapter_name_or_path": "exercise/saves/qwen25-lora-sft",
        "template": "qwen",
    })
    for q in QUESTIONS:
        messages = [{"role": "user", "content": q}]
        resp = chat_model.chat(messages)
        print(f"Q: {q}")
        print(f"A: {resp[0].response_text.strip()}")
        print("-" * 40)

if __name__ == "__main__":
    main()
