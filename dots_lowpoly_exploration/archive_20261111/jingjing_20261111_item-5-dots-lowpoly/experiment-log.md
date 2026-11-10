# Dots 自动换题材与程序化低模试验 · 真实实验日志

执行时间：2026-11-11 01:20:36 CST（UTC+8）

只读公共研究＋云端隔离实验。自编程序不是上游实现，除明确标出的官方构建。

## 按主题轮换生成网格
目的：用确定性菜谱写出8个不同题材的OBJ/GLB和预览图

```bash
cd /workspace/reminder-batch-2026-11-11/item-5-dots-lowpoly
python3 exercise/generate.py generate
```

真实输出（exit=0）：
```text
generated 8 models; themes=['tree', 'house', 'crystal', 'robot', 'boat', 'cactus', 'lantern', 'mushroom']; real dots runs=0; blender=0
  tree: faces=24 obj=24 glb=24 paint=30366
  house: faces=30 obj=30 glb=30 paint=3146
  crystal: faces=12 obj=12 glb=12 paint=20663
  robot: faces=72 obj=72 glb=72 paint=36296
  boat: faces=36 obj=36 glb=36 paint=27051
  cactus: faces=60 obj=60 glb=60 paint=25059
  lantern: faces=48 obj=48 glb=48 paint=30954
  mushroom: faces=18 obj=18 glb=18 paint=21084
/workspace/reminder-batch-2026-11-11/item-5-dots-lowpoly/exercise/generate.py:182: DeprecationWarning: Image.Image.getdata is deprecated and will be removed in Pillow 14 (2027-10-15). Use get_flattened_data instead.
  n = sum(1 for px in img.getdata() if px != bg and px != (37, 99, 235))

```
验证：输出含 generated 8 models 与 real dots runs=0

## 对账面数与文件
目的：确认OBJ与GLB面数一致、预览非空、题材确实在轮换

```bash
cd /workspace/reminder-batch-2026-11-11/item-5-dots-lowpoly
python3 exercise/generate.py verify
```

