# sources：可追溯来源清单

全部读取日为2026-11-11（Asia/Shanghai）；时间统一转换至Asia/Shanghai，论文日期标签来自原站。

## S1 原帖及作者链
- https://x.com/srini_vij/status/2113777992811807207
- https://x.com/srini_vij/status/2113994340586357233
- https://x.com/srini_vij/status/2113994507712893015
读取：x.get_posts_by_id，x.search_posts_all（conversation_id，第二页0条）。记录见sources/original-post.md，包含note_tweet全文。没有引用帖字段；未完整观看210秒附带视频。身份以作者自己贴的仓库链接为依据，不以第三方机器人回答作最终证明。
原帖发表于2026-10-24 07:42:00（Asia/Shanghai），清单的2026-10-25为收录/查看线索，不当发表时间。

## S2 主论文
- https://arxiv.org/abs/2604.14141v3
- https://arxiv.org/html/2604.14141v3
标题LingBot-Map: Geometric Context Transformer for Streaming 3D Reconstruction。v1提交2026-04-16 01:58:13（Asia/Shanghai），v3修订2026-09-09 00:51:09（Asia/Shanghai）。实读方法§3、训练/推理§4、指标§5与实验/局限§6–7。abs及HTML均落盘；仓库内paper.pdf也保存并pdftotext，仓库PDF按SHA定位，不强行宣称与arXiv字节相同。
关键定位：§3.2上下文公式、§3.4分页KV、§4.4 Direct/VO、§5.2 Sim(3)对齐ATE、表9 H800/4090。

## S3 一手仓库
- https://github.com/Robbyant/lingbot-map/tree/b9dd1b1de535e6d36e777fb42b8433c781bfd783
- main SHA `b9dd1b1de535e6d36e777fb42b8433c781bfd783`
- 提交时间 2026-10-14 23:56:56（Asia/Shanghai）
读取范围：README、pyproject.toml、LICENSE.txt、aggregator/stream.py特殊token与缓存参数、models/gct_stream_window_v2.py窗口与对齐、layers/attention.py后端/注意力定义、utils/geometry.py深度反投影。只读源码，无模型执行。
README:31宣称约20 FPS；239–249关键帧/Direct范围与windowed；320–329相机头迭代；416–418表格的10/13矛盾。
- https://raw.githubusercontent.com/Robbyant/lingbot-map/b9dd1b1de535e6d36e777fb42b8433c781bfd783/README.md
- https://raw.githubusercontent.com/Robbyant/lingbot-map/b9dd1b1de535e6d36e777fb42b8433c781bfd783/lingbot_map/aggregator/stream.py
- https://raw.githubusercontent.com/Robbyant/lingbot-map/b9dd1b1de535e6d36e777fb42b8433c781bfd783/lingbot_map/models/gct_stream_window_v2.py
- https://raw.githubusercontent.com/Robbyant/lingbot-map/b9dd1b1de535e6d36e777fb42b8433c781bfd783/LICENSE.txt
许可：README及LICENSE.txt声明Apache2.0；练习ZIP仅含原创教学代码，不打包上游源码。权重和外部数据许可未逐一核查，不能推广为所有素材都同许可。

## S4 历史一手反证
- https://www.robots.ox.ac.uk/~gk/PTAM/
Klein/Murray PTAM官网，说明ISMAR2007相机跟踪/建图，不需惯性传感器；强调初始化需要平移。保存ptam.html；页面更新标签2014，不假造commit SHA。

## S5 预积分一手论文
- https://arxiv.org/abs/1512.02363v3
- https://arxiv.org/pdf/1512.02363v3
Forster/Carlone/Dellaert/Scaramuzza, On-Manifold Preintegration for Real-Time Visual-Inertial Odometry；v3日期2016-10-30 18:43:58（Asia/Shanghai）。读摘要及§V–VI关键推导（关键帧汇总、状态解耦、SO(3)、偏置修正），不宣称完成全篇逐式验证。保存PDF与文本。

## 查重与风格基线
- https://github.com/Smashwinny/reminder_knowlege/tree/a8674777e18302b8804b137212b1396cbfe5a747
- main SHA `a8674777e18302b8804b137212b1396cbfe5a747`
- 提交时间 2026-11-04 17:42:58（Asia/Shanghai）
已实读：vault/00-总览.md、vault/项目笔记/abot-recon.md、vault/项目笔记/slamformer.md、vault/概念/点图与前馈重建.md、vault/概念/流式滑窗与O(1)状态.md、vault/概念/漂移与回环闭合.md；风格样本abot-recon/abot_recon_guide.html。来源文件名在sources内以__替代/，保留原文。

