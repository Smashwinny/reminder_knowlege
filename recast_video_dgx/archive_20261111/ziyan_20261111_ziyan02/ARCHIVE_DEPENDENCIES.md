# 公开归档版依赖恢复说明

本次公开整理移除了第三方源码、模板及上游说明书副本；原始ZIP仍在本地归档，原创驱动、教学代码、测试和既有结果保留。许可证/NOTICE仅说明来源及条件，不代表源码仍随包提供。

**本轮没有下载依赖、重新执行实验或重新学习；不能宣称清理后的目录直接可运行或已通过复现。** 原HTML/PDF/实验日志及README中的命令描述的是当时完整实验包，公开版需先恢复下表依赖，并检查原README的运行环境和其他外部依赖。不要把历史成功记录当作新环境运行结果。

## 已记录的一手版本

仓库：[JayceHuang/jayce-recast-video-dgx](https://github.com/JayceHuang/jayce-recast-video-dgx)  
固定提交：`bee52327a92ce6fe7cbb07b43330c88da526cb14`（[固定树](https://github.com/JayceHuang/jayce-recast-video-dgx/tree/bee52327a92ce6fe7cbb07b43330c88da526cb14)）。

版本和路径来自已经保存的sources.md、实验清单/许可与原ZIP，不是本轮重新连接上游的结果。SHA256是从原交付包逐字节计算的预期内容哈希。

## 恢复方法（说明，未执行）

1. 将上述公开仓库的固定提交取回另一个隔离的依赖目录，不把完整上游或.git纳入学习仓库。
2. 以该提交的仓库根为起点读取下表“上游相对路径”；仅将必要文件恢复到本项目archive_20261111下的“练习相对路径”。保留原许可证、署名与第三方条件。
3. 对每个恢复文件计算SHA256并与表中比较。路径不可得或哈希不符时停止恢复、保留差异，不用最新main替代，也不覆盖原创练习。
4. 本说明只交代缺失依赖；没有执行这些步骤，没有确认网络可达/重新取回字节，也没有承诺跨系统或新环境的复现。

| 练习相对路径（恢复位置） | 固定仓库内相对路径 | 原交付字节SHA256 |
|---|---|---|
| `evidence/upstream/assets/h3-api-base.json` | `assets/h3-api-base.json` | `68b5129d0011ecc46f42cfa5bd04918b100b0776272d75802f05deb285fab458` |
| `evidence/upstream/examples/plan.example.json` | `examples/plan.example.json` | `1fc0fc7da74049089a316aa161a485aa2eef8829382591edca8e1a7e77f79772` |
| `evidence/upstream/examples/task.example.json` | `examples/task.example.json` | `3424c0c8e91d579dec7418fe1088a0dc21422db486a2d2b156aa656c2659ece6` |
| `evidence/upstream/examples/visual-review.example.json` | `examples/visual-review.example.json` | `a4ca08ef6f46d28573f1279b7761eb2b00135aa217f1954871c8e291f8798814` |
| `evidence/upstream/README.md` | `README.md` | `8b4e6fb41f56ab8b9e5c6db07e736207b4f0c95e08279b03fd1ef20f41526dd6` |
| `evidence/upstream/references/comfyui.md` | `references/comfyui.md` | `3b7e670a4527ef0f6ecc9cbbf756e8f8285b98a434e1313f098f3b5b359727af` |
| `evidence/upstream/references/production.md` | `references/production.md` | `a493fc0d5ab4c33ec94905b895c0cdded0cff127260bc279cf34036e938a8dae` |
| `evidence/upstream/references/quality.md` | `references/quality.md` | `4532c967f367481e0654b3da44cca2c820cd6f90d51ae52f824c5641424bbc19` |
| `evidence/upstream/scripts/native_run.py` | `scripts/native_run.py` | `85bac1fe8004a121927affe81addbbc376f4c876f5b097cdd82fe3ac5a008084` |
| `evidence/upstream/scripts/recast.py` | `scripts/recast.py` | `978696c62e8e888e897b8cf7123aef14f7de8988a29de4d9a402326b63e4765c` |
| `evidence/upstream/scripts/remote_job.py` | `scripts/remote_job.py` | `cd184dc23df231a13162e919650b4d3284c4bbdba8efdd329efb145b61ba1913` |
| `evidence/upstream/SKILL.md` | `SKILL.md` | `96c846906af3d1bede63d036112a9b6a19dd7c0527523931461a80071da6cb92` |
| `evidence/upstream/tests/test_production.py` | `tests/test_production.py` | `ad8b540cc572a497e7f768ce4fab74fbd8503e21fd2d667cda22f969902076da` |
| `evidence/upstream/VALIDATION.md` | `VALIDATION.md` | `a23481f797d5201895362db58850958f08ce027991d21aed29a36964571de29a` |
