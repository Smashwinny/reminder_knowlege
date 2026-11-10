# 原创作品集实验
这是方法层替身，不是 WorkBuddy/Step 或真实3D生成复现。无账户、网络服务或上游组件源码。
环境：Python3、Node24、Chrome。`test.cjs`的Chrome路径默认为`/usr/bin/google-chrome`。
解压进入exercise后：
```
npm ci --ignore-scripts --no-audit --no-fund
python3 audit.py
node test.cjs baseline
node test.cjs responsive
node test.cjs interaction
node test.cjs reduced
```
第2步期望检测到缺陷（360px里1100px宽），不是“页面修复失败”。其余测试验证响应式、键盘筛选、悬停、reduce降级。JSON/PNG写当前目录。原型文件同时包含`?v=before`缺陷对照与默认修复态。
不提供用户效果或性能结论。原创代码以MIT许可提供；上游链接见sources.md，未捆绑上游代码。
