# -*- coding: utf-8 -*-
"""
实验2：Context Engineering —— LangChain 四操作 Write/Select/Compress/Isolate
场景：编码 agent 的历史里，早期塞了 8 条 v1 版 API 文档，后来用户切换到 v2。
一个"哪个词出现多就信哪个"的关键词策略（模拟注意力被历史带偏的模型）：
- 全量上下文（不 Select）：v1 出现次数多 -> 选中已废弃的 v1  -> 错
- 四操作处理：Select 只留切换后的消息 + Compress 把旧文档压成一行摘要 -> 选中 v2 -> 对
同时统计两种策略送给"模型"的 token 估算，验证"太多"和"太少"一样有害。
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HISTORY = [
    ("system", "你是编码助手。当前任务：给客户列表模块接数据源。"),
    ("tool_doc", "fetch_data_v1(url) 返回 JSON 列表。fetch_data_v1 支持分页。fetch_data_v1 已上线稳定。"),   # v1 文档1
    ("tool_doc", "fetch_data_v1 的错误码：404/500。fetch_data_v1 超时 30s。fetch_data_v1 示例见 wiki。"),     # v1 文档2
    ("tool_doc", "fetch_data_v1 返回字段 name/phone。fetch_data_v1 限频 10qps。fetch_data_v1 不可并发。"),     # v1 文档3
    ("tool_doc", "fetch_data_v1 需要 token。fetch_data_v1 走网关。fetch_data_v1 建议缓存 5 分钟。"),          # v1 文档4
    ("tool_doc", "fetch_data_v1 分页参数 page/size。fetch_data_v1 默认 20 条。fetch_data_v1 排序按 id。"),     # v1 文档5
    ("tool_doc", "fetch_data_v1 历史版本 changelog：v1.0 上线。fetch_data_v1 由平台组维护。fetch_data_v1 SLA 99.9。"),  # v1 文档6
    ("user",   "通知：平台已发布 fetch_data_v2，v1 下个月后下线，我们切换到 v2。"),
    ("tool_doc", "fetch_data_v2(url) 返回 JSON 列表，兼容 v1 用法，额外支持游标分页。"),                      # v2 文档（只有2条）
    ("tool_doc", "fetch_data_v2 的游标参数 cursor/limit，返回 next_cursor。"),
    ("user",   "好，请开始写调用代码。"),
]
CUTOFF = 7          # 第 8 条(索引7)起是切换之后（前 6 条 v1 文档 + 1 条系统提示）
KEY = "任务"

def tokens(msgs):
    return sum(len(t) + len(c) for t, c in msgs)   # 粗估：字符数即 token

def naive_pick(msgs):
    """无记忆策略：数 v1/v2 出现次数，谁多信谁 —— 模拟被历史淹没的注意力"""
    v1 = sum(c.count("v1") for _, c in msgs)
    v2 = sum(c.count("v2") for _, c in msgs)
    return ("fetch_data_v1" if v1 > v2 else "fetch_data_v2"), v1, v2

def four_ops(msgs):
    # Write：新事件照常追加（历史本身就是 Write 的产物）——这里体现为不丢 user 指令
    # Select：只留「切换之后」的消息 + 系统提示 + 最新 user 指令
    selected = [msgs[0]] + [m for i, m in enumerate(msgs) if i >= CUTOFF]
    # Compress：把被扔掉的 6 条 v1 文档压成一行带结论的摘要（只点名一次旧版接口）
    stale = [m for i, m in enumerate(msgs) if 0 < i < CUTOFF]
    compressed = ("tool_doc", f"[摘要] 历史 6 条细节已折叠：fetch_data_v1【即将下线】，"
                              f"仅作故障排查参考，新代码一律禁用。")
    # Isolate：把可能干扰主任务的 v1 细节隔离到子上下文（这里用摘要代替原文进主上下文）
    ctx = selected[:1] + [compressed] + selected[1:]
    return ctx, *naive_pick(ctx)[0:1], sum(c.count("v1") for _, c in ctx), sum(c.count("v2") for _, c in ctx)

if __name__ == "__main__":
    print("=" * 62)
    print("实验2：上下文工程四操作 Write/Select/Compress/Isolate")
    print("=" * 62)
    print(f"历史共 {len(HISTORY)} 条消息，其中 v1 文档 6 条、v2 文档 2 条、切换指令 1 条")
    print(f"全量上下文 token 估算：{tokens(HISTORY)}")
    pick, v1, v2 = naive_pick(HISTORY)
    print(f"\n【A. 不做处理（全量塞给模型）】v1 出现 {v1} 次 / v2 出现 {v2} 次")
    print(f"  关键词策略选中：{pick}  ->  {'❌ 选中下个月就下线的 v1，代码写完即报废' if 'v1' in pick else '✅'}")
    ctx, pick2, sv1, sv2 = four_ops(HISTORY)
    print(f"\n【B. 四操作处理后】Select 保留 {len([m for i,m in enumerate(HISTORY) if i>=CUTOFF])+1} 条 + Compress 压缩 1 条摘要 + Isolate 隔离 v1 细节")
    print(f"  送给模型的 token 估算：{tokens(ctx)}（降到 {tokens(ctx)*100//tokens(HISTORY)}%）")
    print(f"  摘要后 v1 出现 {sv1} 次 / v2 出现 {sv2} 次 -> 关键词策略选中：{pick2}")
    print(f"  -> {'✅ 选中 v2，正确' if 'v2' in pick2 else '❌'}")
    print("\n结论：上下文太少丢历史，太多则旧信息以数量优势『骗』过注意力；")
    print("      Write 管记录、Select 管筛选、Compress 管浓缩、Isolate 管隔离——四件事各司其职。")
