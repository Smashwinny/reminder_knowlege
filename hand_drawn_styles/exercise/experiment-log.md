# hand-drawn-styles 动手实验日志（task 8e674041-e9f2-4aba-be1f-4b614d670696）

实验日期：2026-10-27
环境：Windows 11，Python（仓库要求 3.10+，本机 Python 3.14），零第三方依赖
上游：threerocks/hand-drawn-styles，main @ 5a2f91f（浅克隆）

## 实验设计

该项目是"手绘风格提示词配方库"（自称不生图，只输出 prompt / JSON 调用包）。
验证三件事：①配方真源（STYLES.md）能否被脚本原样提取；②编号/中文名/别名三种路由是否都通；
③占位符缺省时是否"fail-closed"（宁可报错也不输出半成品 prompt）。

## 步骤与真实输出

### 步骤 1：克隆 + 完整性自检

```
git clone --depth 1 https://github.com/threerocks/hand-drawn-styles repo   # HEAD 5a2f91f
python scripts/check_skill.py
```
✅ 输出：`pass: 23 套配方, 116 个别名, 23 项完整调用`

### 步骤 2：水墨风渲染（零占位符风格）

```
python scripts/render_prompt.py --style ink-wash --subject "一只鸟停在细枝上" --aspect 3:4
```
✅ 输出完整中文 prompt：生宣纸质感、"墨分五色"（焦浓重淡清）、飞白枯笔、留白构图、
朱红印章、"严禁：照片写实、3D、均匀灰度滤镜……"负向清单。配方提取自 STYLES.md，未走样。

### 步骤 3：三种路由方式

- `--style ink-wash`（英文别名）✅
- `--style 9`（编号，像素风）✅（见步骤 4 首次报错后补全渲染成功）
- `--style crayon`（英文别名）✅

### 步骤 4：fail-closed 占位符机制（重要发现）

```
python scripts/render_prompt.py --style 9 --subject "一只猫在屋顶"
→ render_prompt: 缺少占位符: 主色调            ← 拒绝输出半成品！
python scripts/render_prompt.py --style crayon --subject "..." --var 主色调=暖黄
→ render_prompt: 缺少占位符: 主色调, 标题词     ← 逐项报出缺哪个槽
python scripts/render_prompt.py --style no-such-style --subject x
→ render_prompt: STYLES.md 中不存在画风 no-such-style 的代码块配方
```
✅ 未知画风 / 缺槽位都明确报错，不输出残次 prompt。

### 步骤 5：补齐槽位后的完整渲染

```
python scripts/render_prompt.py --style pixel-art --subject "一只猫在屋顶" --var 主色调=深蓝
```
✅ 完整英文 prompt：8-bit/16-bit sprite、硬边像素阶梯、无抗锯齿、8~16 色限定调色板、
dithering 棋盘点阵代替渐变。

```
python scripts/render_prompt.py --style crayon --subject "爸爸教我骑自行车" --var 主色调=暖黄 --var 标题词=成长
```
✅ 英文 prompt 开头即负向锚定："A drawing made by a real 5-year-old child …
NOT made by an artist. It should look clumsy, messy, and 'bad' on purpose."

## 结论

- 23 套配方 / 116 个别名全部可路由，自检脚本通过；
- 渲染器从 STYLES.md 原样提取配方，输出含正向社会化描述+负向"严禁"清单的完整 prompt；
- **占位符 fail-closed**：缺槽位宁可报错也不交付半成品——与知识库 [[质检Gate与自我纠错循环]] 精神一致；
- 画风 3.1/19/20/22 需参考锚图并输出 JSON 调用包（本实验未下载锚图，未验证该路径）。

## 产物

- `exercise/experiment-log.md`（本文件）
- `repo/` 上游克隆（.gitignore 排除）
