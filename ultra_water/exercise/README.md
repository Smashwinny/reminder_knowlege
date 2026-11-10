# Ultra-Water：五步复现实验

先安装官方 Git 和 Node（Node 满足 ^20.19.0 或 >=22.12.0）。本次实际使用 Node24.21.0/npm11.19.0。把本压缩包内容放在 ultra_water/exercise，repo与exercise同级。路径可替换成自己的目录；已有repo不要覆盖，先核对版本和干净状态。

## 1. 取得并锁定源码
```powershell
New-Item -ItemType Directory -Force F:\reminder\ultra_water | Out-Null
Set-Location F:\reminder\ultra_water
# 仅首次、没有repo时运行clone：
git clone https://github.com/Humpalumps/Ultra-Water.git repo
git -C repo checkout --detach 30ea65ecb0a66b137aa200d099965634bdd84d51
git -C repo rev-parse HEAD
git -C repo status --short
node --version
npm --version
```
目的：绑定来源与运行环境。实际结果：固定SHA相符、原仓库tracked文件无改动。验证：上述SHA逐字相同、status为空；不要在已有他人改动上强制检出。

## 2. 安装锁定依赖并构建
```powershell
Set-Location F:\reminder\ultra_water\repo
npm.cmd ci --ignore-scripts --no-audit --no-fund
if ($LASTEXITCODE -ne 0) { throw 'npm ci failed' }
npm.cmd run build
if ($LASTEXITCODE -ne 0) { throw 'build failed' }
Get-Item .\dist\index.html,.\dist\licenses.md,.\dist\THIRD_PARTY_NOTICES.md
```
目的：真实执行锁定工程。实际结果：安装17包、构建32模块，退出0；主JS751.48KB触发体积提示。验证：产物和许可文件存在。关闭audit不代表无漏洞。

## 3. 执行上游JS及边界检查
```powershell
Set-Location F:\reminder\ultra_water
node --check .\exercise\verify-ocean.mjs
node .\exercise\verify-ocean.mjs
if ($LASTEXITCODE -ne 0) { throw 'verification failed' }
```
目的：直接执行上游参数常量、JONSWAP函数，核对边界。实际结果：检查01–07通过，非法风速/fetch记录非有限值；不会把JSON null当有效0。验证：前7项PASS；第03项只是源码结构字符串检查，不是update动态执行。

## 4. CPU数值独立对照
```powershell
node .\exercise\verify-ocean.mjs 2>&1 | Tee-Object .\exercise\verification-output-reproduced.txt
if ($LASTEXITCODE -ne 0) { throw 'verification failed' }
```
目的：CPU解释GLSL与独立二维DFT对照，同时测试色散、pack2、Hermitian和固定J泡沫样例。实际结果：14/14 PASS；N4/N8误差约3.95e-15/1.72e-14。验证：输出中出现SUMMARY checks=14 status=PASS gpu=NOT_TESTED且进程退出0。该结果不是GPU shader、256×1024图集隔离、fp16或MRT正确性的证明；泡沫两条路径均饱和到J=0.8，不能推断动态泡沫正确。原始失败与oracle修正保留于experiment-log.txt。

## 5. 真实浏览器单参数对照
```powershell
Set-Location F:\reminder\ultra_water\repo
npm.cmd run dev -- --host 127.0.0.1 --port 5187 --strictPort
```
打开 http://127.0.0.1:5187/ 。保持Lagoon；展开Water，将caustics从1改0并回车，再恢复1；最后camera选Underwater。
目的：确认光学通道有可见效果。实际结果：1时沙底有网状亮纹，0时亮纹消失但沙纹/波浪保留；恢复后水下焦散可见。验证：输入值与画面一致。时间继续流动，不是同一时刻像素差分。
另点击一次Run benchmark，UI报告2.38ms/frame、GPU2.34ms；暂停常规循环后连续推进300帧，非冻结画面、非跨硬件保证，未独立捕获disjoint。完整配置/计时见browser-experiment-evidence.txt。

## 证据与许可
原实跑Shell为Git Bash；本文列对应PowerShell复现命令，CLI结果记录在experiment-log.txt与verification-output.txt。浏览器操作由协调者实做，截图在对话工具证据中已查看，本包不包含截图文件。CPU翻译参照上游MIT源码，保留UPSTREAM-LICENSE.txt及THIRD_PARTY_NOTICES.md；完整上游代码通过固定SHA获得，不把node_modules打包。