## 证据等级与限制
原帖=作者所见，论文表=作者报告，源码=固定实现文本，本批输出=原创合成数值实验；四层不混用。无真实GPU模型指标，无独立审核，无完整原视频观看。

## 本地来源指纹（SHA256）
- `arxiv-v3-full.html` `32b332220e6797f9b07667a2720d319010deb4633c27bc8740b66e692b36bd63`
- `arxiv-v3.html` `065a02de831994c7943ac31e4dd3b0a25f45f892afa7687fdb986f89774f29fd`
- `imu-paper-v3.pdf` `214b8bee53e1fb6218c1cec1352d74c24951feec815517e6a0cc6dfcf1fd8f32`
- `imu-paper-v3.txt` `9d50f879e9bc6fa3f3338d486f65a2f01fbc2676eb462aca2eb0e607db8da866`
- `imu-paper.html` `f24a75b5c1636bc5f459ee704fb3cc83ef5a6cd61f858cec85d623593fdc0a69`
- `lingbot-map-commit.json` `36abf9d6e6b26a8c02e45fabb1777399333790764dfb8fad22892de033701ace`
- `lingbot-map-tree.json` `e2307a4210ed0913414ef91a2b5c61bdaaf89a159591ca890f02905dd6044a79`
- `lingbot-map__LICENSE.txt` `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4`
- `lingbot-map__README.md` `9c1bc132ef09f7bb55d293f06ef92fcec2bbdb954ea938960736580745721bec`
- `lingbot-map__lingbot-map_paper.pdf` `ffc4e177ad3166dcc4b045913739a7bebc8f1e621dd86d9a6ec52b6682d8bb66`
- `lingbot-map__lingbot_map__aggregator__stream.py` `6a19e43cb3ddaa569a56d2b9c6675d1693be0d8ad381803a354de32f75aa0a5f`
- `lingbot-map__lingbot_map__layers__attention.py` `59d28bdbb80c7d9138ce5b77fffdc636beee7081767c774a5c6ca7a675925419`
- `lingbot-map__lingbot_map__models__gct_stream.py` `46709995f10c2dcb9770cbfac70c9de6b849a76d18e83089f2d938914d9dd668`
- `lingbot-map__lingbot_map__models__gct_stream_window_v2.py` `63e6c90d9002f17394f02e7f7dd8da7c7bee5ee5a7e28a27b5d1e0959d2dbee0`
- `lingbot-map__lingbot_map__utils__geometry.py` `7c89c10008dfeaed16f24ae3cadcf21b388a3cb9b98b3eee58a270ddbe877afb`
- `lingbot-map__pyproject.toml` `457219623bb313d632b50f595c808714cd6708d19fe83179fe5b8f5bd909f6fa`
- `original-post.md` `eed881bc70e7616cda89db19318b19b98f616298ac1fb0073a81a130a8c4332a`
- `paper.txt` `1d12815a9ff617075f521f76096df4d85f5d4ed57db3cd199448da9125a4394b`
- `ptam.html` `ec54d29bab5febdb3ac7af51069fa06ba699a952e447aeee27b5c951312c0c67`
- `reminder_knowlege-commit.json` `e08045cd24b4e964fb34ecfc8b36ea31cbe0dc74f7461974b714e980cc811335`
- `reminder_knowlege-tree.json` `078ab5a69beab6a31bb3b0d3fd6509fa2dc88995834e2c65fe3e3d96b0c009af`
- `reminder_knowlege__abot-recon__abot_recon_guide.html` `1618a09c6024bee0b3c2b9d4908c12e9a91bdf674f461d9a9b02c73a428a4519`
- `reminder_knowlege__vault__00-总览.md` `a8779f945f617faa941692db5f1bc684228082930fbe4703b8e8eb8b1b3a8580`
- `reminder_knowlege__vault__概念__流式滑窗与O(1)状态.md` `c2e32fbcc4a12772415f3f79e71ee307037f318c356a9cbbf42e25a7c56c4573`
- `reminder_knowlege__vault__概念__漂移与回环闭合.md` `fc3a3710ac82e3aa3866436dc2d075431f4c4fa000d147b71e7ddfad6da8cf48`
- `reminder_knowlege__vault__概念__点图与前馈重建.md` `391ebbddd9e9777fc1b74f524fc502cbf774b66de78aef3b0cb55f8103a468d8`
- `reminder_knowlege__vault__项目笔记__abot-recon.md` `583bbc70c64abf7234519247e2ecd833777c76ab8182b2c7f45bc33aeeba762f`
- `reminder_knowlege__vault__项目笔记__slamformer.md` `8dadbe40964c85152356cdd66b0dd0f648abe9aa5af96e9fc4b95ba750540951`
