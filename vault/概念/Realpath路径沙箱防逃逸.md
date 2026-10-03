---
tags: [概念]
领域: AI Agent / 安全沙箱
别名: ["路径沙箱", "realpath sandbox", "符号链接逃逸防护", "虚拟路径映射"]
首次来源: "[[项目笔记/chat-on-steroids]]"
---

# Realpath路径沙箱防逃逸

**一句话定义**：AI 文件工具的路径 containment 方案——模型只见虚拟路径（如 /project/src/main.ts），宿主把它映射到真实路径时先做 `fs.realpath` 规范化、再与规范化后的批准根目录做前缀比对，符号链接/NTFS junction/reparse point 穿出根目录即拒绝。

**属于领域**：AI Agent / 安全沙箱（[[沙箱与审批正交]] 中"路径边界"的具体实现；[[MCP服务器]] 文件类工具的地基）

**通俗理解**（比喻/例子，讲完落回术语）：像**酒店房卡**——房卡写着"1208 房"（虚拟路径），真正开门时系统查的是这把钥匙物理能开哪扇门（realpath 真实路径）。关键陷阱：批准目录里被种一个指向外部的符号链接（如 /project/link → C:\Users），按"路径字符串前缀"判断就上当了——/project/link 开头看着合规，实际落点在外面。对策是**永远先 realpath 解析出物理路径再比对**：跟着链接走没问题，只要落点仍在根目录内就放行。chat-on-steroids 的设计哲学一句话：**"Enforcement lives here, in code. It is never delegated to prompt text."（约束写在代码里，绝不写在提示词里）**——提示词可被注入、可被遗忘，代码不会。Windows 还有两个专门补丁：大小写不敏感的路径身份归一（toLowerCase）、WSL 的 \\wsl.localhost 路径别名处理。

**与已有概念的关联**：
- [[沙箱与审批正交]]：路径沙箱是静态边界，审批是动态放行，两者正交
- [[AgentHarness智能体挽具]]："最小权限工具"职责的文件系统版
- [[Checkpoint存档与持久执行]]：虚拟路径映射表也需要持久化，重启后同一虚拟路径要解析到同一真实路径
- [[本地MCP端点安全四道门]]：同一项目里"谁能连"（门）与本概念"连上后能碰哪"（沙箱）构成完整纵深

**首次接触于**：[[项目笔记/chat-on-steroids]]（src/main/sandbox.ts）
