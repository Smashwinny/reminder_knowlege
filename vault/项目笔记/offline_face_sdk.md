---
tags: [项目]
类别: 开源项目类（本地离线人脸识别 SDK，"开源"成色打折）
上游仓库: https://github.com/Faceplugin-ltd/Open-Source-Face-Recognition-SDK (dd5795f)
完成日期: 2026-10-03
---

# offline_face_sdk

**这是什么**（一句话）：Faceplugin 的"Open Source Face Recognition SDK"——把 检测→68点关键点→对齐→特征→比对 五步流水线打包成三个 Python 函数，纯 CPU 单脸约 50ms，全部权重仅 61MB，100% 离线。

**它给我什么能力**：任意图片找人脸+标框、68 点关键点、三轴头部姿态、256 维脸向量、0~100 同人判定（阈值 75⇔cos 0.5）；用途：相册按人聚类、考勤小工具、照片自动打码、人脸识别教学。

**引入的概念**：
- [[人脸识别流水线]] — 五道工序总图 + MB-Tiny SSD 超轻量检测 + 性能账单
- [[脸向量与同人判定]] — score=(cos+1)×50 公式破解、同异分离度、变装鲁棒性
- [[开源验货三查]] — 无 LICENSE + 闭源 FaceUtil.dll + 宣传活体检测实货没有

**实验记录**（做了什么、结果、坑）：
- 实验1 基线：`python run.py` → score=86.27 "same person"，4.6s 含冷启动，纯 CPU 断网可跑
- 实验2 逐工序计时（exp_pipeline.py）：检测 20ms / 关键点 6ms / 姿态 1ms / 特征 21ms；特征 256 维（非 512）、L2 范数=1.0；标注图 annotated_output.jpg
- 实验3 变装矩阵（exp_similarity.py）：翻转/旋转10°/模糊/提亮/缩放 互打分 97.3~100 全判同人
- 实验4 不同人区分（exp4_different_person.py，randomuser.me 公开授权头像，未采集真实人脸）：同人跨角度 cos 0.725→86.3 ✓；异人 cos 0.18~0.37→59~69 ✗ 正确拒绝
- 重要发现：官方 demo 图 1.jpg 与 2.png 是**同一人两个角度**（姿态 ry 7.3° vs -30.8° 佐证）——官方示例从未演示过"拒绝陌生人"，必须自己补验收
- 闭源取证：libFaceUtil.so 未剥符号表，strings 见 Jacobi SVD/Cholesky/Rodrigues → getPose68 实为"2D 关键点拟合 3D 人脸模板 SVD 解姿态"经典套路
- 坑：权重相对路径必须 chdir 到 repo 根；torch 2.4.1 最高支持 Py3.12（本机 3.14 装不上，用 3.12 venv）；Tensor 要 .numpy()/.detach()；DLL 仅 x64，Mac 无支持

**后续可深入的方向**：
- 用 insightface 开源权重替换闭源对齐环节，彻底合规
- 接入真活体检测（RGB 反射/红外双目）对抗照片攻击
- 向量聚类做本地相册按人分文件夹工具
