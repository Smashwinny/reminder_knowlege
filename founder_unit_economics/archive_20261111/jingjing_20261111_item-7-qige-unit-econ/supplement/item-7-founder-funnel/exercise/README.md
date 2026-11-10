# 第 7 项练习：带标签的单位经济与漏斗敏感度

所有输入都带 `author_claim` 或 `teaching_assumption` 标签。作者自述的融资、GMV、课程收入不是测量值，融资也不计入利润。

```bash
python3 funnel.py
sha256sum funnel.py results.json sensitivity.csv
```

- 成功标准：标签完整、算术正确、27 组敏感度写出、转化率下降时利润下降、高压组合利润为负、退出码 0。
- 本模型不能用来宣传或复现投流、多店或高价课策略。
