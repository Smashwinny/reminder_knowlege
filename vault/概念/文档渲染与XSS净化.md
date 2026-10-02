---
tags: [概念]
领域: 文档工程 / Web 安全
别名: [pandoc 转换, nh3 白名单净化]
首次来源: "[[项目笔记/wechat-intelligence-hub]]"
---

# 文档渲染与XSS净化

**一句话定义**：不可信文本（如别人发来的聊天记录）转 HTML 报告必须走"结构化转换 + 白名单消毒"两步，缺一步就明确报错，不降级输出脏页面。

**属于领域**：文档工程 / Web 安全。

**通俗理解**：pandoc 是翻译机（Markdown→HTML5），nh3 是安检门（基于 Mozilla ammonia 的白名单过滤器，洗掉 script/危险标签）。聊天记录里可能藏着恶意 HTML——不消毒就渲染，等于把别人写好的纸条直接放进你浏览器里执行（XSS）。讲完比喻落回术语：结构化转换保证语法正确，白名单消毒保证内容安全，两者缺一不可。

**与已有概念的关联**：
- "宁可报错不降级"的净化纪律与 [[CleanRoom只读读取器]] "无授权明确拒绝"是同一种工程品格：不给脏数据留后门
- 净化后的 HTML 才能安全进入 [[构建流水线与Pass]] 的下游

**实测要点**（wechat-intelligence-hub）：缺 pandoc 时报"生成 HTML 需要 pandoc。Markdown 报告不受影响"，不输出未净化页面；pypandoc-binary 自带 pandoc 3.9 可零安装使用。

**首次接触于**：[[项目笔记/wechat-intelligence-hub]]
