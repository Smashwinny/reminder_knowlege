from pathlib import Path
import html,json,zipfile,datetime
P=Path(__file__).resolve().parents[1];E=html.escape
sha='bee52327a92ce6fe7cbb07b43330c88da526cb14';main='a8674777e18302b8804b137212b1396cbfe5a747';base='https://github.com/JayceHuang/jayce-recast-video-dgx/blob/'+sha+'/'
qa=[
('这篇教程真正可复用的是什么？','不是名人换脸的效果保证，而是七站生产链：原片→分镜→剧照→任务包→生成→时钟恢复→成片，质检贯穿其中。原帖作者称54段、78次生成、三台机器，这些是案例自述，本轮没有复现这些规模或耗时。引用的10月13日与15日视频帖文字已随原文阅读，视频内容和互动数据未核验。[S1]',['原片与分镜','生成与映射','留痕和验收']),
('为什么先给原片做指纹和探测？','文件名与播放器显示秒数都可能误导。保存SHA256、解码帧数、有理数帧率、尺寸和音轨后，才有可追溯坐标系。本轮合成源是24fps、120帧、320×180、无音轨；不是文章里的8163帧原MV。原始probe做r/avg帧率相等检查，但这只是初筛，不是任意VFR的充分检测。[S2:recast.py 26–33]',['SHA256输入','120帧 / 24fps','5秒合成源']),
('分镜为什么用从0开始的半开区间？','[0,75)与[75,150)各有75帧，边界75只属于后一段；末端150是排他边界，不是最后可见帧。原帖“停在第8163帧”应理解为覆盖[0,8163)，最后索引8162。原始validate_plan校验无缺口、无重叠、无重复ID；本轮76制造缺口、74制造重叠均被拒绝。[S1][S2]',['[0,75)','[75,150)','总数150帧']),
('角色卡和每镜剧照能混用吗？','不能。身份卡回答是谁；场景图回答服装、机位、站位、姿势和遮挡。一个人的身份卡衣服不应污染镜头服装。旧库已经讲过身份锚定，本项只补“参考维度分离”和“软约束不能叫硬锁”：RGB/Guide/提示词仍可能漂移，必须观察生成产物。[S1][S3]',['身份是谁','场景穿什么','动作何时发生']),
('怎样冻结任务，且不编造审核通过？','固定run_id、segment_id、version、输入和工作流哈希。build-h3会拒绝已有输出目录；verify-task核对冻结输入、图和规格。reviewed只检查passed/reviewer/evidence/at字段，并不能证明人真的看过。我们只创建v001/v002合成占位清单，generation_authorized=false；未构建真实人像任务，也没填虚假的视觉通过。[S2 79–156]',['新版本目录','输入/图指纹','实际审核另证']),
('上一段尾帧如何接到下一段？','必须来自实际已生成且审过的上一段输出，保存predecessor_run、tail_path与tail_sha256。计划里画的“理想尾帧”不能替代真实尾帧。带前文上下文的生成片要用native_source_start表达源坐标偏移，避免接点重复。原始map_indices偏移测试本轮通过，但人像动作连续性尚未验证。[S2][S4]',['真实前段尾帧','带偏移映射','接口重审']),
('24fps变30fps为何不能直接加速？','5秒×24=120帧；把120帧以30fps播放只剩4秒，会比原动作快25%。保持5秒必须输出150帧，可用最近邻重复30帧。本轮原始map命令真实得到150帧/30fps/5秒；故意setpts=0.8*PTS得到120帧/30fps/4秒，QC拒绝。重复帧不是生成新运动，也不是光流补帧。[S2 169–200]',['120帧 / 5秒','最近邻重复30帧','150帧 / 5秒']),
('最近邻映射精确到什么程度？','公式j=round((source_frame−native_source_start)/source_fps×native_fps)，原始实现使用Fraction与Python半偶舍入。源30fps前12帧对应0,1,2,2,3,4,5,6,6,7,8,9；末帧映射119。源30000/1001不可偷换30。我们另用ffprobe逐帧检查150个PTS，最大误差0.000000334秒，受输出十进制精度影响。[S2][S4]',['源帧 i / fps','有理数与偏移','最近邻 j']),
('技术QC通过就是成片合格吗？','不是。原始qa对正确片给technical_pass=true，但visual_acceptance=false、dynamic_review=pending；错误片帧数失败却进程exit=0。这是本轮新增的重要消费者契约：必须读取JSON判定，不能只看退出码。当前qa检查计数/帧率/解码/可选PCM/黑场候选，不逐帧验证PTS；所以本练习另加PTS检查。[S2 202–210]',['进程 exit=0','读取技术判定','动态审看另记']),
('声音相同能证明同步吗？','不能。原工具合成时源音频packet copy，QA对全解码48k双声道PCM做相等比较；起始偏移与容器时钟仍需另核验。本轮选定上游合成测试对0.4004秒合成视频/正弦音做了真实合成和PCM相等检查；正式合成缺少视觉审核会被拒绝。自写5秒主实验没有音轨，不冒称声画同步通过。[S4]',['原声packet copy','PCM相等','PTS/观看另查']),
('生成翻车时该改哪里？','先定位缺陷阶段：原片/参考/第一阶段草稿/第二阶段精修/映射/拼接。原帖弯腰从草稿阶段产生、singing误导闭嘴角色、半睁眼补图仍未全修，是作者案例而非本轮模型实测。当前ComfyUI说明还提醒split2→6不能简化为所有任务固定6+6真实步数；应保留完整sigma、seed和实际执行事件。[S1][S5]',['问题帧定位','阶段归因','新版本对照']),
('能否现在宣布完整换脸MV已复现？','不能。已完成的是公开原文/源码实读、合成媒体CPU流水线与资料交付。GPU、ComfyUI节点/模型权重、真人身份/嘴形/眼神、连续播放和完整MV均待验证。不要下载版权MV或把名人形象当已授权素材；代码许可与媒体许可分别核对。先用自有/获授权素材做单人5秒镜头，公开成片需标注AI合成并避免冒充。[S3][S6]',['CPU已验证','模型生成待验证','授权与动态验收'])]
css='''@page{size:A4;margin:12mm}*{box-sizing:border-box}body{margin:0;color:#17213b;background:#eef6ff;font-family:"Noto Sans CJK SC",sans-serif;font-size:14px;line-height:1.65}.page{width:186mm;min-height:270mm;margin:8mm auto;padding:9mm;background:white;break-after:page;position:relative}.page:last-child{break-after:auto}.hero{background:linear-gradient(130deg,#00b8d9,#3157f6);padding:26px;border-radius:20px;color:white}h1{font-size:35px;line-height:1.3}h2{font-size:24px;color:#1744ca;border-bottom:4px solid #00b8d9;padding-bottom:6px}h3{font-size:18px;line-height:1.4;margin:10px 0}p{margin:9px 0}.card{border:1px solid #c8ddf7;border-left:6px solid #00b8d9;border-radius:12px;padding:14px 17px;margin:16px 0;break-inside:avoid}.big{font-size:26px;font-weight:900;color:#ec6b12}.warn{background:#fff0ce;border-left:6px solid #ff7a1a;padding:14px}.num{font-size:26px;color:#3157f6;font-weight:900}svg{width:100%;height:54px;margin-top:6px}svg text{font-family:"Noto Sans CJK SC",sans-serif}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#17213b;color:#eaf7ff;font-size:11px;line-height:1.6;padding:13px;border-radius:10px}a{color:#2456d9;overflow-wrap:anywhere}.foot{font-size:10px;color:#617287;border-top:1px solid #c8ddf7;margin-top:18px;padding-top:8px}li{margin:7px 0}@media print{body{background:white}.page{margin:0;padding:0;width:auto;min-height:0;height:260mm;display:flow-root}.card{margin:12px 0;padding:12px 15px}body{font-size:12.5px}h3{font-size:17px}svg{height:48px}}'''
def svg(ls):
 s='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 660 60" role="img" aria-label="'+E('→'.join(ls))+'">'
 for i,t in enumerate(ls):
  x=i*223;s+=f'<rect x="{x}" y="4" width="208" height="50" rx="10" fill="{["#00a9c5","#3157f6","#f27b15"][i]}"/><text x="{x+104}" y="35" fill="white" text-anchor="middle" font-size="16">{E(t)}</text>'
  if i<2:s+=f'<path d="M{x+209} 29h13l-5 -5m5 5l-5 5" stroke="#17213b" fill="none"/>'
 return s+'</svg>'
