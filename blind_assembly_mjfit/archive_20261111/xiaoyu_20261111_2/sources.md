# sources：URL、版本、日期、来源指纹

读取日：2026-11-11（Asia/Shanghai）。所有具体时间转为Asia/Shanghai。

## S1 原帖全文
https://x.com/IlirAliu_/status/2113539950444474809
@IlirAliu_，2026-10-23 15:56:06（Asia/Shanghai），无引用帖。x.get_posts_by_id首次仅280字，但x.search_posts_all(conversation_id)提供note_tweet全文、原帖项目/论文/仓库链接。实读原文及链接转录在sources/original-post.md。没有把读者回复当作者声明。
原视频33.933秒未完整观看，不从画面推断性能。订阅推广不操作。

## S2 主论文
- https://arxiv.org/abs/2610.23849v1
- https://arxiv.org/html/2610.23849v1
- https://arxiv.org/pdf/2610.23849v1
Antonia Bronars, Younghyo Park, Kushal Kedia, Pulkit Agrawal；Blind Precise Assembly: Proprioceptive Sim-to-Real Peg-in-Hole for Diverse Parts。
v1提交2026-10-17 01:58:48（Asia/Shanghai）。abs/HTML/PDF均保存。实际读取§2方法、§3结果、§5局限及附录A–C：33/36维观测、H30历史、训练特权监督、随机化范围、173/237真机计数、碰撞benchmark限制、ID/OOD结果。
关键区分：20µm为碰撞几何benchmark；真机插销clearance约0.5–1.5mm单侧。齿轮/螺母没有在此论文证明真机同率。

## S3 mjfit一手仓库
- https://github.com/younghyopark/mjfit/tree/5833f465896e1e06bc4be4f003be847f5183a4db
- main SHA `5833f465896e1e06bc4be4f003be847f5183a4db`
- 提交时间 2026-10-21 22:11:21（Asia/Shanghai）
读取README、pyproject.toml、LICENSE、docs/pegs.md、docs/sampling.md、examples/drop_peg.py、examples/many_pegs.py、_peg.py签名与生成参数、_sample.py快照与test_peg.py几何测试片段。没有声称全套测试执行。
- https://raw.githubusercontent.com/younghyopark/mjfit/5833f465896e1e06bc4be4f003be847f5183a4db/examples/drop_peg.py
- https://raw.githubusercontent.com/younghyopark/mjfit/5833f465896e1e06bc4be4f003be847f5183a4db/docs/pegs.md
- https://raw.githubusercontent.com/younghyopark/mjfit/5833f465896e1e06bc4be4f003be847f5183a4db/docs/sampling.md
- https://raw.githubusercontent.com/younghyopark/mjfit/5833f465896e1e06bc4be4f003be847f5183a4db/src/mjfit/_peg.py
安装：固定SHA公开ZIP；实际版本mjfit0.1.0/MuJoCo4.0.0。仅运行CPU几何/动力学，未重跑论文所有碰撞基线或GPU Warp。
许可MIT，保留LICENSE于sources及exercise/upstream。上游drop_peg.py原样打包；lab.py为原创。

## S4 作者项目页
https://younghyopark.me/blind-proprioceptive-assembly/
读取方法、观测/动作、训练期decoder、几何构造、真实硬件起点与任务分层。HTML保存project.html，无固定commit可得，以读取日期和SHA256存档；未执行其浏览器交互策略。

## 查重与风格
https://github.com/Smashwinny/reminder_knowlege/tree/a8674777e18302b8804b137212b1396cbfe5a747
main SHA `a8674777e18302b8804b137212b1396cbfe5a747`，提交时间2026-11-04 17:42:58（Asia/Shanghai）。总览/相关笔记已读取，路径见sources/vault__*。旧样式参考第一项已固定读取的同SHA abot-recon指南，沿用其圆角问答卡、渐变、醒目数值和SVG；本批没有改旧文件。

## E1–E6 本批证据
exercise/下MJCF、JSON、trace和完整stdout均真实生成。每次随机化参数可追踪，seed固定；统计作者样本计数与本批输出分开，不混算成功率。MuJoCo4版本差异明确，cpu_wall_s不拿去替代作者benchmark。

