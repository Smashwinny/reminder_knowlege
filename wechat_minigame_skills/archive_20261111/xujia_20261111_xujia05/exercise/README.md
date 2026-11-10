# 拾光：原创方法层实验
不是Codex/微信/Higgsfield端到端复现。不安装技能、不用服务密钥、不联网联机或部署。
依赖：Python3、Node24、Chrome默认`/usr/bin/google-chrome`（可改browser.cjs）。
进入exercise目录：
```
npm ci --ignore-scripts --no-audit --no-fund
python3 audit.py
node lab.cjs replay
node lab.cjs boundaries
node lab.cjs feedback
node browser.cjs
```
可直接浏览器打开game.html操作。采用手动推进固定60tick/模拟秒，不是实时FPS演示。键盘左右或按钮每次推进一步。浏览器测试钩子advanceTime保留分数毫秒，render_game_to_text输出同一状态。原创core.js无浏览器依赖，复放600步输入固定。
source-manifest.json记录11个来源入口的固定SHA和下载结果，不代表宿主加载成功或全仓审阅；不捆绑上游代码和原始游戏素材。测试JSON与PNG写本目录。原创代码MIT许可。