pages=[]
def add(t):pages.append('<section class="page">'+t+f'<div class="foot">item02 · {len(pages)+1} / 9 · 2026-11-11（Asia/Shanghai）· 制作者自查，非独立审核</div></section>')
add('''<div class="hero"><b>REMINDER / 02 · 增量学习</b><h1>换脸 MV 不靠运气<br>靠可追溯生产线</h1><p>原帖《AI名人换脸从 0 到 1 小白教程》<br>七站工作流 × 帧级时钟 × 逐镜质检</p></div><p class="big">150 帧对齐通过 ≠ 演得正确</p><div class="warn">本轮真跑：5秒合成片24→30fps，150帧逐帧PTS检查；正确/错误片QC正负对照；3个选定原始上游测试。没有生成任何真人换脸视频。</div><h2>四个用途</h2><ul><li>给短视频工程建立原片、分镜、版本、合成、质检的追溯链。</li><li>跨24/30/30000÷1001帧率恢复动作时钟，避免快进冒充对齐。</li><li>通过缺口/重叠与错误时长负例，测试交片检查器是否真会拒绝。</li><li>把技术通过、静态参考与动态表演质量分账，精准定位返工。</li></ul><h2>已有知识不重复造轮子</h2><p>固定main已读总览、分镜表驱动生成、角色一致性锚定与ai_shortdrama_tools笔记；保留原有概念。本项只补半开帧区间、有理数映射、不可变选片版本和QC判定消费契约。视觉采用旧库的大号数字、圆角卡片及青蓝橙高亮，不内嵌字体或大图。</p>''')
for z in range(4):
 b='<h2>十二问：从工程组织到验收边界</h2>'
 for i in range(z*3,z*3+3):
  q,a,l=qa[i];b+=f'<div class="card"><h3><span class="num">{i+1:02}</span> {E(q)}</h3><p>{E(a)}</p>{svg(l)}</div>'
 add(b)
