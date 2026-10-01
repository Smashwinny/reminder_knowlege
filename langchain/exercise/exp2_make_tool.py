# 实验 2：认识 Tool —— 用 @tool 把普通函数变成"模型的工具"
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """查询指定城市的当前天气。

    Args:
        city: 城市名，例如"北京"
    """
    # 真实场景这里会调天气 API；演示就返回固定值
    return f"{city}：晴，26°C"

print("工具名:", get_weather.name)
print("给 LLM 看的说明书:", get_weather.description)
print("参数说明书:", get_weather.args_schema.model_json_schema())
print("直接调用结果:", get_weather.invoke({"city": "北京"}))
