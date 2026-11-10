"""自写runner；AST只装载已审阅原始纯函数/文件工具，绝不执行dotenv/OpenAI/原主循环。"""
from pathlib import Path
import ast,typing,json,inspect,hashlib,argparse,os,unittest
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results';SOURCE=ROOT/'coding_agent_from_scratch.py'
NAMES={'resolve_abs_path','read_file_tool','list_files_tool','edit_file_tool','extract_tool_invocations'}
def save(name,obj):
 OUT.mkdir(exist_ok=True);(OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n');print(json.dumps(obj,ensure_ascii=False,indent=2))
def load():
 tree=ast.parse(SOURCE.read_text());parts=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in NAMES];assert len(parts)==5
 scope={'Path':Path,'json':json,'List':typing.List,'Dict':typing.Dict,'Any':typing.Any,'Tuple':typing.Tuple}
 exec(compile(ast.Module(body=parts,type_ignores=[]),str(SOURCE),'exec'),scope);return scope
F=load()
def manifest():
 names=['source-post.json','course-home.html','course-calendar.txt','course2026-source-fragment.txt','transcript-0924.txt','transcript-1001.txt','coding_agent_from_scratch.py'];save('manifest.json',[{'file':n,'bytes':len((b:=(ROOT/n).read_bytes())),'sha256':hashlib.sha256(b).hexdigest()}for n in names])
def inspect_source():
 tree=ast.parse(SOURCE.read_text());reg=next(x.value for x in tree.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='TOOL_REGISTRY' for t in x.targets));names=[ast.literal_eval(k) for k in reg.keys]
 save('inspection.json',{'physical_lines':len(SOURCE.read_text().splitlines()),'registry':names,'has_bash':'bash' in names,'selected_functions':sorted(NAMES),'global_api_initialization_skipped':True})
def parsing():
 cases={'normal':'tool: read_file({"filename":"demo.txt"})','trailing':'tool: read_file({"filename":"demo.txt"}) SURPLUS','array':'tool: read_file([1,2])','unknown':'tool: remove_everything({})','malformed':'tool: read_file({broken})'}
 save('parser.json',{name:F['extract_tool_invocations'](v) for name,v in cases.items()})
def file_tools():
 work=ROOT/'scratch';work.mkdir(exist_ok=True);file=work/'demo.txt';file.write_text('alpha alpha\n');r1=F['edit_file_tool'](str(file),'alpha','beta');content=F['read_file_tool'](str(file));assert content['content']=='beta alpha\n';r2=F['edit_file_tool'](str(file),'missing','no');r3=F['edit_file_tool'](str(file),'','fresh\n');assert file.read_text()=='fresh\n'
 save('file-tools.json',{'replace_first':r1,'read_after_replace':content,'missing_old':r2,'empty_old':r3,'final_content':file.read_text()})
def replay():
 # Deterministic scripted responses; not a model and not the original infinite loop.
 file=ROOT/'scratch/replay.txt';script=[f'tool: edit_file({json.dumps({"path":str(file),"old_str":"","new_str":"answer=42"})})',f'tool: read_file({json.dumps({"filename":str(file)})})','Finished: answer=42'];events=[]
 tools={'edit_file':F['edit_file_tool'],'read_file':F['read_file_tool']}
 for step,response in enumerate(script,1):
  if step>4:raise RuntimeError('budget')
  calls=F['extract_tool_invocations'](response)
  if not calls:events.append({'step':step,'assistant':response,'stop':True});break
  for name,args in calls:
   assert name in tools and isinstance(args,dict);events.append({'step':step,'tool':name,'result':tools[name](**args)})
 assert file.read_text()=='answer=42';save('replay.json',{'scripted_model':True,'max_steps':4,'observed_steps':len(events),'events':events,'artifact':file.read_text()})
class Tests(unittest.TestCase):
 def test_normal(self):self.assertEqual(F['extract_tool_invocations']('hello'),[])
 def test_malformed(self):self.assertEqual(F['extract_tool_invocations']('tool: x({broken})'),[])
 def test_array_accepted(self):self.assertEqual(F['extract_tool_invocations']('tool: x([1])')[0][1],[1])
 def test_unknown_accepted(self):self.assertEqual(F['extract_tool_invocations']('tool: unknown({})')[0][0],'unknown')
 def test_trailing_accepted(self):self.assertEqual(len(F['extract_tool_invocations']('tool: x({})garbage')),1)
 def test_missing_closer_accepted(self):self.assertEqual(len(F['extract_tool_invocations']('tool: x({}')),1)
 def test_absolute_not_sandbox(self):self.assertEqual(F['resolve_abs_path']('/tmp/nonexistent-public-test'),Path('/tmp/nonexistent-public-test'))
 def test_relative_can_leave_scratch(self):
  prior=os.getcwd();os.chdir(ROOT/'scratch')
  try:self.assertEqual(F['resolve_abs_path']('../not-read.txt'),ROOT/'not-read.txt')
  finally:os.chdir(prior)
 def test_docstring(self):self.assertIn('first occurrence',F['edit_file_tool'].__doc__)
def test():unittest.main(argv=['course_lab'],verbosity=2)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('step',choices=['manifest','inspect_source','parsing','file_tools','replay','test']);a=p.parse_args();globals()[a.step]()
