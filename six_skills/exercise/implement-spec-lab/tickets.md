# Ticket 任务图（非步骤清单，是图）

T1-tokenize  [无阻塞，frontier 初始成员]
  实现 tokenize(text) -> list[str]：仅保留字母、小写化
T2-report  [blocked by T1]
  实现 report(words, n) -> list[(word, count)]：按次数降序、同频按字母序
T3-cli  [blocked by T1, T2]
  main：argparse 接文件路径与 -n，打印排行
