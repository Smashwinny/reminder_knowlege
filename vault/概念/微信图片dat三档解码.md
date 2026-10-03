---
tags: [概念]
领域: 数据安全 / 本地数据读取
别名: [微信dat三档解码, legacy XOR magic反推, V1固定AES, V2 AES+XOR]
首次来源: "[[项目笔记/wx_cli_again]]"
---

# 微信图片dat三档解码

**一句话定义**：微信聊天图片以 `.dat` 文件加密存储，历史上用过三代方案，读取工具必须按文件头 magic 分发到三档解码器：legacy 单字节 XOR（无 magic，靠已知图片格式头反推 key）、V1 固定 AES-128-ECB（硬编码 key `cfcd208495d565ef` = md5("0")[:16]）、V2 AES+XOR 三段拼接（AES key 平台派生）。

**属于领域**：本地加密媒体文件的格式逆向与兼容读取。

**通俗理解**：同一个衣柜换了三代的锁。最早是"挂锁"（XOR 一个字节，钥匙就在锁孔边上——拿已知 magic 一试就出来）；第二代是"统一配发的钥匙"（所有文件同一把固定 AES key，写在源码里）；第三代是"每人一把的钥匙"（AES key 从 uin/wxid 派生，还得配合一段明文 raw 段和一段 XOR 尾段拼起来）。讲完比喻落回术语：`.dat` 头部 6 字节 magic（`07 08 V1/V2 08 07`）是分发的开关，无 magic 旧文件用"密文[0] ⊕ 已知格式头[0] = key，再验 magic 剩余字节"反推，按 magic 长度降序试探（PNG 4 字节优先于 JPG 3 字节）防假阳性；BMP 仅 2 字节 magic 需额外校验文件头 `bf_size`/`bf_offset` 合理性。

**与已有概念的关联**：
- 读取对象是 [[进程取钥与副本解密]] / [[CleanRoom只读读取器]] 同款"微信本地数据"，但攻的不是数据库整库加密（SQLCipher），而是附件文件的历代格式加密
- V2 的 image AES key 提取（macOS kvcomm cache + uin 暴力枚举 / Windows 扫 WeChat.exe 内存）与 [[进程取钥与副本解密]] 同属"从活进程/周边缓存取钥"家族
- 本批次实验（[[项目笔记/wx_cli_again]]）：上游真实 decoder 源码 + 合成 87 字节 PNG 往返 legacy_xor / v1_aes 全过，全零垃圾/空文件/缺 key 三负向全拒

**首次接触于**：[[项目笔记/wx_cli_again]]
