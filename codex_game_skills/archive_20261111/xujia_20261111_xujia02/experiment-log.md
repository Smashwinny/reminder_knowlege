# 五步真实实验日志

2026-11-11T01:16:01.383832+08:00（Asia/Shanghai）
原创JS教学实现，不是Codex/引擎/平台端到端成功。此前Chrome无头启动分别45s、30s、25s超时；PDF命令也未生成文件。

## 步骤1 已执行
工作目录：解压后的item02/exercise
```bash
python3 source_audit.py
```
真实输出：
```text
{"skills_verified": 8, "all_current_path_reads": true, "installed_skills": 0, "model_calls": 0}

exit_code=0
```

## 步骤2 已执行
工作目录：解压后的item02/exercise
```bash
node lab.mjs contracts
```
真实输出：
```text
{"checks":8,"win":"WIN","lose":"LOSE","score_events":3,"duplicate_rejected":true,"invalid_hp_rejected":true,"replay_hash":"171d176076837f6e36ee0c878bdb1f022da83c50de4a4b155679c22b6d33cc33"}

exit_code=0
```

## 步骤3 已执行
工作目录：解压后的item02/exercise
```bash
node lab.mjs ui
```
真实输出：
```text
{"focus_stack":"game→pause→settings→pause→game","viewports":[{"w":360,"h":800,"inset":16,"pause_target":44,"overlap":false},{"w":1280,"h":720,"inset":16,"pause_target":44,"overlap":false},{"w":2560,"h":1080,"inset":16,"pause_target":44,"overlap":false}],"note":"geometry assertions, not physical device/gamepad tests"}

exit_code=0
```

## 步骤4 已执行
工作目录：解压后的item02/exercise
```bash
node lab.mjs feel
```
真实输出：
```text
{"overlap_restore_at":0.11,"old_deadline_still_frozen":true,"new_deadline_restored":true,"reduced_motion_offset":0,"trauma_after_2s":0,"simulation_mutation":false,"note":"original JS adaptation; not Godot/Unity runtime and not subjective playtest"}

exit_code=0
```

## 步骤5 已执行（仅页面生成；浏览器执行见下）
工作目录：解压后的item02/exercise
```bash
python3 build_demo.py
```
真实输出：
```text
built demo.html: inline shared core, no dependencies

exit_code=0
```

## 步骤5浏览器部分：运行待验证
```bash
google-chrome --headless --disable-extensions --no-first-run --disable-gpu --disable-dev-shm-usage --user-data-dir=/workspace/xujia-batch/item02/qa/final-demo-profile --window-size=1100,800 --screenshot=/workspace/xujia-batch/item02/qa/demo.png --dump-dom file:///workspace/xujia-batch/item02/exercise/demo.html?test=1
```
结果：exit_code=124；timeout=15秒；没有取得有效自测DOM或截图，浏览器部分受阻/待验证。
不得将build_demo成功当成网页运行成功；源代码内自测的预期结果不是实测。

## 待验证
Codex宿主8技能加载、Unity/Unreal/Godot适配、Three.js/移动/手柄、真人试玩与Higgsfield生成部署均未执行。
没有账号、密钥、付费模型、外发或公开部署；没有FPS/提效百分比结论。
主实验步骤1—4本地真实通过；步骤5文件生成通过，Chrome执行失败。
PDF：无头Chrome未生成guide.pdf，标未渲染；没有PDF逐页图像，不能声称视觉验收通过。
参考排查：官方https://developer.chrome.com/docs/chromium/headless确认headless用法；一次公开网页检索及X检索未找到可直接验证的安全修复。未修改代理/系统安全配置/其他助手会话。