## 文件SHA256
- `mjfit-commit.json` `1f29c1e7344cf5f9a32d5f1b00c2d43942092201deacb3a1ac0d7d355127e10f`
- `mjfit-tree.json` `b217120cb11588974f0494700745aa78e2afc959a41520051819dddef90b2fde`
- `mjfit__LICENSE` `8b790eb529558ab0f2226c81e102fd21b8774c309db005239c70cb705f6fb09c`
- `mjfit__README.md` `2920fea56f4dc835f6fa614782d19c18c423d17eab924377e08c1d29fed004f1`
- `mjfit__docs__pegs.md` `ed52b2c98f52f4047d3b878d266e67e44c42c5af148dcdf9a51a92a715397db3`
- `mjfit__docs__sampling.md` `601b3e6255ba7abc0c576851564840f12848dce298f52921362e60d83b5b2b4d`
- `mjfit__examples__drop_peg.py` `a883fb8b3d63a5ceb5d509bd1a094068fe290198637ee69da7da4b970faaeb96`
- `mjfit__examples__many_pegs.py` `445d50cbc8e118873d41898d908117feebb065727d166a61126b18dd7e54dfda`
- `mjfit__pyproject.toml` `92ccc89b1d3268cb8b28f8be52f320539a4843cb667cabc4d9abc9b4c7c3d31e`
- `mjfit__src__mjfit____init__.py` `d6f45a4edfeb5ac81e7115f6f1f2cfb6d712204a35d3a6dc3a69cc669d5d14f2`
- `mjfit__src__mjfit___peg.py` `56411d22a23def6545deefc1c70a8f9c1e8c1fc5edb4a016aabbe2fe2d233cd5`
- `mjfit__src__mjfit___sample.py` `0238128c5f643c3145a15ebda906c18eb445836fe41d11b7295dc0a6cc82220d`
- `mjfit__tests__test_peg.py` `6548682d56c9b725b8e42ac57c1c3eff11666a1c33426e0767dce7437c82d199`
- `original-post.md` `070ba85a10432f6a8dc3e94f20f8fd24eddb54d0f018a880b18b2c6a95272b04`
- `paper-abs.html` `0c242f65b6a3eee7a261c24b2b7a476d99126cee7d210e47cb159db458b65757`
- `paper-full.html` `1c6319bff0b2ab9716a181cf8b07977bd1c426df499f5bf214c48adf79989a72`
- `paper-v1.pdf` `5bc66905c70d821a0d70a728e66ba80acb2269f6b4231f2e57de0b3470f122fb`
- `paper-v1.txt` `2d84fc4e5e75eed379380db867b7090363a0ff093b72b8d3c73ac87f55057c2d`
- `project.html` `e706bb5e2aff427f8e3bda3549716459df7690928f12fe25c69d0836bf3c37a9`
- `vault-commit.json` `e08045cd24b4e964fb34ecfc8b36ea31cbe0dc74f7461974b714e980cc811335`
- `vault-tree.json` `078ab5a69beab6a31bb3b0d3fd6509fa2dc88995834e2c65fe3e3d96b0c009af`
- `vault__vault__00-总览.md` `a8779f945f617faa941692db5f1bc684228082930fbe4703b8e8eb8b1b3a8580`
- `vault__vault__概念__Sim2Real与MuJoCo仿真.md` `f1e2d25684a03cf48638e3864452f462cd1418360158a2923a20ac01d59272e4`
- `vault__vault__概念__策略观测向量与动作契约.md` `c1fc025fc8a7a4c526083f1b1052c88a369f5c61f2a5a6c8a23d663e092f0942`
- `vault__vault__项目笔记__microduck.md` `5146cd83e9fa34b81f769ac177c75a802eea937510baa80d394f3bfd810ad958`
- `vault__vault__项目笔记__openarm.md` `434daa5c9b216d8909a9d49810bcdedcf85414006fd46771d3de0a89ed23add3`