steps=[
('建立可控输入，不碰私人或版权素材','python3 exercise/lab.py 1','生成5秒testsrc2并用原始probe探测。底层完整生成命令：','ffmpeg -v error -f lavfi -i testsrc2=size=320x180:rate=24 -t 5 -c:v libx264 -pix_fmt yuv420p media/native24.mp4','结果：120帧，24/1fps，5.000000秒，320×180，无音轨。验证：results/native-probe.json与step1.txt；全部解码计数，不信播放器。'),
('原始目录骨架与分镜/版本负例','python3 exercise/lab.py 2','调用原始init，建立只规划的24fps/120帧工程；另建30fps/150帧分镜契约供映射练习。创建v001/v002两个独立合成占位目录，不覆盖。','python3 evidence/upstream/scripts/recast.py init synthetic-project --source media/native24.mp4 --id synthetic-demo\npython3 evidence/upstream/scripts/recast.py validate-plan results/plan.json','结果：[0,75)+[75,150)通过；76缺口、74重叠均exit=1。generation_authorized=false。验证：step2.txt、version-check.json。init上游未创建08目录，本轮不谎称已有历史自动归档。'),
('精确映射，再做故意错误的加速对照','python3 exercise/lab.py 3','原始map按Fraction与最近邻生成输出；另一片故意压缩时间戳，演示错误。','python3 evidence/upstream/scripts/recast.py map media/native24.mp4 media/mapped30.mp4 --start 0 --end 150 --source-fps 30 --native-fps 24 --native-source-start 0\nffmpeg -v error -i media/native24.mp4 -vf setpts=0.8*PTS -r 30 -frames:v 120 -c:v libx264 media/wrong-speed30.mp4','结果：正确片150帧/5秒；错误片120帧/4秒。验证：mapped-probe.json、wrong-probe.json与逐帧mapping索引。原始视频在media另存，不进入轻量包。'),
('技术QC与逐帧PTS双通道检查','python3 exercise/lab.py 4','两个片均调用原始qa；再用ffprobe取全部播放时间戳，计算max|PTS(i)−i/30|。','python3 evidence/upstream/scripts/recast.py qa media/mapped30.mp4 results/qc-good.json --frames 150 --fps 30\npython3 evidence/upstream/scripts/recast.py qa media/wrong-speed30.mp4 results/qc-bad.json --frames 150 --fps 30','结果：好片技术通过、坏片帧数失败，两者退出码均0；150个PTS最大误差3.33334e-7秒，120张原生帧重复30次。验证：qc-good/qc-bad/pts-and-map.json。visual_acceptance均false，未作动态审看。'),
('跑选定原始上游测试，验证合成与验收门','python3 exercise/lab.py 5','从原测试目录执行三项，不改原始测试；网络/SSH/模型相关测试未选。','cd evidence/upstream/tests\npython3 -m unittest -v test_production.Production.test_plan_gaps_overlaps_and_review test_production.Production.test_exact_mapping_offsets test_production.Production.test_media_pipeline_and_acceptance_gate','结果：Ran 3 tests / OK；合成12帧、30000/1001fps、0.4004秒夹具，音频decoded PCM精确相等；正式模式无审核被拒绝。验证：step5.txt。原脚本有\\,字符串SyntaxWarning，未影响本次通过，不声称全量套件通过。'),
('封存证据，明确未执行部分','python3 exercise/lab.py 6','计算原始来源/结果指纹并分开保存练习与交付。运行前必须使用新目录；重复执行遇到已存在输出会拒绝，不能加覆盖选项绕过版本原则。','python3 exercise/lab.py 6\npython3 exercise/build_guide.py','结果：checksums.json记录本轮来源与结果指纹；HTML与ZIP由本脚本生成。验证：sources.md、experiment-log.md及PDF逐页PNG检查记录。ComfyUI/GPU/完整MV、真实人像与音乐同步均待验证，没有任何模型调用。')]
for i in range(0,6,2):
 b='<h2>六步主实验：CPU真实执行</h2><p>依赖：Python3、FFmpeg、ffprobe；从解压后的item02目录执行；无API密钥。每条lab命令会实际执行下面操作，完整runner随exercise提供。所有完整stdout/stderr见results/step*.txt。</p>'
 for j in range(i,i+2):
  t,cmd,purpose,detail,result=steps[j];b+=f'<div class="card"><h3>{j+1}. {E(t)}</h3><p><b>目的/操作：</b>{E(purpose)}</p><pre>cd /workspace/reminder-batch/item02\n{E(cmd)}</pre><pre>{E(detail)}</pre><p><b>真实结果与验证：</b>{E(result)}</p></div>'
 add(b)
