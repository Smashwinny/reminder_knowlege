# Spec: topwords —— 文本词频统计小工具

## Problem Statement
工科学生拿到一段英文文本，想知道哪几个词出现最多，肉眼数不过来。

## Solution
一个命令行工具 `topwords.py`：读入文本文件，输出出现频率最高的 N 个词。

## User Stories
1. 作为学生，我想传入 txt 文件路径，所以能看到词频排行
2. 作为学生，我想用 -n 指定看前几个词，所以能控制输出长度
3. 作为学生，我想大小写不敏感计数（The 和 the 算同一个词），所以结果符合直觉

## Implementation Decisions
- 模块拆分：tokenize（分词）与 report（排序输出）两个函数，放在一个包里
- 分词规则：仅保留字母，小写化（ticket T1 决定接口，T2 依赖它）
- API 契约：tokenize(text) -> list[str]；report(words, n) -> list[tuple[str, int]]

## Testing Decisions
- 只测外部行为：给输入断言输出，不测内部实现
- ticket 完成标准：该 ticket 的测试全绿

## Out of Scope
- 停用词过滤、中文分词、UTF-8 以外的编码
