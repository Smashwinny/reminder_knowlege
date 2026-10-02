# -*- coding: utf-8 -*-
"""实验B：复刻仓库的双低转债选股逻辑
原仓库路线: datahub/jisilu.py 登录集思录 -> 爬 cb_list_new -> MySQL -> trader/auto_trader.py 按'可转债价格'排序选最低价轮动。
本实验: 1) 先诚实实测原接口(不登录)是否还能匿名访问; 2) 用合成转债快照复刻'双低 = 价格 + 转股溢价率(百分数)'选股逻辑,
        并对比'纯低价'与'双低'两种选法的差异(为什么低价策略会踩可转债强赎坑)。
"""
import datetime
import json
import os

import pandas as pd

pd.set_option('display.width', 200)
pd.set_option('display.max_columns', 20)

OUT_DIR = os.path.dirname(__file__)


def try_jisilu_raw():
    """诚实实测：原仓库依赖的集思录 cb_list_new 接口，2026 年不登录还能不能匿名拿全量数据。"""
    import requests
    url = 'https://www.jisilu.cn/data/cbnew/cb_list_new/?___jsl=LST___t={}'.format(
        int(datetime.datetime.now().timestamp() * 1000))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.jisilu.cn/data/cbnew/',
    }
    try:
        r = requests.post(url, headers=headers, timeout=15)
    except Exception as e:
        print(f'[实测] 集思录接口请求失败: {type(e).__name__}: {e}')
        return None
    print(f'[实测] 集思录 cb_list_new HTTP {r.status_code}, 响应前 200 字符:')
    print(' ', r.text[:200].replace('\n', ' '))
    try:
        data = r.json()
    except ValueError:
        print('[实测] 响应不是 JSON(多半是登录页/验证页 HTML) -> 判定: 匿名不可用')
        return None
    rows = data.get('rows')
    if not rows:
        print('[实测] JSON 无 rows 字段 -> 判定: 匿名拿不到数据')
        return None
    print(f'[实测] 拿到 {len(rows)} 条转债(匿名仅给前 30 条, 登录才给全量约 500 只), 字段为英文名: '
          f'bond_id/bond_nm/price/premium_rt/ytm_rt')
    df = pd.DataFrame([r['cell'] for r in rows])
    # 字段名映射到中文, 与原仓库 MySQL 表(tb_jsl_*)口径一致
    df = df.rename(columns={'bond_id': '转债代码', 'bond_nm': '转债名称',
                            'price': '转债价格', 'premium_rt': '转股溢价率',
                            'ytm_rt': '到期收益率'})
    for col in ('转债价格', '转股溢价率', '到期收益率'):
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df


def make_synthetic_bonds(n=30, seed=2026):
    """合成一版可转债快照(结构对齐集思录字段: 转债代码/转债名称/转债价格/转股溢价率/到期收益率)。
    特意埋两只'低价高溢价'的坑券, 演示纯低价选法 vs 双低选法的差异。"""
    import random
    rng = random.Random(seed)
    rows = []
    for i in range(n):
        price = round(rng.uniform(100, 150), 2)
        premium = round(rng.uniform(-2, 60), 2)
        rows.append({
            '转债代码': f'12{i:04d}',
            '转债名称': f'模拟转债{i:02d}',
            '转债价格': price,
            '转股溢价率': premium,
            '到期收益率': round(rng.uniform(-8, 4), 2),
        })
    df = pd.DataFrame(rows)
    # 坑券: 价格全场最低, 但溢价率高得离谱(正股早已跌破转股价, 靠债底撑着)
    df.loc[0] = ['123001', '坑券A(低价高溢价)', 102.0, 88.0, 3.5]
    df.loc[1] = ['123002', '坑券B(低价高溢价)', 103.5, 75.0, 3.2]
    return df


def main():
    print('=== 实验B：双低转债选股逻辑复刻 ===\n')

    raw = try_jisilu_raw()
    if raw is not None:
        raw["双低值"] = raw["转债价格"] + raw["转股溢价率"]  # premium_rt 已是百分数, 直接相加
        df = raw
        source = '集思录真实数据'
    else:
        df = make_synthetic_bonds()
        source = '合成快照(接口不可用后的兜底)'

    df["双低值"] = df["转债价格"] + df["转股溢价率"]  # 百分数口径直接相加

    print(f'\n[数据来源] {source}, 共 {len(df)} 只\n')

    # 选法1: 原仓库 auto_trader.py 的纯低价轮动 (sort_values by 可转债价格)
    low_price = df.sort_values('转债价格').head(5)
    print('[选法1] 纯低价 Top5 (原仓库 auto_trader.py 思路, 忽略溢价率):')
    print(low_price[['转债代码', '转债名称', '转债价格', '转股溢价率']].to_string(index=False))

    # 选法2: 双低 = 价格 + 100*溢价率
    double_low = df.sort_values('双低值').head(5)
    print('\n[选法2] 双低值 Top5 (价格与溢价率兼顾):')
    print(double_low[['转债代码', '转债名称', '转债价格', '转股溢价率', '双低值']].to_string(index=False))

    overlap = set(low_price['转债代码']) & set(double_low['转债代码'])
    print(f'\n[对比] 两种选法重合: {len(overlap)}/5; '
          f'纯低价名单里的坑券: {[n for n in low_price["转债名称"] if "坑券" in n] or "无"}')
    print('[结论] 纯低价会选中"价格低但溢价率 80%+"的债底券——弹性几乎为零, 只能吃到期收益; '
          '双低值同时惩罚高溢价, 是社区十年实盘经验压出来的核心单因子。')

    out_csv = os.path.join(OUT_DIR, 'double_low_result.csv')
    df.sort_values('双低值').to_csv(out_csv, index=False, encoding='utf-8-sig')
    print(f'\n[落盘] 完整排序已存 {out_csv}')


if __name__ == '__main__':
    main()