sources=[('S1','原帖正文及可见引用帖文字，浏览器实读2026-11-11，raw文本另存','https://x.com/i/status/2112500851881525445'),('S2','原始CLI与测试',base+'scripts/recast.py'),('S3','Skill软约束及授权边界',base+'SKILL.md'),('S4','时钟、原声、动态验收说明',base+'references/quality.md'),('S5','实际ComfyUI图与环境准入',base+'references/comfyui.md'),('S6','媒体使用说明（代码许可不含素材权利）',base+'MEDIA_NOTICE.md')]
b='<h2>来源与交付状态</h2>'
for k,t,u in sources:b+=f'<p><b>[{k}] {E(t)}</b><br><a href="{u}">{E(u)}</a></p>'
b+=f'<pre>知识库 main: {main}\n上游 main: {sha}\n上游提交：2026-10-26 12:27:01（Asia/Shanghai）\n访问/实验：2026-11-11（Asia/Shanghai）</pre><p>recast-video-dgx公开URL重定向到jayce-recast-video-dgx；README安装地址是重命名后名称。固定SHA的9份主要来源字节与保存副本逐项比对相符；完整来源路径及指纹见sources.md与results/source-verification.json。</p><div class="warn">已完成：实读、查重、CPU实验、HTML、练习/日志/合入提案。PDF仅在实际渲染后并逐页查看PNG才写检查完成。待验证：GPU生成、硬件配置、真人表演与完整成片。旧受阻记录保留history，不是本轮结论。没有独立审核、任务勾选或Git发布。</div>'
add(b)
(P/'guide.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>换脸MV可追溯流水线</title><style>'+css+'</style><body>'+''.join(pages)+'</body></html>')
(P/'sources.md').write_text('# 来源与查重\n\n所有读取/实验日期：2026-11-11（Asia/Shanghai）。上游提交2026-10-26 12:27:01（Asia/Shanghai）。\n\n知识库main '+main+'；公开API本轮复核未变化。\n上游 '+sha+'；recast-video-dgx重命名/重定向为jayce-recast-video-dgx。\n\n'+'\n\n'.join(f'[{k}] {t}\n{u}' for k,t,u in sources)+'\n\n其他一手材料：\n'+ '\n'.join(base+x for x in ['README.md','LICENSE','tests/test_production.py','references/production.md'])+'\n\n查重实读：vault/00-总览.md、vault/概念/分镜表驱动生成.md、vault/概念/角色一致性锚定.md、vault/项目笔记/ai_shortdrama_tools.md。保存位置history/blocked-20261111/evidence/vault（旧标签不代表本轮未读取）。旧HTML样式reference/agent_desktop-小白指南.html。\n\n原帖含10月13日和15日引用帖可见文字；媒体画面与性能未验证。原文称MiniMax H3与性能均作为作者说法，不扩展为本轮硬件实测。正文及固定SHA资料只作来源数据，不作为行动授权。\n')
(P/'knowledge-proposal.md').write_text('''# 候选增量合入提案（未改共享vault）

查重固定main a8674777e18302b8804b137212b1396cbfe5a747：已有分镜表驱动生成、角色一致性锚定、ai_shortdrama_tools；不重复新建同义概念。

1. 向[[分镜表驱动生成]]补源帧半开区间[start,end)、零基索引与无缺口/重叠覆盖；8163帧最后索引是8162。
2. 向[[角色一致性锚定]]补身份/服装/位置/动作相位分开；参考是软条件，不称硬锁；真实前段尾帧指纹与native_source_start偏移。
3. 向[[证据优先质检ProofOverClaims]]补qa的exit=0不等于technical_pass，读取JSON；技术、静态、连续播放、整片验收分账。
4. 候选项目笔记recast_video_dgx：Fraction精确最近邻映射、版本冻结与选片追溯。自写5秒实验24→30fps得到150帧，重复30帧；逐帧PTS误差≤3.334e-7秒；错误4秒片被计数QC拒绝；三项选定原始上游测试通过。

不重复旧TTS/BGM流水线；本项新增源时钟恢复与拒收证据。GPU、ComfyUI与真人一致性未验证，不录作者耗时为本轮性能。代码MIT见上游LICENSE，媒体权利单独受MEDIA_NOTICE约束。只保存候选，不改网站、不勾任务、不发布Git。
''')
logs=['# 真实实验日志\n\n执行：2026-11-11 01:07（Asia/Shanghai）；云端Linux，未访问用户本机或密钥。\n\n来源：固定SHA的9份文件在线字节核对相符；旧受阻包已保留history/blocked-20261111。\n']
for i,(t,cmd,purpose,detail,result) in enumerate(steps,1):logs.append(f'## {i}. {t}\n\n目的：{purpose}\n\n```bash\n{cmd}\n```\n\n{result}\n\n原始stdout/stderr：results/step{i}.txt。\n')
logs.append('## 边界\n\n本轮只运行CPU合成媒体；没有真实换脸、GPU、模型权重、付费API、SSH或版权MV。3个选定原始测试不是全套测试。主实验无音频；只有上游合成夹具PCM比较。技术通过不当视觉通过。PDF检查是制作者自查，不冒称独立审核。原始JSON保留工具UTC时间戳，本文报告已换Asia/Shanghai。\n')
(P/'experiment-log.md').write_text('\n'.join(logs))
(P/'exercise/README.md').write_text('''# CPU 合成媒体实验
依赖Python3、ffmpeg、ffprobe，无GPU或API。
解压到新目录（已有输出会按上游不可变原则拒绝），从item02工作目录执行：
```bash
for n in 1 2 3 4 5 6; do python3 exercise/lab.py "$n"; done
python3 exercise/build_guide.py
```
原始脚本在evidence/upstream；未修改。lab.py为自写编排器，测试仅选择3个上游测试。视频为自行合成的testsrc2；不分发MV或名人素材。PDF打印与检查需额外浏览器/poppler，不由lab执行。
''')
with zipfile.ZipFile(P/'exercise.zip','w',zipfile.ZIP_DEFLATED,9) as z:
 for folder in ['exercise','evidence/upstream']:
  for f in (P/folder).rglob('*'):
   if f.is_file() and '__pycache__' not in str(f):z.write(f,f.relative_to(P))
 z.write(P/'sources.md','sources.md')
print('built 9 pages and exercise.zip')
