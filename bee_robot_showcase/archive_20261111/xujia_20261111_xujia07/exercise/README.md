# Kestrel K-1 有界回归（原创学习脚本）

上游：Bee / thtbee，https://github.com/thtbee/waggles
固定SHA：286d56ccbbb924c10812fc5e6cabb11906454afc
上游许可CC BY-NC4.0：https://creativecommons.org/licenses/by-nc/4.0/
本练习是新增审计/测试脚本，不是机器人作者工程；取回原文件，内存HTTP响应中添加测试脚本，原index/bundle磁盘文件不改。上游字节不嵌入轻量ZIP。下载约15.7MB，无密钥、不付费、不自动安装依赖。

要求Python3、Node、/usr/bin/google-chrome（实际环境Chrome156.0.8078.47、Node24.22.1、Python3.13.5）。无npm依赖。

按顺序执行（初次需公共网络）：
```
python3 fetch.py
python3 assets.py
node clock.cjs
python3 browser.py studio
python3 browser.py explode
```

fetch结果逐项SHA256在download-manifest.json。与本包expected-manifest.json逐项比较，确认固定字节。assets-result.json只计四个外壳资源，不等于整机零件数。clock-result.json是从上游精确提取计时类的合成函数实验，不是性能测试。

browser.py只起临时localhost服务器，用Chrome命令行新建headless进程，不使用用户已登录浏览器。注入harness.js明确改变运行环境：阻断自主requestAnimationFrame调度，改由公开__robo API显式step/render；中间状态检查暂时抑制renderer.render，最终恢复真实renderer并绘制截图，便于确定性检查与避免软件渲染无限重绘。它不是普通交互会话，也不测FPS。若保留自主帧循环，原始1280x900/12s虚拟预算在本环境150秒内未完成；失败记录保留。

studio-result.json/explode-result.json、HTTP请求日志、DOM、stderr与PNG保存真实输出。截图的调试文字是新增仪表，不是原UI。错误、资源未就绪或断言失败会非零退出；不得把异常当通过。其它模式、物理真实性、硬件与付费生成待验证。

## 本次实际结论（必须先读）
最新browser两命令均非零退出：UI启动，成功GLB为0/4，reason=not ready，完整机器人画面未通过。不是“全套测试通过”。fallback-*保留较早的降级运行：29关节变化、4186对象移动、0复位残差；缺外壳且中间重绘被抑制，不能当完整模型验收。早期walkPhase字段读错，修正为原构建walkPhaseRad后因资产门槛失败未重新执行该步，因此步态冻结仍待验证。
线程HTTP服务器替换与30秒虚拟预算没有解决此问题；同源最小fetch诊断成功，根因尚不确定。原始失败记录在主交付日志。脚本保留严格非零退出，不自动忽略失败。
