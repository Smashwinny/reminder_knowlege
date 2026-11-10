"""官方HTML的真实无头浏览器键盘交互，不调用模型。"""
import pathlib,sys,json,hashlib
P=pathlib.Path(__file__).parent;sys.path.insert(0,str(P.parents[1]/'vendor'))
from playwright.sync_api import sync_playwright
from PIL import Image,ImageChops
mode=sys.argv[1]
if mode=='browser':
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/google-chrome',headless=True);pg=b.new_page(viewport={'width':1000,'height':800},reduced_motion='reduce');network=[];errors=[]
  pg.on('pageerror',lambda err:errors.append(str(err)));pg.route('http://**/*',lambda r:(network.append(r.request.url),r.abort()));pg.route('https://**/*',lambda r:(network.append(r.request.url),r.abort()))
  pg.goto((P/'upstream/examples/dial-indicator/dial-indicator-light.html').as_uri());stage=pg.locator('.iso-stage');stage.focus();rows=[]
  for key,want in [('Home',18),('ArrowLeft',14),('End',10)]:
   stage.press(key);pg.wait_for_function('(v)=>document.querySelector(".iso-stage").getAttribute("aria-valuenow")===String(v)',arg=want,timeout=10000);pg.wait_for_timeout(700);row={'key':key,'want':want,'aria':stage.get_attribute('aria-valuenow'),'readout':pg.locator('[data-readout]').inner_text(),'needle':pg.locator('[data-part="needle"]').get_attribute('d')};rows.append(row);pg.screenshot(path=str(P/f'pose-{want}.png'))
  out={'rows':rows,'errors':errors,'network_attempts':network,'paths':pg.locator('svg path').count()};(P/'browser-results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));b.close()
elif mode=='verify':
 r=json.loads((P/'browser-results.json').read_text());assert not r['errors'];assert not r['network_attempts'];assert r['paths']>30
 assert [int(x['aria']) for x in r['rows']]==[18,14,10];assert len(set(x['needle'] for x in r['rows']))==3
 assert ImageChops.difference(Image.open(P/'pose-18.png').convert('RGB'),Image.open(P/'pose-10.png').convert('RGB')).getbbox()
 print('PASS 6 checks: no JS errors, no HTTP attempts, path count, 3 readouts, 3 needle paths, different rendered poses; not a mechanical accuracy or pedagogy audit')
elif mode=='hash':
 for f in [P/'upstream/examples/dial-indicator/build.mjs',P/'upstream/kit/iso-kit.mjs',P/'upstream/examples/dial-indicator/dial-indicator-light.html']:
  print(hashlib.sha256(f.read_bytes()).hexdigest(),str(f.relative_to(P)))
