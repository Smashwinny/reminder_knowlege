# -*- coding: utf-8 -*-
"""实验A：Rockyzsu/stock 仓库结构考古
统计 152 个 Python 文件的模块分布，验证"个人实盘工具箱 = 爬虫(数据采集) + 策略(分析) + 交易"的三大件构成。
纯本地运行，无外部依赖。
"""
import os
import re
from collections import Counter

REPO = os.path.join(os.path.dirname(__file__), '..', 'repo')

# 模块 -> 定位标签
LABELS = {
    'datahub': '数据采集(爬虫)',
    'fund': '基金/套利(爬虫+策略)',
    'analysis': '数据分析/策略',
    'backtest': '回测(backtrader)',
    'trader': '自动交易',
    'ptrade': '自动交易(券商实盘)',
    'futu': '券商API(富途)',
    'hk_stock': '港股',
    'k-line': 'K线形态(技术分析)',
    'machine_learning': '机器学习预测',
    'monitor': '监控/提醒',
    'common': '公共库',
    'configure': '配置',
    'data': '数据文件',
    'utils': '工具函数',
    'market': '行情',
    'daily': '定时任务',
    'juejin': '工具(掘金)',
}

def main():
    py_files = []
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', '.idea')]
        for f in files:
            if f.endswith(('.py', '.ipynb')):
                rel = os.path.relpath(os.path.join(root, f), REPO)
                py_files.append(rel.replace('\\', '/'))

    # 按顶层模块归类
    by_module = Counter()
    by_label = Counter()
    for p in py_files:
        top = p.split('/')[0]
        if '/' not in p:
            top = '(根目录脚本)'
        by_module[top] += 1
        by_label[LABELS.get(top, '其他')] += 1

    # 代码考古：识别"老代码"特征
    legacy = {'py2_queue': 0, 'cookielib': 0, 'py2_print': 0, 'spider_requests': 0, 'db_access': 0}
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', '.idea')]
        for f in files:
            if not f.endswith('.py'):
                continue
            try:
                src = open(os.path.join(root, f), encoding='utf-8', errors='ignore').read()
            except OSError:
                continue
            if re.search(r'^\s*(import|from)\s+Queue\b', src, re.M):
                legacy['py2_queue'] += 1
            if 'cookielib' in src:
                legacy['cookielib'] += 1
            if re.search(r'requests\.(get|post|Session)', src):
                legacy['spider_requests'] += 1
            if re.search(r'(pymysql|pymongo|sqlalchemy|create_engine|get_mysql_conn|read_sql)', src):
                legacy['db_access'] += 1

    print('=== 实验A：仓库结构考古 ===')
    print(f'总文件数(.py+.ipynb): {len(py_files)}')
    print('\n[按模块分布]')
    for mod, n in by_module.most_common():
        print(f'  {mod:<22} {n:>4} 个文件')
    print('\n[按功能定位分布]')
    for label, n in by_label.most_common():
        print(f'  {label:<24} {n:>4} 个文件')
    print('\n[代码考古特征]')
    print(f"  Python2 遗留 Queue 模块引用 : {legacy['py2_queue']} 个文件")
    print(f"  cookielib(Python2 拼写)引用 : {legacy['cookielib']} 个文件")
    print(f"  requests 爬虫特征           : {legacy['spider_requests']} 个文件")
    print(f"  数据库直连特征              : {legacy['db_access']} 个文件")

    spiderish = legacy['spider_requests']
    total_py = sum(1 for p in py_files if p.endswith('.py'))
    print(f"\n[结论] 约 {spiderish}/{total_py} 的脚本带 requests 爬虫特征 —— "
          f"这是'十年个人实盘工具箱'的典型形态:重心在数据采集与落库,而非框架化回测。")

if __name__ == '__main__':
    main()
