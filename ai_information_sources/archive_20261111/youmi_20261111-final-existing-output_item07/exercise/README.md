# 七渠道离线练习
Python3.13标准库，无依赖、密钥或订阅。已保存的公开snapshots及source-manifest随exercise.zip附带；其中6页只是明确标注的WebFetch有限摘录，非完整HTML。
进入解压后的item07目录：
```bash
python3 exercise/source_flow_lab.py catalog
python3 exercise/source_flow_lab.py dedupe
python3 exercise/source_flow_lab.py evidence
python3 exercise/source_flow_lab.py ranks
python3 exercise/source_flow_lab.py cost
python3 exercise/source_flow_lab.py test
```
默认完全离线。fetch_public.py是本轮实际使用的公开下载器，非复现必须步骤；重跑会重新访问网页且可能403。固定实验请用随包快照，不改写日期。合成排名区间/报价不是网站数据或购买建议。论文ID识别只支持现代编号，未覆盖旧式arXiv ID。
