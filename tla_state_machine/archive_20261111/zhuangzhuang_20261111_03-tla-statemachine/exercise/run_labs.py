#!/usr/bin/env python3
"""真实执行TLC；保留预期失败退出码；只处理合成订单。"""
from pathlib import Path
import subprocess,json,hashlib,re,sys,os,shutil
from dataclasses import asdict
from order_reference import State,successors,safe,graph
E=Path(__file__).resolve().parent;B=E.parent;M=E/'models';R=E/'results';R.mkdir(exist_ok=True)
java=os.environ.get('JAVA') or shutil.which('java') or str(next((B/'tools').glob('jdk-*/bin/java')))
jar=Path(os.environ.get('TLA2TOOLS_JAR',str(B/'tools/tla2tools.jar'))).resolve()
def run(name,module,config,expected_rc,expected_distinct=None):
    cmd=[java,'-Xmx256m','-XX:+UseParallelGC','-jar',str(jar),'-workers','1','-fp','0','-config',config,'-metadir',str(R/f'{name}-meta'),'-dump','dot,actionlabels',str(R/f'{name}-graph.dot'),module]
    (R/f'{name}-command.json').write_text(json.dumps({'cwd':str(M),'argv':cmd},ensure_ascii=False,indent=2))
    print('实际命令：',subprocess.list2cmdline(cmd),'\n工作目录：',M,flush=True)
    p=subprocess.run(cmd,cwd=M,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60)
    (R/f'{name}-stdout.txt').write_text(p.stdout);print(p.stdout);print('TLC实际OS退出码：',p.returncode)
    assert p.returncode==expected_rc,(name,p.returncode)
    found=re.search(r'([\d,]+) states generated, ([\d,]+) distinct states found, ([\d,]+) states left on queue',p.stdout)
    assert found,p.stdout
    generated,distinct,queue=(int(x.replace(',','')) for x in found.groups())
    if expected_distinct is not None:assert distinct==expected_distinct,(name,distinct)
    if expected_rc==12:assert 'Invariant NoUnpaidShipment is violated' in p.stdout
    else:assert 'Model checking completed. No error has been found.' in p.stdout and queue==0
    out={'name':name,'os_exit_code':p.returncode,'generated':generated,'distinct':distinct,'queue':queue,'completed':expected_rc==0,'meaning':'TLC有限模型检查；非任意规模证明或真实支付产品验收'}
    (R/f'{name}-summary.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print('核验：',json.dumps(out,ensure_ascii=False));return out

def bug():return run('bug','OrderBug.tla','OrderBug.cfg',12)
def fixed():return run('fixed','OrderFixed.tla','OrderFixed.cfg',0,5)
def scaling():
    return [run(f'orders{n}','OrderMany.tla',f'Orders{n}.cfg',0,5**n) for n in [1,2,3]]
def mutation():
    # 从固定版复制，去掉实时paid检查；保持配置中的不变量和退款前提不变。
    source=(M/'OrderFixed.tla').read_text();assert 'ShipFixed' in source
    mutant=source.replace('MODULE OrderFixed','MODULE OrderMutant').replace('ShipFixed','ShipBug');(M/'OrderMutant.tla').write_text(mutant)
    (M/'OrderMutant.cfg').write_text((M/'OrderFixed.cfg').read_text())
    return run('mutant','OrderMutant.tla','OrderMutant.cfg',12)
def parse_trace(text):
    out=[]
    for part in re.split(r'(?m)^State \d+: ',text)[1:]:
        fields={}
        for key,pat in [('paid',r'(?m)^/\\ paid = (TRUE|FALSE)$'),('shipPhase',r'(?m)^/\\ shipPhase = "(\w+)"$'),('checkedPaid',r'(?m)^/\\ checkedPaid = (TRUE|FALSE)$')]:
            m=re.search(pat,part);assert m,(key,part);fields[key]=m[1] if key=='shipPhase' else m[1]=='TRUE'
        out.append(State(**fields))
    return out

def replay():
    path=parse_trace((R/'bug-stdout.txt').read_text());assert len(path)==5,path;assert path[0]==State() and not safe(path[-1])
    actions=[]
    for a,b in zip(path,path[1:]):
        matches=[name for name,t in successors(a,False) if t==b];assert len(matches)==1;actions.append(matches[0])
    assert actions==['Pay','CheckPayment','Refund','ShipBug'],actions
    fixed_states,edges=graph(True);bug_states,_=graph(False);assert len(fixed_states)==5 and len(bug_states)==6;assert all(safe(s) for s in fixed_states)
    # 核对TLC固定版DOT的全部状态，而不只比较计数。
    dot=(R/'fixed-graph.dot').read_text();observed=[]
    for line in dot.splitlines():
        if 'label="' not in line or '->' in line:continue
        pairs={key:re.search(r'\b'+key+r' = (TRUE|FALSE|\\?"\w+\\?")',line) for key in ['paid','shipPhase','checkedPaid']}
        if all(pairs.values()):
            d={k:(v.group(1).replace('\\"','').replace('"','') if k=='shipPhase' else v.group(1)=='TRUE') for k,v in pairs.items()};observed.append(State(**d))
    assert set(observed)==fixed_states,(observed,dot)
    blocked=successors(path[-2],True);assert all(t!=path[-1] for _,t in blocked)
    result={'trace_actions':actions,'states':[asdict(s) for s in path],'transition_count':len(actions),'state_count':len(path),'python_fixed_reachable':len(fixed_states),'python_bug_full_reachable':len(bug_states),'fixed_TLC_DOT_equals_python_full_state_set':True,'fixed_blocks_bug_final_transition':True,'scope':'仅自编合成实现的逐步重放与状态集合交叉检查；非产品代码精化证明'}
    (R/'replay.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
    covered=['order_reference.py','models/OrderCore.tla','models/OrderBug.tla','models/OrderFixed.tla','models/OrderMany.tla','run_labs.py']
    (E/'coverage-manifest.json').write_text(json.dumps({'baseline_type':'云端scratch无Git提交，使用内容哈希；不要把pstack源SHA当合成订单同步提交','files':{p:hashlib.sha256((E/p).read_bytes()).hexdigest() for p in covered},'assumptions':['单步原子读写','发货后不允许退款；此限制在bug/fixed完全一致','单一币种/金额抽象为布尔paid','无网络、真实支付或数据库','多订单互相独立，无库存共享、重试次数或消息队列']},ensure_ascii=False,indent=2))
if __name__=='__main__':
    stage=sys.argv[1]
    if stage=='all':
        for fn in [bug,fixed,scaling,mutation,replay]:fn()
    else:assert stage in ['bug','fixed','scaling','mutation','replay'];globals()[stage]()
