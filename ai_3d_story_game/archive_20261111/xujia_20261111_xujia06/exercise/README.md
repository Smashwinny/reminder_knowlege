# 原创叙事状态+WebGL方法实验
不是作者的《龙珠·七星冒险》，原HTML未取得；不含其源码或IP素材。three固定0.170.0。
```
npm ci --ignore-scripts --no-audit --no-fund
python3 audit.py
node test.cjs graph
node test.cjs gates
node test.cjs route
python3 browser.py
```
browser.py启动临时localhost服务，调用/usr/bin/google-chrome CLI无头加载本次scene.html、截图和dump DOM，不读取用户浏览器会话。可在浏览器打开本地HTTP scene.html看几何球。story.cjs完整四节点是独立Node逻辑；scene.html只演示按钮/几何更换，未整合完整剧情。包里源码本次原创，MIT许可；依赖许可见npm包。没有FPS结论。
