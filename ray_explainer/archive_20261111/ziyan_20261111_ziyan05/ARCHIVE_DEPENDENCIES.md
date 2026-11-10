# 公开归档版依赖恢复说明

本次公开整理移除了第三方源码、模板及上游说明书副本；原始ZIP仍在本地归档，原创驱动、教学代码、测试和既有结果保留。许可证/NOTICE仅说明来源及条件，不代表源码仍随包提供。

**本轮没有下载依赖、重新执行实验或重新学习；不能宣称清理后的目录直接可运行或已通过复现。** 原HTML/PDF/实验日志及README中的命令描述的是当时完整实验包，公开版需先恢复下表依赖，并检查原README的运行环境和其他外部依赖。不要把历史成功记录当作新环境运行结果。

## 已记录的一手版本

仓库：[imraywang/rayskills](https://github.com/imraywang/rayskills)  
固定提交：`ca254f09a17e2e2c0aba7651c36688c322b1f2b2`（[固定树](https://github.com/imraywang/rayskills/tree/ca254f09a17e2e2c0aba7651c36688c322b1f2b2)）。

版本和路径来自已经保存的sources.md、实验清单/许可与原ZIP，不是本轮重新连接上游的结果。SHA256是从原交付包逐字节计算的预期内容哈希。

## 恢复方法（说明，未执行）

1. 将上述公开仓库的固定提交取回另一个隔离的依赖目录，不把完整上游或.git纳入学习仓库。
2. 以该提交的仓库根为起点读取下表“上游相对路径”；仅将必要文件恢复到本项目archive_20261111下的“练习相对路径”。保留原许可证、署名与第三方条件。
3. 对每个恢复文件计算SHA256并与表中比较。路径不可得或哈希不符时停止恢复、保留差异，不用最新main替代，也不覆盖原创练习。
4. 本说明只交代缺失依赖；没有执行这些步骤，没有确认网络可达/重新取回字节，也没有承诺跨系统或新环境的复现。

| 练习相对路径（恢复位置） | 固定仓库内相对路径 | 原交付字节SHA256 |
|---|---|---|
| `ray-explainer-offline/upstream/assets/canvas.json` | `skills/ray-explainer/assets/canvas.json` | `4f24b7f961a507146f26d677c241272f90124b121aeac698d3a28b98650a74e5` |
| `ray-explainer-offline/upstream/assets/hf-template/build.py` | `skills/ray-explainer/assets/hf-template/build.py` | `be1718627c0ffafc7dd1ee562ac08f7df7a728a7216de180f5e48fcf51b84659` |
| `ray-explainer-offline/upstream/assets/hf-template/host_build.py` | `skills/ray-explainer/assets/hf-template/host_build.py` | `52319d73886eff9565f16bafd0cedb2c686d62cbd5bacf9248baf035419c5ab9` |
| `ray-explainer-offline/upstream/assets/hf-template/make_beats.py` | `skills/ray-explainer/assets/hf-template/make_beats.py` | `2aa14d2a527813c773044233e823243e551d8742688fe1bf82a2de5eb6603ac6` |
| `ray-explainer-offline/upstream/assets/huashu/clip.html` | `skills/ray-explainer/assets/huashu/clip.html` | `73db3956310c7798452057e4328e961c899507483ab0bb72e817ce0372893874` |
| `ray-explainer-offline/upstream/assets/huashu/clip.js` | `skills/ray-explainer/assets/huashu/clip.js` | `99eb158d8c71ca4c4ad967a6f996ec36fe87062f17e4d733723e32802720b2d8` |
| `ray-explainer-offline/upstream/assets/huashu/lib/camera.js` | `skills/ray-explainer/assets/huashu/lib/camera.js` | `53ddc95e972900abfb49bfea704a2b77897b9237836ee653aeed966d39ceeec5` |
| `ray-explainer-offline/upstream/assets/huashu/lib/chart.js` | `skills/ray-explainer/assets/huashu/lib/chart.js` | `93d3605cba7d7cf0bdda2c2dd8f9797734dd06c1f64fa18ef7a492f8755a8d27` |
| `ray-explainer-offline/upstream/assets/huashu/lib/collage.js` | `skills/ray-explainer/assets/huashu/lib/collage.js` | `4dcd3d15f8895dc6e3d4f2e4d82766782a4e77876fb863ded9480320b8959d93` |
| `ray-explainer-offline/upstream/assets/huashu/lib/diagram.js` | `skills/ray-explainer/assets/huashu/lib/diagram.js` | `98b15ba5f883dd95eca2ff52ba1d768c10a5bea7862bd13aee6d84b875e2b8c5` |
| `ray-explainer-offline/upstream/assets/huashu/lib/fonts.js` | `skills/ray-explainer/assets/huashu/lib/fonts.js` | `0d6a9608e46d58d44224b98286e5ac52736a07d9d9e2302b34862ff82dd3978b` |
| `ray-explainer-offline/upstream/assets/huashu/lib/kit.js` | `skills/ray-explainer/assets/huashu/lib/kit.js` | `a066c4d0d4dc7189dd9de7776938b4cbc6025a4bf4a38d2e181a6667744f3024` |
| `ray-explainer-offline/upstream/assets/huashu/lib/media.js` | `skills/ray-explainer/assets/huashu/lib/media.js` | `81d07aa964b76b0e8cf7f9ae871dc6e5283dec83190f69fd1c0acfe4b0be0476` |
| `ray-explainer-offline/upstream/assets/huashu/lib/motion.js` | `skills/ray-explainer/assets/huashu/lib/motion.js` | `22762a3691464b7504da562b3761edc70f7c138721618639697df3a5a93c1b97` |
| `ray-explainer-offline/upstream/assets/huashu/lib/paint.js` | `skills/ray-explainer/assets/huashu/lib/paint.js` | `95ccd1945a4a19b6e2d89a422d7ea7de96174acdbae1801090ca9ee48131f9a3` |
| `ray-explainer-offline/upstream/assets/huashu/lib/palettes.js` | `skills/ray-explainer/assets/huashu/lib/palettes.js` | `934acc426ebdada51f613d6e7b1cb693590d615a01d7a66d5461483bf79ff30a` |
| `ray-explainer-offline/upstream/assets/huashu/lib/toon.js` | `skills/ray-explainer/assets/huashu/lib/toon.js` | `54778963a97767742257e5b68890e5b292f2b89ce3fd1a1f9711224573988d8b` |
| `ray-explainer-offline/upstream/assets/huashu/lib/typo.js` | `skills/ray-explainer/assets/huashu/lib/typo.js` | `30db0cc68145dca22532e487da01aeb3ec97155e8b2c3a0747a009ce6638be8f` |
| `ray-explainer-offline/upstream/assets/huashu/lib/ui.js` | `skills/ray-explainer/assets/huashu/lib/ui.js` | `2608da0a38bfd429a9fe41c1a93a5d080d54c5fcccea80e7fea764e6ca3a97bf` |
| `ray-explainer-offline/upstream/assets/huashu/lib/util.js` | `skills/ray-explainer/assets/huashu/lib/util.js` | `a2092233bbca337a29b00ce261d81a5c7b6baa020c9e301916ebe4a997450b9d` |
| `ray-explainer-offline/upstream/assets/template/kit.js` | `skills/ray-explainer/assets/template/kit.js` | `8d22962cb3b7a7bc4357acc0bd7b9ef45dfefa8a6a943fa19a4096566b14005d` |
| `ray-explainer-offline/upstream/assets/template/overlay.js` | `skills/ray-explainer/assets/template/overlay.js` | `d12bf9a28e42ee6e03531fd2483f2db71ed245b79377429783e8f7b5f79f4609` |
| `ray-explainer-offline/upstream/assets/template/patterns.js` | `skills/ray-explainer/assets/template/patterns.js` | `bd4c134b4610cd508e050d686a8c55c7d1a7e3c2b1bbb6f123d5281bdc4cf7f4` |
| `ray-explainer-offline/upstream/assets/template/scenes.example.js` | `skills/ray-explainer/assets/template/scenes.example.js` | `e9a0b9bb4f5412161e362a87266abf4d9924a25332e5952935ec9d61eadaa6b3` |
| `ray-explainer-offline/upstream/assets/template/script.example.json` | `skills/ray-explainer/assets/template/script.example.json` | `b2ce701019a0c7c6f7983c86c92da89d870e9203f05f1a12264bf3b8f0a55580` |
| `ray-explainer-offline/upstream/assets/template/script.patterns.example.json` | `skills/ray-explainer/assets/template/script.patterns.example.json` | `185653255d4b30960e2881bd3712f8bbb8f1b1d207c71ebd223fac361fa8566f` |
| `ray-explainer-offline/upstream/assets/template/script.template.json` | `skills/ray-explainer/assets/template/script.template.json` | `7315bbdb28122c971cc2dcc34cec90e57b4be42bbd031fc3d1d1138798a74d81` |
| `ray-explainer-offline/upstream/assets/template/video.html` | `skills/ray-explainer/assets/template/video.html` | `27d6180558d14a90aedd2f4fa3c6b3d32cae6e7cac048536e3a75f7f5c5a0794` |
| `ray-explainer-offline/upstream/scripts/new_project.sh` | `skills/ray-explainer/scripts/new_project.sh` | `7ba1bdff33c594b66d9ae8998237658297877d7798766050910705ce1e11293d` |
| `ray-explainer-offline/upstream/scripts/qa_video.py` | `skills/ray-explainer/scripts/qa_video.py` | `febdec26521c11c405946ffb02cce9f74837729d2b0f53438d304187e565b236` |
| `ray-explainer-offline/upstream/scripts/render.js` | `skills/ray-explainer/scripts/render.js` | `68b17c67be7d69450f5ffbd20d79acaab184c00bbb9b0b89d3376ab79ee8f722` |
| `ray-explainer-offline/upstream/scripts/review.py` | `skills/ray-explainer/scripts/review.py` | `c813215cb6682babd0a9cc7f4c3c6a8e72c85ba3b49c379a16774c06a983194a` |
| `ray-explainer-offline/upstream/scripts/review_page.py` | `skills/ray-explainer/scripts/review_page.py` | `6321ee46f41ec7e0a06e38771e01334fecb3f34ca3a195dd9cd4f65caf928c7d` |
| `ray-explainer-offline/upstream/scripts/storyboard.py` | `skills/ray-explainer/scripts/storyboard.py` | `565f8b5b68c00bb0b762a38a91fba256afe3962525a9247a7253ed3831a9e878` |
| `ray-explainer-offline/upstream/scripts/test_hf_anchors.py` | `skills/ray-explainer/scripts/test_hf_anchors.py` | `b3d4e517032b69a4603bdeaf274eb0c7d81e01f8a03342a56bef81b1f74734b6` |
| `ray-explainer-offline/upstream/scripts/test_hf_template.py` | `skills/ray-explainer/scripts/test_hf_template.py` | `e4b35a84fe1d7ab0b0c327f937f69d37abf79956e0cbf22adcf4ab979d1d8b22` |

表中huashu文件的直接来源是该固定rayskills树内的vendored子集；其另有alchaincyf/huashu-art-motion归属与MIT许可。rayskills主体CC BY-NC、字体有各自条件；字体/浏览器/Node依赖仍按原README另行准备，本次不下载。
