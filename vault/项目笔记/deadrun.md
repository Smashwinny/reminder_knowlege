---
tags: [项目]
类别: 开源项目类（GPS 健身游戏，拾遗队列 task 11a63d10）
上游仓库: https://github.com/larprober/Deadrun (MIT, @1c625f8)
完成日期: 2026-10-03
---

# deadrun

**这是什么**（一句话）：一个周末 + Claude Code 构建的开源 GPS 丧尸追逐跑步游戏——丧尸刷新在你真实的街道上走向你的 GPS 位置，唯一的操作是你的腿；推文 om_patel5 的"丧尸追你"App 闭源无名，Deadrun 是其功能等价开源孪生。

**它给我什么能力**：① 不依赖 Google key 的手搓瓦片地图方案（CARTO/OSM + Web Mercator 三公式 + @2x 退一级 zoom 省 4 倍请求）；② GPS 健身 App 传感器融合全套（anchor 计步噪声地板 / course-罗盘 1.4m/s 切换 / 9m/s×12s 反作弊闸门）；③ 纯函数游戏引擎（可 headless 仿真、种子复放、暂停时间旅行）；④ 波次难度经济（20 波前封顶保公平，之后无上限保证"必死但值得挑战"）。

**引入的概念**：
- [[Web墨卡托与瓦片金字塔]]
- [[相机死区跟随]]
- [[GPS朝向融合]]
- [[纯函数游戏引擎与种子复放]]

**实验记录**（做了什么、结果、坑）：
- 环境坑：`npm install` 被权限拒绝 → 改用 Node 24 内置类型剥离，exercise/node-src 复制源码补 `.ts` 扩展名，`node --experimental-transform-types` 直接跑，零依赖
- 实验1 平衡仿真（simulate.ts）：9 画像×5 种子；雕像 2m16s caught、3.3m/s 跑者 14.4 波 10m33s、贪心补给 18 波——"站着必死、绕路活最久"兑现
- 实验2 投影校验（check-tiles.ts）：31/33 通过；2 FAIL 仅因无 CARTO key 水印使市中心=太平洋字节数，非投影错误
- 实验3 交叉验证（osm-crosscheck.ts，自写）：同一 z/x/y 打 OSM 官方服务器，市中心 24835B vs 太平洋 103B = 241 倍，铁证手搓投影正确
- 实验4 无头复放（chase-demo.ts，自写）：整局追逐画成 SVG，Edge 截图目检通过；seed42 存活 5m00s/7 波/990m

**后续可深入的方向**：把引擎抽出来做任意 GPS 驱动小游戏；在真机上 Expo Go 跑通真 GPS；研究 MapCanvas 的瓦片缓存与旋转合成。

**产出**：`deadrun/Deadrun丧尸GPS跑步游戏-小白指南.pdf`
