# Mesh Avatar 文件层离线实验

输入 avatar/ 为本次程序化自绘的256×256几何头像，CC0-1.0，不含Miko或第三方插画。分层与rig是教学夹具，不是 Agent 自动识图结果。

在 item16 目录执行：
```bash
npm install --prefix exercise/runtime --ignore-scripts --no-audit --no-fund mesh-avatar@0.7.2
node exercise/lab.mjs version
node exercise/lab.mjs validate
node exercise/lab.mjs pack
node exercise/lab.mjs negative
```

runtime/package-lock.json 锁定包和完整性；ZIP 不含 node_modules，需要按上面命令重新安装。完整源码定位见 sources.md，npm包为上游MIT运行库。

validateAvatarFiles不解码图像、不做IO。没有WebGL/编辑器/嘴型/摄像头或语音实测。preflight-notes.md保留初次view边距单位错误。demo.html仅为未执行的候选加载入口，不代表网页已运行。
