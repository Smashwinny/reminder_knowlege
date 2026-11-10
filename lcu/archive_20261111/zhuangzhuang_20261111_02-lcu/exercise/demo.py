#!/usr/bin/env python3
"""自编协议驱动。真实进程/JSON-RPC，桌面对象完全是内存模拟；非安全沙箱。"""
import json,sys,os,subprocess,selectors,time,pathlib,shutil,hashlib,platform,importlib.util
ROOT=pathlib.Path(__file__).resolve().parent;OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
NODE=shutil.which('node');checks=[]
def check(name,condition,value=None):
    if not condition:raise AssertionError((name,value))
    checks.append({'name':name,'pass':True,'observed':value});print('PASS',name,json.dumps(value,ensure_ascii=False))
class Client:
    def __init__(self,name,auto=True):
        self.seq=0;self.buf=b'';self.trace=(OUT/f'{name}-wire.jsonl').open('w');self.err=(OUT/f'{name}-stderr.txt').open('w')
        home=OUT/'empty-home';home.mkdir(exist_ok=True)
        self.p=subprocess.Popen([NODE,str(ROOT/'mock_mcp.mjs')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.err,env={'PATH':os.environ.get('PATH',''),'HOME':str(home),'LANG':'C.UTF-8'})
        self.sel=selectors.DefaultSelector();self.sel.register(self.p.stdout,selectors.EVENT_READ)
        if auto:
            self.init=self.call('initialize',{'protocolVersion':'2025-11-25','clientInfo':{'name':'本地教学驱动','version':'1'},'capabilities':{}})['result']
            self.send({'jsonrpc':'2.0','method':'notifications/initialized'})
    def send(self,x):
        self.trace.write(json.dumps({'direction':'client_to_server','message':x},ensure_ascii=False)+'\n');self.trace.flush()
        self.p.stdin.write((json.dumps(x,ensure_ascii=False)+'\n').encode());self.p.stdin.flush()
    def raw(self,text):self.p.stdin.write(text.encode()+b'\n');self.p.stdin.flush();self.trace.write(json.dumps({'direction':'client_to_server','raw':text})+'\n');self.trace.flush()
    def receive(self):
        deadline=time.monotonic()+4
        while time.monotonic()<deadline:
            if b'\n' in self.buf:
                line,self.buf=self.buf.split(b'\n',1);x=json.loads(line)
                self.trace.write(json.dumps({'direction':'server_to_client','message':x},ensure_ascii=False)+'\n');self.trace.flush();return x
            if self.sel.select(max(0,deadline-time.monotonic())):
                data=os.read(self.p.stdout.fileno(),65536)
                if not data:raise RuntimeError('服务提前退出')
                self.buf+=data
        raise TimeoutError('协议响应超时')
    def call(self,method,params=None):
        self.seq+=1;self.send({'jsonrpc':'2.0','id':self.seq,'method':method,'params':params or {}});x=self.receive();assert x['id']==self.seq;return x
    def js(self,code):return self.call('tools/call',{'name':'js','arguments':{'code':code}})['result']
    def val(self,code):
        x=self.js(code);assert not x['isError'],x;return json.loads(x['content'][0]['text'])
    def close(self):
        self.p.stdin.close();rc=self.p.wait(timeout=4);self.sel.close();self.err.close();self.trace.close();assert rc==0
    def __enter__(self):return self
    def __exit__(self,*args):self.close()
def baseline():
    print('系统',platform.platform(),'Python',platform.python_version(),'Node',subprocess.check_output([NODE,'--version'],text=True).strip())
    up=ROOT.parent/'upstream'
    for p in ['adapters/host-guard.mjs','adapters/test/host-guard.test.mjs','tests/mcp_client.py','LICENSE']:
        data=(ROOT/'vendor'/p).read_bytes();same=(up/p).read_bytes()==data
        check('上游原样副本 '+p,same,hashlib.sha256(data).hexdigest())
    readme=(up/'README.md').read_text();check('当前README已明确不需要Python','no Python on any platform' in readme)
    print('范围声明：仅启动mock_mcp.mjs，不导入LCU启动器、不读取ChatGPT目录；这不是安全隔离证明。')
def protocol():
    with Client('protocol') as c:
        check('固定协议版本',c.init['protocolVersion']=='2025-11-25',c.init['protocolVersion'])
        check('初始化说明传回', '模拟' in c.init['instructions'],c.init['instructions'])
        tools=c.call('tools/list')['result']['tools'];check('公开工具恰好两个',[x['name'] for x in tools]==['js','js_reset'],[x['name'] for x in tools])
        check('工具schema为对象',all(x['inputSchema']['type']=='object' for x in tools))
        check('ping返回空对象',c.call('ping')['result']=={})
        check('模拟桌面明确非实机',c.val('cua.getState()')['actualDesktopAccess'] is False)
def state():
    with Client('state') as c:
        check('首次JS返回值',c.val('var counter = 40; counter + 2')==42,42)
        check('跨调用保留变量',c.val('counter += 1; counter')==41,41)
        check('先发现模拟应用',c.val('cua.getState().applications[0].id')=='demo.notes','demo.notes')
        r=c.val('var app = cua.getApp("demo.notes"); app.typeText("学习MCP"); app.click({elementId:"save"}); app.getState()')
        check('单次调用组合读写保存',r['text']=='学习MCP' and r['saved'] is True,r)
        check('后续调用复用app句柄',c.val('app.getState().text')=='学习MCP')
        image=c.val('app.getScreenshot()');check('截图仅模拟元数据',image['actualCapture'] is False,image)
        (OUT/'mock-note-snapshot.json').write_text(json.dumps(r,ensure_ascii=False,indent=2))
def reset():
    with Client('reset') as c:
        c.val('var app=cua.getApp("demo.notes"); var token="自造演示值"; app.typeText("A")')
        check('重置前变量存在',c.val('typeof token')=='string')
        r=c.call('tools/call',{'name':'js_reset','arguments':{}})['result'];check('reset返回成功',not r['isError'])
        check('reset清空JS变量',c.val('typeof token')=='undefined')
        check('reset不撤销外部模拟文档',c.val('cua.getApp("demo.notes").getState().text')=='A','A')
        r=c.js('cua.getApp("demo.notes").typeText("B"); throw new Error("故障注入")')
        check('半程失败带isError',r['isError'] is True,r)
        check('错误不回滚文档',c.val('cua.getApp("demo.notes").getState().text')=='AB','AB')
        c.val('cua.getApp("demo.notes").typeText("B")')
        check('盲重试产生重复副作用',c.val('cua.getApp("demo.notes").getState().text')=='ABB','ABB')
def negative():
    with Client('negative-pre',auto=False) as c:
        check('初始化前拒绝工具',c.call('tools/list')['error']['code']==-32002)
        check('协议版本不支持明确拒绝',c.call('initialize',{'protocolVersion':'2099-01-01'})['error']['code']==-32602)
        c.raw('{bad json');check('畸形JSON产生解析错误',c.receive()['error']['code']==-32700)
    with Client('negative') as c:
        check('未知方法错误',c.call('missing')['error']['code']==-32601)
        check('未知工具拒绝',c.call('tools/call',{'name':'turn_ended','arguments':{}})['error']['code']==-32602)
        check('缺code参数拒绝',c.call('tools/call',{'name':'js','arguments':{}})['error']['code']==-32602)
        check('模拟白名单拒绝未知App',c.js('cua.getApp("real.browser")')['isError'] is True)
        check('模拟坐标越界拒绝',c.js('cua.move({x:900,y:1})')['isError'] is True)
        r=c.js('while(true){}');check('同步循环80ms超时为工具错误',r['isError'] is True and 'timed out' in r['content'][0]['text'],r)
        check('超时后仍可执行',c.val('2+2')==4,4)
        check('console日志不污染stdout',c.val('console.log("只进stderr"); 7')==7,7)
        c.val('var localOnly=99')
        with Client('isolation') as d:check('另一进程看不到JS变量',d.val('typeof localOnly')=='undefined')
    stderr=(OUT/'negative-stderr.txt').read_text();check('真实stderr捕获日志','只进stderr' in stderr,stderr.strip())
def upstream():
    sys.path.insert(0,str(ROOT/'vendor/tests'));from mcp_client import Client as Original,text
    err=(OUT/'upstream-client-stderr.txt').open('w')
    c=Original([NODE,str(ROOT/'mock_mcp.mjs')],protocol_version='2025-11-25',env={'PATH':os.environ.get('PATH',''),'HOME':str(OUT/'empty-home')},stderr=err)
    try:
        check('上游轻客户端握手互通',c.initialization['protocolVersion']=='2025-11-25')
        check('上游客户端发现两个工具',len(c.call('tools/list',{})['tools'])==2)
        check('上游客户端跨调用状态',json.loads(text(c.js('var n=20; n')))==20 and json.loads(text(c.js('n+1')))==21)
        check('上游客户端接收isError',c.js('throw new Error("预期失败")',error=True)['isError'] is True)
    finally:c.close();err.close()
if __name__=='__main__':
    stage=sys.argv[1];assert stage in ['baseline','protocol','state','reset','negative','upstream'];globals()[stage]()
    (OUT/f'{stage}-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n');print(f'本组命名检查：{len(checks)} PASS；不是完整MCP合规或真实桌面验收。')
