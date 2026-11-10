# 合成订单的形式化验收合同（候选，不是已注册技能）

## 验证什么
当前支付有效的订单才能处于shipped状态：NoUnpaidShipment。TypeOK仅约束变量取值。本次覆盖自编合成订单，不覆盖任何真实支付产品，也没有实际安装/调用pstack插件。

## 代码—模型对应
|TLA+动作|Python参考实现|原子边界|
|---|---|---|
|Init|State()|paid=false, shipPhase=new, checkedPaid=false|
|Pay|pay|若未支付且未发货，把paid设true|
|CheckPayment|check_payment|读取paid并缓存checkedPaid，阶段改checked|
|Refund|refund|若paid且未发货，把paid改false|
|ShipBug|ship(fixed=False)|只根据阶段和旧快照修改为shipped|
|ShipFixed|ship(fixed=True)|额外检查实时paid，守卫与修改视作同一原子步骤|
|Done|successors的终态分支|完成后保持全部变量，不关闭死锁检查|

所有函数在order_reference.py，动作在models/OrderCore.tla。OrderMany把相同规则提升成按订单ID索引的函数。多订单互相独立，没有共享库存或金额总和。每个函数是合成原子转移，不据此声称实际业务原子性；Python/TLC对照是经验交叉检查，不是精化证明。

## 边界与未覆盖
- paid是当前支付有效性，不是“历史上曾支付”。两版都禁止发货后退款；真实售后流程需要重写业务状态语义，不得偷偷改弱规则。
- 单订单粗候选12种组合，固定版可达5；多订单固定N=1/2/3，实际分别5/25/125，未检查所有N。
- 不含消息重复、持久化、崩溃、网络、真实退款/付款/发货副作用、金额或资金守恒。
- 只检查已配置安全不变量；没有PROPERTY活性、公平性、实时期限或独立死锁变异验收。

## 一条复跑命令
先在包根运行python3 exercise/setup_tools.py（下载到本目录，固定版本/哈希），再：
```bash
cd exercise
python3 run_labs.py all
```
该命令真实调用TLC，不是Python模拟TLC。bug与mutant期望TLC退出12；驱动确认NoUnpaidShipment违反后整体返回0。fixed与各Orders边界要求TLC退出0且队列0。任何非预期退出、统计不符、重放不符都会使驱动报错。

## 判读证据
1. results/bug-stdout.txt必须包含Pay→CheckPayment→Refund→ShipBug的四转移反例。
2. fixed-summary.json必须生成8、不同5、队列0；不要把generated当不同状态。
3. Orders1/2/3需分别5/25/125不同状态；mutant需再次失败，不可删不变量或禁退款。
4. replay.json需显示合成Python的逐步可行性、fixed阻断末步、固定版DOT全部状态集合与Python枚举相同；没有比较/证明全部真实产品行为。
5. 变异产生单独模型，不改固定版；交付前已再次运行fixed成功。
6. 结果阅读可参照pstack /statechart手册的反例表达原则，但本合同不安装或冒充执行该插件。这里只执行自己的TLC命令；官方脚本的mise下载/渲染流程未执行。

## 同步基线与维护
本scratch没有Git提交，coverage-manifest.json以SHA256记录当前合成参考实现、模型与驱动。pstack官方SHA仅固定方法来源，不是订单代码sync commit。后续改变覆盖文件时先读差异、核对守卫与原子边界，再按代码更新模型；只有承诺确实有意改变并给出业务证据时才能改性质。不得先看哪个改动能变绿再倒改模型。

结果应分in sync、updated、bug、blocked；发生blocked不前移同步基线。若将来合入真实Git工程，再由协调者记录该工程的真正同步commit，本worker不创建虚构提交。