真实输出（exit=0）：
```text
PASS count n=8
PASS unique_themes ['tree', 'house', 'crystal', 'robot', 'boat', 'cactus', 'lantern', 'mushroom']
PASS rotation themes change across the batch
PASS tree_files obj+glb+png
PASS tree_counts {'index': 0, 'theme': 'tree', 'obj': '00-tree.obj', 'glb': '00-tree.glb', 'png': '00-tree.png', 'vertices': 18, 'faces': 24, 'obj_vertices': 18, 'obj_faces': 24, 'glb_vertices': 18, 'glb_faces': 24, 'preview_painted_pixels': 30366, 'lowpoly': True, 'sha256_obj': '411de900199c1df90d8c2937f66147d914870816bfb841abf9ba9b672c88b7b6', 'sha256_glb': '29bfd345a70c6fdbdc3c13501436ada1719369a2ea859d9a41ab9ab24007c4d5'}
PASS tree_lowpoly faces=24
PASS tree_preview 30366
PASS tree_obj_hash obj unchanged
PASS house_files obj+glb+png
PASS house_counts {'index': 1, 'theme': 'house', 'obj': '01-house.obj', 'glb': '01-house.glb', 'png': '01-house.png', 'vertices': 21, 'faces': 30, 'obj_vertices': 21, 'obj_faces': 30, 'glb_vertices': 21, 'glb_faces': 30, 'preview_painted_pixels': 3146, 'lowpoly': True, 'sha256_obj': 'ba5770b03b2e16443eba446ecfd4b9eb8ddb9df2d2da233d4a4cff72d3cc5c92', 'sha256_glb': 'bc97e1d704143e7c0210ac8babf27dbd04d9bb2f7f6d91e40ca93287125eff13'}
PASS house_lowpoly faces=30
PASS house_preview 3146
PASS house_obj_hash obj unchanged
PASS crystal_files obj+glb+png
PASS crystal_counts {'index': 2, 'theme': 'crystal', 'obj': '02-crystal.obj', 'glb': '02-crystal.glb', 'png': '02-crystal.png', 'vertices': 10, 'faces': 12, 'obj_vertices': 10, 'obj_faces': 12, 'glb_vertices': 10, 'glb_faces': 12, 'preview_painted_pixels': 20663, 'lowpoly': True, 'sha256_obj': '7b80366c87c5e6e8b8b264300119588d01ef4a21076ece8ce54c4fe8d983fdff', 'sha256_glb': '4a4dcde694a7c65b9cb2731246f43f391c16df963bf9bd16c3a3b4aeaaecc268'}
PASS crystal_lowpoly faces=12
PASS crystal_preview 20663
PASS crystal_obj_hash obj unchanged
PASS robot_files obj+glb+png
PASS robot_counts {'index': 3, 'theme': 'robot', 'obj': '03-robot.obj', 'glb': '03-robot.glb', 'png': '03-robot.png', 'vertices': 48, 'faces': 72, 'obj_vertices': 48, 'obj_faces': 72, 'glb_vertices': 48, 'glb_faces': 72, 'preview_painted_pixels': 36296, 'lowpoly': True, 'sha256_obj': '6d22ce4ce29ec293d6911fa78b1216e28bffb27c6dfcc9818e4de70e6b0afac6', 'sha256_glb': 'bd75d3ca15a8dfdd96212d98f5fbdf120219351a8ca1335287ecb1ba02d39d05'}
PASS robot_lowpoly faces=72
PASS robot_preview 36296
PASS robot_obj_hash obj unchanged
PASS boat_files obj+glb+png
PASS boat_counts {'index': 4, 'theme': 'boat', 'obj': '04-boat.obj', 'glb': '04-boat.glb', 'png': '04-boat.png', 'vertices': 26, 'faces': 36, 'obj_vertices': 26, 'obj_faces': 36, 'glb_vertices': 26, 'glb_faces': 36, 'preview_painted_pixels': 27051, 'lowpoly': True, 'sha256_obj': 'c55b342d8f0246e8c5fa7d34fdc20798c386e5051ce7dba23a5aaf611cbdc72a', 'sha256_glb': 'eec75385135fb457d788434e1eda8730c87ea68bd548477c81550294f6f825db'}
PASS boat_lowpoly faces=36
PASS boat_preview 27051
PASS boat_obj_hash obj unchanged
PASS cactus_files obj+glb+png
PASS cactus_counts {'index': 5, 'theme': 'cactus', 'obj': '05-cactus.obj', 'glb': '05-cactus.glb', 'png': '05-cactus.png', 'vertices': 40, 'faces': 60, 'obj_vertices': 40, 'obj_faces': 60, 'glb_vertices': 40, 'glb_faces': 60, 'preview_painted_pixels': 25059, 'lowpoly': True, 'sha256_obj': 'd17706bebd593f7c82375e90be98a8b7acc7c68cedcbf727177941e948ade240', 'sha256_glb': 'b573139b2ad10e6ee403525a1b48237aad584e9ed2fd9030837efb7e79e01d11'}
PASS cactus_lowpoly faces=60
PASS cactus_preview 25059
PASS cactus_obj_hash obj unchanged
PASS lantern_files obj+glb+png
PASS lantern_counts {'index': 6, 'theme': 'lantern', 'obj': '06-lantern.obj', 'glb': '06-lantern.glb', 'png': '06-lantern.png', 'vertices': 32, 'faces': 48, 'obj_vertices': 32, 'obj_faces': 48, 'glb_vertices': 32, 'glb_faces': 48, 'preview_painted_pixels': 30954, 'lowpoly': True, 'sha256_obj': 'e2f6e338011bff72dc8b99674f9fe5fb95798e31b69c8930bfedee9bca4f3eb1', 'sha256_glb': '85dcda836cf4a291ea0f6f220021759d03b8a6af1685fb733429047898096c85'}
PASS lantern_lowpoly faces=48
PASS lantern_preview 30954
PASS lantern_obj_hash obj unchanged
PASS mushroom_files obj+glb+png
PASS mushroom_counts {'index': 7, 'theme': 'mushroom', 'obj': '07-mushroom.obj', 'glb': '07-mushroom.glb', 'png': '07-mushroom.png', 'vertices': 13, 'faces': 18, 'obj_vertices': 13, 'obj_faces': 18, 'glb_vertices': 13, 'glb_faces': 18, 'preview_painted_pixels': 21084, 'lowpoly': True, 'sha256_obj': '46eb26ae36856ad06a1d8ae35c517b3552d036fd0973a1adfc7673103379e15b', 'sha256_glb': 'd5445a11ae6b4dc25174945054fb4ce5a2572ecae42b074f5858cd5757546f08'}
PASS mushroom_lowpoly faces=18
PASS mushroom_preview 21084
PASS mushroom_obj_hash obj unchanged
assertions=43 failed=0 dots_quality_claimed=0

```
验证：退出码0；assertions=43 failed=0

## 抽查一份OBJ结构
目的：确认导出的是可解析的三角形OBJ，而不是空文件

```bash
cd /workspace/reminder-batch-2026-11-11/item-5-dots-lowpoly
python3 exercise/inspect_obj.py
```

真实输出（exit=0）：
```text
# procedural low-poly tree
v 18 f 24

```
验证：与 manifest 中 tree 的顶点数、面数一致

## 留下输入与结果指纹
目的：给生成器与清单留下不可混淆的哈希

```bash
cd /workspace/reminder-batch-2026-11-11/item-5-dots-lowpoly
sha256sum exercise/generate.py exercise/out/manifest.json
```

真实输出（exit=0）：
```text
b6132898fa21c2f94db972a3687a2c39a0e2fd26c6d9d875d6fffebb123f5382  exercise/generate.py
272e4520d0eca0451e6be9b1c139f1f2ffd2aec0ea3c86c265d4a38b9b577bf2  exercise/out/manifest.json

```
验证：同样输入重跑则清单哈希不变


## 未验证边界
未登录、未调用 Dots，未测量积分或 token；未安装或操作 Blender；未见原帖视频；未做引擎导入、UV、碰撞或动画绑定；程序化网格不能代表 AI 生成质量。
