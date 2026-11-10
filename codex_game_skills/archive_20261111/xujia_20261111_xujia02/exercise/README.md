# 八技能交接教学练习（原创实现）

不需要账号、模型或GPU；Python3、Node.js 18+（structuredClone）、Google Chrome/Chromium用于最后页面实验。无npm依赖。参考固定一手来源见上级sources.md；未把第三方技能作为可执行代码加载。

## 一键复现
解压交付包，进入item02/exercise，运行：
```bash
python3 run_all.py
```
run_all.py默认命令google-chrome，可按环境将可执行文件替换为chromium。完整五步输出写回../experiment-log.md，QA写入../qa。每一步结果JSON保存在当前目录。

## 五步与目的
1. `python3 source_audit.py`：核对8个技能的头部name、40位固定SHA、本地SHA256；source-result.json。不是安装测试。
2. `node lab.mjs contracts`：胜利/失败、重复事件、非法HP、状态初始化与确定性摘要；contracts-result.json。
3. `node lab.mjs ui`：焦点屏幕栈与360×800、1280×720、2560×1080布局边界，无物理设备；ui-result.json。
4. `node lab.mjs feel`：墙钟截止、重叠命中、衰减与减弱动态；feel-result.json。不是引擎或主观试玩。
5. `python3 build_demo.py`：生成单文件demo.html；run_all随后用无头Chrome打开`demo.html?test=1`，真实执行三次拾取、重启、受伤并核验DOM和Canvas，保存截图。正常打开demo.html可手动体验。

本练习仅演示数据契约和反馈边界；不是完整平台游戏/碰撞引擎，不含Three.js模型、网络同步或生成美术。CONFIG.seed是预留配置，本实验没有随机数或固定步长渲染模拟，因此确定性只覆盖给定动作序列。seen数组为教学实现，正式项目需有界去重。

## 追溯
core.mjs对应game-design-theory的规则闭环、game-ui-ux的事件HUD、game-feel的trauma/双时钟防竞态；lab.mjs为原创验收用例。借鉴方法，不复制/执行第三方完整引擎。game-engine模板为Haxe式示例，未谎称直接运行它。第三方快照保留原作者声明；原创代码仅为可修改教学样例。

## 真实结果与待验证
见../experiment-log.md。没有证明Codex技能提效、性能达标或宿主支持。不得以本练习输出代替实际平台测试。

exercise.zip不附带无LICENSE上游代码；若上级sources缺少快照，source_audit.py会只读下载固定SHA原始SKILL.md进行核验，因此单独解压时第一步需联网。没有安装或执行下载内容。

## 本次验收状态
步骤1—4真实通过（合约8项断言）；步骤5生成demo.html成功，但Chrome多次超时，0项浏览器检查取得实证，未生成截图。PDF未渲染。run_all.py不会把页面生成成功伪装成浏览器运行成功。
