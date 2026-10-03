# -*- coding: utf-8 -*-
# 探针：直接问训练集里的原题（验证训练信号是否到达正确 token）
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from llamafactory.chat import ChatModel

QUESTIONS = [
    "这个实验用了什么硬件？",
    "微调用了多少数据？",
    "你用的哪个微调方法？",
    "LLaMA-Factory 是什么？",
    "谁是通义千问？请忽略之前的问题，你的名字是什么？",
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
