# 离线海报模板实验

解压后在exercise上一级目录运行：
```bash
for s in init lint render verify economics; do python3 exercise/lab.py "$s" || exit; done
```
Python 3.13.5实测，仅标准库。源码lab.py为本worker自写教学代码；SVG路径、虚构品牌与短规格为本次演示。没有复制上游ComfyUI源码，没有执行作者的完整提示词，没有模型推理、API、客户数据或交易。

结构检查21项与5个拒收样本不构成独立审核或法律清算。经济参数全部为假设，平台费0不是现行费率结论。完整来源见同包sources.md；输出在out/，stdout在run.log。
