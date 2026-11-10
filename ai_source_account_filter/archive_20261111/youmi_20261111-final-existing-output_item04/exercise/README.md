# 可复现的零API实验
Python3.13标准库。本练习代码由worker自写，允许复制修改（MIT）。真实文章公开输入随包保存；X Article原作权利归原作者，使用请保留原链接。官方文档快照保留来源。不含密钥，不发网络请求。
```bash
python3 exercise/source_filter_lab.py manifest
python3 exercise/source_filter_lab.py audit
python3 exercise/source_filter_lab.py filtering
python3 exercise/source_filter_lab.py sensitivity
python3 exercise/source_filter_lab.py aging
python3 exercise/source_filter_lab.py test
```
在解压后的item04目录运行。命令写results/*.json；只有第2步计数真实文章，第3—5步均为明确合成样本。不会给真人账号打标签，也不会创建X列表/关注/定时任务。缺失=unknown；450为本练习离散化上限，非作者精确实现。首次emoji140误当人数的风险与修正至138行，完整保留在experiment-log.md。
