# iOS 入口证据练习
Python 3 标准库。自写教学辅助程序，不是 Apple/Bot 实现。
从 item01 运行：
```bash
python3 exercise/voice_entry_lab.py manifest
python3 exercise/voice_entry_lab.py matrix
python3 exercise/voice_entry_lab.py negative
python3 exercise/voice_entry_lab.py test
python3 exercise/voice_entry_lab.py report
```
仅处理本目录公开来源与自造矩阵，不录音、不调用网络、不获取用户密钥。

## 打包后复现
2026-11-11 01:02（Asia/Shanghai）从exercise.zip全新解压至qa/repro，完整运行上述五步，退出0，结果与初跑一致；见experiment-log.md末节与qa/zip-repro-output.txt。
