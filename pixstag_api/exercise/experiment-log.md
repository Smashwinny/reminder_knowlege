# PixStag API · 实验日志（task e55165e3-957e-42dd-9cde-523cd6a5b663）

实验日期：2026-10-27
性质：接口契约学习 + 本地模拟验证。未充值、未创建真实生成任务（POST 创建任务需本人授权，已按规则不执行）。

## 步骤与真实输出

### 步骤 1：官方 API 文档直读（pixstag.com/docs/api）

- 端点：POST /api/v2/video_generation（创建）、GET /api/v2/query/video_generation/{task_id}（查询）、GET /api/v2/user/me
- 认证：Authorization: Bearer <token>
- 异步五态：queued / running / succeeded / failed / cancelled；支持 callback_url  webhook（最多 3 次通知）
- 输入契约：model（MiniMax-H3 / doubao-seedance-2 / 2-5）、duration 4–30 秒整数、ratio、resolution（720P–2K）
- 多模态 content 数组：text（必填非空 ≤5000 字，**"不用自己想提示词"≠底层无提示词**）、
  image_url/audio_url/video_url + role（first_frame/last_frame/reference_*）；图/音 ≤3MB、视频 ≤5MB
- 成功响应带 usage：total_seconds/input_seconds/output_seconds/各 token 计数——**按秒计量**
- user/me 返回 credit / credit_frozen / credit_valid_time（积分有有效期）

### 步骤 2：真实只读探针（无 token GET /user/me）

```
HTTP 401: login fail: Please carry the API secret key in the 'Authorization' field (1004)
```
✅ 错误契约与文档一致（code 1004）；未越权执行任何写操作。

### 步骤 3：客户端骨架 + 状态机 + 对账模拟（pixstag_client_sim.py）

```
① 真实 401 探针断言通过
② 状态机：本地假服务端 queued→running→succeeded，3 轮轮询到达终态 ✅
③ 用量对账：请求 6s vs 计费 6s → ✅ 一致；篡改 8s → ❌ 拒付复核 ✅
```

## 结论

- 接口是标准的"创建即返回 task_id + 轮询 + 可选 webhook"异步契约，五态齐全；
- **按秒计费 + 积分有效期**意味着"1 块钱做视频"要核算：时长×单价×失败重试×积分过期；
- 多模态 role 设计（first/last frame、reference 三类）与 [[角色一致性锚定]] 的参考图注入一脉相承；
- 未验证：真实生成质量/速度/账单（需充值授权）。

## 产物

- `exercise/pixstag_client_sim.py` — 客户端骨架 + 状态机 + 对账（含真实 401 探针）
- `exercise/experiment-log.md`（本文件）
