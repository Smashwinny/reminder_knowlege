---
tags: [概念]
领域: 移动开发 / 地图
别名: [slippy map, 瓦片金字塔, z/x/y 瓦片]
首次来源: "[[项目笔记/deadrun]]"
---

# Web墨卡托与瓦片金字塔

**一句话定义**：把经纬度球面压成平面像素的投影公式（Web Mercator），再把平面切成按 `z/x/y` 编号、可逐张下载的 256px 小图（瓦片金字塔）。

**属于领域**：移动开发 / 地图渲染。

**通俗理解**：地球是橘子皮，屏幕是纸。先把橘子皮压平（Mercator 会让两极放大），再把这张巨大的纸裁成带编号的瓦片——zoom 17 时世界 = 131072×131072 像素 = 2^17 × 2^17 张 256px 瓦片。手机只下载屏幕附近几张。压平的公式两行：`x = (lng+180)/360 × 2^z`、`y = (0.5 − ln((1+sinφ)/(1−sinφ))/4π) × 2^z`。符号写反不报错，症状是"地图显示错误的城市"，所以要用教科书公式独立重算 + 真服务器字节比对来验收（Deadrun 实测市中心瓦片 24835B vs 太平洋 103B = 241 倍）。

**与已有概念的关联**：
- 相关：[[相机死区跟随]]（瓦片只画摄像头窗口）、[[确定性脚本]]（投影是纯函数，可写对照测试）
- 对照：[[Three.js与场景图]]（三维场景图 vs 二维瓦片拼接，都是"只渲染视野"）

**首次接触于**：[[项目笔记/deadrun]]

## Route Studio：瓦片/像素单位勘误与距离边界（2026-10-06）

[[项目笔记/route_studio]] 的既有学习材料指出，上文“zoom 17 时世界 = 131072×131072 像素”混淆了瓦片与像素。正确拆分为每轴 2^17=131072 张瓦片；若每张瓦片边长是 256 像素，则每轴 256×2^17=33554432 像素。旧公式的 x/y 乘 2^z 得瓦片坐标，转像素还需乘实际瓦片边长；三角函数中的纬度须用弧度。256 只作此处条件，其他尺寸按实际服务核对。

保留上述旧文以追踪勘误，不再将其像素数当正确结论。投影到平面、计算地表距离与按经纬度分量插值是不同问题。固定 Route Studio 的 distance_meters 使用半径 6371000 米的球面大圆近似，interpolate 则线性混合经纬度并钳制 fraction；二者不能合称椭球测地线算法或真实 GPS 精度验证。

历史 TEST_ONLY 原点附近三点的相邻段约 111.194926645 米，两段约 222.389853289 米，只是该公式与合成输入的结果。没有地图服务、浏览器、真机或真实路程测量。关联 [[Agent输出协议契约]]、[[事实与判断分离]]。

来源：[MapTiler 瓦片与像素](https://docs.maptiler.com/google-maps-coordinates-tile-bounds-projection/)、[PROJ 投影](https://proj.org/en/stable/operations/projections/webmerc.html)、[PROJ 测地计算](https://proj.org/en/stable/geodesic.html)、[固定 gpx.py](https://github.com/yinsuecci/mockrunning/blob/137297d7ca980f92a6a832708c9c61964bde7591/src/ios_location_controller/gpx.py)；[历史实验日志](../../route_studio/delivery/route-studio-experiment-log.md)。
