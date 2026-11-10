# 真实实验日志

执行：2026-11-11 01:07（Asia/Shanghai）；云端Linux，未访问用户本机或密钥。

来源：固定SHA的9份文件在线字节核对相符；旧受阻包已保留history/blocked-20261111。

## 1. 建立可控输入，不碰私人或版权素材

目的：生成5秒testsrc2并用原始probe探测。底层完整生成命令：

```bash
python3 exercise/lab.py 1
```

结果：120帧，24/1fps，5.000000秒，320×180，无音轨。验证：results/native-probe.json与step1.txt；全部解码计数，不信播放器。

原始stdout/stderr：results/step1.txt。

## 2. 原始目录骨架与分镜/版本负例

目的：调用原始init，建立只规划的24fps/120帧工程；另建30fps/150帧分镜契约供映射练习。创建v001/v002两个独立合成占位目录，不覆盖。

```bash
python3 exercise/lab.py 2
```

结果：[0,75)+[75,150)通过；76缺口、74重叠均exit=1。generation_authorized=false。验证：step2.txt、version-check.json。init上游未创建08目录，本轮不谎称已有历史自动归档。

原始stdout/stderr：results/step2.txt。

## 3. 精确映射，再做故意错误的加速对照

目的：原始map按Fraction与最近邻生成输出；另一片故意压缩时间戳，演示错误。

```bash
python3 exercise/lab.py 3
```

结果：正确片150帧/5秒；错误片120帧/4秒。验证：mapped-probe.json、wrong-probe.json与逐帧mapping索引。原始视频在media另存，不进入轻量包。

原始stdout/stderr：results/step3.txt。

## 4. 技术QC与逐帧PTS双通道检查

目的：两个片均调用原始qa；再用ffprobe取全部播放时间戳，计算max|PTS(i)−i/30|。

```bash
python3 exercise/lab.py 4
```

结果：好片技术通过、坏片帧数失败，两者退出码均0；150个PTS最大误差3.33334e-7秒，120张原生帧重复30次。验证：qc-good/qc-bad/pts-and-map.json。visual_acceptance均false，未作动态审看。

原始stdout/stderr：results/step4.txt。

## 5. 跑选定原始上游测试，验证合成与验收门

目的：从原测试目录执行三项，不改原始测试；网络/SSH/模型相关测试未选。

```bash
python3 exercise/lab.py 5
```

结果：Ran 3 tests / OK；合成12帧、30000/1001fps、0.4004秒夹具，音频decoded PCM精确相等；正式模式无审核被拒绝。验证：step5.txt。原脚本有\,字符串SyntaxWarning，未影响本次通过，不声称全量套件通过。

原始stdout/stderr：results/step5.txt。

## 6. 封存证据，明确未执行部分

目的：计算原始来源/结果指纹并分开保存练习与交付。运行前必须使用新目录；重复执行遇到已存在输出会拒绝，不能加覆盖选项绕过版本原则。

```bash
python3 exercise/lab.py 6
```

结果：checksums.json记录本轮来源与结果指纹；HTML与ZIP由本脚本生成。验证：sources.md、experiment-log.md及PDF逐页PNG检查记录。ComfyUI/GPU/完整MV、真实人像与音乐同步均待验证，没有任何模型调用。

原始stdout/stderr：results/step6.txt。

## 边界

本轮只运行CPU合成媒体；没有真实换脸、GPU、模型权重、付费API、SSH或版权MV。3个选定原始测试不是全套测试。主实验无音频；只有上游合成夹具PCM比较。技术通过不当视觉通过。PDF检查是制作者自查，不冒称独立审核。原始JSON保留工具UTC时间戳，本文报告已换Asia/Shanghai。

## PDF交付复核

2026-11-11 01:10（Asia/Shanghai）：实际Chrome打印A4共9页，全部转PNG并Read逐张查看，已修正首版空白页，最终无裁切重叠。详细qa/pdf-review.md；本轮仅制作者自查。
