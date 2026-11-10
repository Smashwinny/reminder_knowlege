# 第 5 项练习：程序化低模主题轮换

本练习**不是** OpenAI Dots，也不是 Blender 操作技能。它只演示「自动更换题材 → 写出 .obj/.glb → 渲染预览 → 留下人工验收清单」。

```bash
python3 generate.py generate
python3 generate.py verify
sha256sum generate.py out/manifest.json
```

- 成功标准：8 个不同题材、每个三角形面数 < 200、OBJ 与 GLB 面数一致、预览图非空、退出码 0。
- 未证明：Dots 真实生成质量、积分消耗、Blender 预装或游戏引擎可导入后的可用性。
