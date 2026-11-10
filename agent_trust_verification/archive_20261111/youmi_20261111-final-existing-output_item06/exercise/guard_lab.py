"""自写反例/有限状态枚举；不安装插件、不读私密记录、不进行真实发送。"""
from pathlib import Path
from collections import deque
import json,subprocess,unittest,argparse,re
ROOT=Path(__file__).resolve().parents[1];EX=ROOT/'exercise';OUT=ROOT/'results';TSC=EX/'node_modules/typescript/bin/tsc'
def run(args):
 r=subprocess.run(args,cwd=EX,capture_output=True,text=True);return {'command':args,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
def emit(n,x):
 OUT.mkdir(exist_ok=True);(OUT/(n+'.json')).write_text(json.dumps(x,ensure_ascii=False,indent=2));print(json.dumps(x,ensure_ascii=False,indent=2))
def compile(file,emit=False):return run(['node',str(TSC),'--strict','--target','ES2022','--module','commonjs']+(['--outDir',str(OUT/'compiled')]if emit else['--noEmit'])+[file])
def scan(source):return bool(re.search(r'\bas\s+any\b',source))
def explore(safe):
 initial=(False,0);q=deque([initial]);paths={initial:[]}
 while q:
  a,n=q.popleft();nexts=[('approve',(True,n))]
  if n<2 and(not safe or(a and n==0)):nexts.append(('send',(a,n+1)))
  for action,s in nexts:
   if s not in paths:paths[s]=paths[(a,n)]+[action];q.append(s)
 return {'safe_model':safe,'states':len(paths),'states_and_shortest_paths':[{'approved':s[0],'delivered':s[1],'trace':path}for s,path in paths.items()],'violations':[{'state':list(s),'trace':path}for s,path in paths.items()if(s[1]>0 and not s[0])or s[1]>1],'bound':'count<=2, no revocation/crash/network/real approval'}
def legacy():
 r=compile('legacy.ts',True);assert r['exit']==0;v=run(['node',str(OUT/'compiled/legacy.js')]);emit('legacy',{'compiler':r,'runtime':v,'meaning':'逻辑非法组合在宽松结构里可编译，负对照'})
def types():
 good=compile('fixed.ts');bad=compile('negative.ts');assert good['exit']==0 and bad['exit']!=0 and'TS2345'in bad['stdout'];emit('types',{'fixed':good,'negative_expected_failure':bad})
def runtime():
 r=compile('fixed.ts',True);assert r['exit']==0;x=run(['node',str(OUT/'compiled/fixed.js')]);m=compile('mutant.ts');flag=scan((EX/'mutant.ts').read_text());assert flag and m['exit']==0;emit('runtime',{'run':x,'mutant_compiler':m,'local_static_scan_mutant_rejected':flag,'fixed_scan_rejected':scan((EX/'fixed.ts').read_text()),'note':'静态扫描为自写单规则，不称ESLint；receipt完全合成无transport'})
def unsafe():
 r=explore(False);assert r['violations'];emit('unsafe-model',r)
def guarded():
 r=explore(True);assert not r['violations'];emit('guarded-model',r)
class Tests(unittest.TestCase):
 def test_bad_states(self):self.assertEqual(explore(False)['states'],6)
 def test_good_states(self):self.assertEqual(explore(True)['states'],3)
 def test_no_good_violation(self):self.assertEqual(explore(True)['violations'],[])
 def test_shortest(self):self.assertEqual(explore(False)['violations'][0]['trace'],['send'])
 def test_double_send(self):self.assertTrue(any(v['state'][1]==2 for v in explore(False)['violations']))
 def test_no_double_safe(self):self.assertTrue(all(v['delivered']<=1 for v in explore(True)['states_and_shortest_paths']))
 def test_no_early_safe(self):self.assertTrue(all(v['approved']for v in explore(True)['states_and_shortest_paths']if v['delivered']))
 def test_any_lint(self):self.assertTrue(scan('input as any'))
 def test_plain(self):self.assertFalse(scan('const anyValue = 1'))
 def test_real_mutant(self):self.assertTrue(scan((EX/'mutant.ts').read_text()))
 def test_real_fixed(self):self.assertFalse(scan((EX/'fixed.ts').read_text()))
 def test_version_pin(self):self.assertEqual(json.loads((EX/'node_modules/typescript/package.json').read_text())['version'],'5.9.3')
def test():unittest.main(argv=['guard_lab'],verbosity=2)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('step',choices=['legacy','types','runtime','unsafe','guarded','test']);a=p.parse_args();globals()[a.step]()
