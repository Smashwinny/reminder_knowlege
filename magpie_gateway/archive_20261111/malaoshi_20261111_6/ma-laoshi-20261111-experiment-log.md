# 真实实验日志（仅云端回环HTTP）
- 日期：2026-11-11（北京时间，Asia/Shanghai）
- 代码：exercise/ma-laoshi-20261111-gateway.py 与 ma-laoshi-20261111-test_gateway.py。
- 未运行magpie/Kiro；未读用户环境、密钥或账号；没有付费模型API；使用Python标准库与两个临时回环服务。
- 合成计数不是实际tokenizer/credits/账单。4个测试分组和编译均退出0。
- 可复现：解压exercise.zip，在解压目录按HTML中5步命令顺序运行；测试自行起停监听。

## 实际标准输出（完整）
```text
2026-11-11 01:28:18 Asia/Shanghai
$ python3 -m py_compile ma-laoshi-20261111-gateway.py ma-laoshi-20261111-test_gateway.py
compile exit=0
$ python3 ma-laoshi-20261111-test_gateway.py text
{"request": {"model": "study/fast", "max_tokens": 16, "messages": [{"role": "user", "content": [{"type": "text", "text": "hello"}, {"type": "text", "text": "world"}]}], "system": [{"type": "text", "text": "be brief"}]}, "status": 200, "response": {"id": "msg_study_mock", "type": "message", "role": "assistant", "model": "study/fast", "content": [{"type": "text", "text": "mock answer"}], "stop_reason": "end_turn", "stop_sequence": null, "usage": {"input_tokens": 4, "output_tokens": 2}}}
PASS system/text-block conversion + max_tokens + response contract
SEEN_UPSTREAM [{"model": "mock-fast-v1", "messages": [{"role": "system", "content": "be brief"}, {"role": "user", "content": "hello\nworld"}], "max_tokens": 16}]
PASS CASE text
CLEANUP listeners closed
exit=0
$ python3 ma-laoshi-20261111-test_gateway.py routes
{"request": {"model": "study/fast", "max_tokens": 16, "messages": [{"role": "user", "content": "hello world"}]}, "status": 200, "response": {"id": "msg_study_mock", "type": "message", "role": "assistant", "model": "study/fast", "content": [{"type": "text", "text": "mock answer"}], "stop_reason": "end_turn", "stop_sequence": null, "usage": {"input_tokens": 2, "output_tokens": 2}}}
PASS actual upstream observed: mock-fast-v1
{"request": {"model": "study/deep", "max_tokens": 16, "messages": [{"role": "user", "content": "hello world"}]}, "status": 200, "response": {"id": "msg_study_mock", "type": "message", "role": "assistant", "model": "study/deep", "content": [{"type": "text", "text": "mock answer"}], "stop_reason": "end_turn", "stop_sequence": null, "usage": {"input_tokens": 2, "output_tokens": 2}}}
PASS actual upstream observed: mock-deep-v1
PASS upstream header is different from client-visible alias
SEEN_UPSTREAM [{"model": "mock-fast-v1", "messages": [{"role": "user", "content": "hello world"}], "max_tokens": 16}, {"model": "mock-deep-v1", "messages": [{"role": "user", "content": "hello world"}], "max_tokens": 16}, {"model": "mock-fast-v1", "messages": [{"role": "user", "content": "hello world"}], "max_tokens": 16}]
PASS CASE routes
CLEANUP listeners closed
exit=0
$ python3 ma-laoshi-20261111-test_gateway.py usage
{"request": {"model": "study/fast", "max_tokens": 16, "messages": [{"role": "user", "content": "hello world"}]}, "status": 200, "response": {"id": "msg_study_mock", "type": "message", "role": "assistant", "model": "study/fast", "content": [{"type": "text", "text": "mock answer"}], "stop_reason": "end_turn", "stop_sequence": null, "usage": {"input_tokens": 2, "output_tokens": 2}}}
{"request": {"model": "study/deep", "max_tokens": 16, "messages": [{"role": "user", "content": "hello world"}]}, "status": 200, "response": {"id": "msg_study_mock", "type": "message", "role": "assistant", "model": "study/deep", "content": [{"type": "text", "text": "mock answer"}], "stop_reason": "end_turn", "stop_sequence": null, "usage": {"input_tokens": 2, "output_tokens": 2}}}
METER {"input_units": 4, "output_units": 4, "rejected": 0, "success": 2, "upstream_attempts": 2}
PASS 2 requests, 4 synthetic input + 4 output units; NOT credits or billing
SEEN_UPSTREAM [{"model": "mock-fast-v1", "messages": [{"role": "user", "content": "hello world"}], "max_tokens": 16}, {"model": "mock-deep-v1", "messages": [{"role": "user", "content": "hello world"}], "max_tokens": 16}]
PASS CASE usage
CLEANUP listeners closed
exit=0
$ python3 ma-laoshi-20261111-test_gateway.py errors
{"request": {"model": "not-real", "max_tokens": 16, "messages": [{"role": "user", "content": "hello world"}]}, "status": 404, "response": {"type": "error", "error": {"type": "study_error", "message": "unknown model"}}}
{"request": {"model": "study/fast", "max_tokens": 16, "messages": [{"role": "user", "content": "hello world"}], "stream": true}, "status": 501, "response": {"type": "error", "error": {"type": "study_error", "message": "stream not implemented"}}}
{"request": {"model": "study/fast", "max_tokens": 16, "messages": [{"role": "user", "content": "hello world"}], "tools": []}, "status": 400, "response": {"type": "error", "error": {"type": "study_error", "message": "unsupported field; no silent dropping"}}}
{"request": {"model": "study/fast", "max_tokens": 16, "messages": [{"role": "user", "content": [{"type": "image", "source": {}}]}]}, "status": 400, "response": {"type": "error", "error": {"type": "study_error", "message": "only string/text blocks supported"}}}
{"request": {"model": "study/fast", "max_tokens": 0, "messages": [{"role": "user", "content": "hello world"}]}, "status": 400, "response": {"type": "error", "error": {"type": "study_error", "message": "max_tokens must be positive integer"}}}
{"request": {"model": "study/fast", "max_tokens": 16, "messages": []}, "status": 400, "response": {"type": "error", "error": {"type": "study_error", "message": "nonempty messages required"}}}
PASS 6 local rejections, zero upstream attempts
{"request": {"model": "study/fast", "max_tokens": 16, "messages": [{"role": "user", "content": "__fail503__"}]}, "status": 502, "response": {"type": "error", "error": {"type": "upstream_error", "message": "local mock returned 503"}}}
PASS injected mock 503 maps to 502, no success usage; dummy credential rejected
SEEN_UPSTREAM [{"model": "mock-fast-v1", "messages": [{"role": "user", "content": "__fail503__"}], "max_tokens": 16}]
PASS CASE errors
CLEANUP listeners closed
exit=0

```
## 研究阶段失败记录
- 首次使用 `python` 提取网页：`python: command not found`，退出127；使用 `python3`重跑成功。
- WebFetch原帖403，随后普通公开curl200，正文实际可读。
- Kiro /terms-of-service/ 404；/docs/cli/acp/ 403，未作为已读政策证据。
- 上述为工具返回的真实失败，不是额度耗尽提示；本worker没有收到可引用的“配额耗尽”原文。

## 验证边界
这是真HTTP往返，但不是模型推理。没有运行SSE/工具、多模态、缓存、产品GUI、真实账户端点或性能评测。安全边界是本练习的固定回环地址与不读凭证设计，不是操作系统级网络隔离或完整生产安全保证。
