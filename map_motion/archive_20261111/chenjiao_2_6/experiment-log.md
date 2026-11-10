# 真实离线实验日志

执行日期 2026-11-11 01:20:21 北京时间 UTC+8

均为自编教学夹具；第6项调用上游geo.py。合成数据不代表生产服务实测。

## 1. distance
```bash
cd /workspace/chen-jiao-batch2-20261111/item06
python3 exercise/lab.py distance
```
退出码 0
```text
upstream hav equator 1 degree: 111.1949266 km; spherical not road distance

```
## 2. roundtrip
```bash
cd /workspace/chen-jiao-batch2-20261111/item06
python3 exercise/lab.py roundtrip
```
退出码 0
```text
Mercator roundtrip max degree error= 1.4210854715202004e-14

```
## 3. angles
```bash
cd /workspace/chen-jiao-batch2-20261111/item06
python3 exercise/lab.py angles
```
退出码 0
```text
350->10 midpoint= 360.0 degrees (wrap=0); easing clamped endpoints PASS

```
## 4. frames
```bash
cd /workspace/chen-jiao-batch2-20261111/item06
python3 exercise/lab.py frames && ffmpeg -y -hide_banner -loglevel error -framerate 24 -i exercise/frame-%03d.png -c:v libx264 -pix_fmt yuv420p exercise/synthetic-route.mp4 && ffprobe -v error -show_entries format=duration -of default=nw=1 exercise/synthetic-route.mp4
```
退出码 0
```text
upstream geo.dive/frame generated= 48 frames; last= [121.4737, 31.2304, 12.0, 45.0, 10.0, 0] ; drawn path is synthetic, no map tiles/DEM fetched
duration=2.000000

```

## 逐步目的和验证
- 步骤1 调用上游距离公式：目的 使用已知球面几何作回归基准。；验证 赤道1度=111.1949266km，不是道路里程。
- 步骤2 调用上游投影往返：目的 检测常规纬度下经纬度保真。；验证 最大角度误差1.4210854715202004e-14。
- 步骤3 角度与缓动端点：目的 验证跨零最短插值及钳位。；验证 350→10中点360度，缓动两端PASS。
- 步骤4 相机时间轴与示意MP4：目的 真实调用dive/frame，合成帧后编码。；验证 48帧，最终坐标锁定输入；2秒MP4，不是官方完整地图渲染。

## 未验证边界
未调用高德、OSM查询、SRTM下载、真实轨迹、官方渲染器或模型Agent；示意MP4只有合成线段，不是地图成片；无地理数据授权验证。

## PDF机器检查
Chromium真实打印A4，pdftoppm渲染9页；DOM溢出检查：[]。等待逐页视觉自查；不等于独立审核。


## PDF逐页自查结论
2026-11-11 01:28:26 北京时间 UTC+8：查看pdftoppm生成的page-1..9.png（contact.png汇总），九页均未见裁切/重叠/空白；DOM溢出=[]；pdftotext回读5085字符、替换字符0。为本人自查，非独立审核。

示意动画已查看首末帧，画面标SYNTHETIC ROUTE - NOT MAP；完整视频未逐帧审片，不作官方地图渲染验收。
