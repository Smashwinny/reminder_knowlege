# 实验日志：已执行不等于验收通过

日期2026-11-11（Asia/Shanghai）。环境Python3.13.5、Node24.22.1、Chrome156.0.8078.47。无付费模型、无硬件、无用户凭据；原构建固定286d56ccbbb924c10812fc5e6cabb11906454afc。

1. **已执行** `python3 fetch.py`：取回18个固定文件15,705,996字节，SHA256清单逐项保存；expected-manifest用于重放比对。
2. **已执行，通过结构断言** `python3 assets.py`：四个GLB头/长度/JSON块有效，147节点147网格，全部无skins/animations。仅外壳资源计数。
3. **已执行，通过函数断言** `node clock.cjs`：从原生产构建精确提取class T5，不是自造时钟。100ms/1000ms合成间隔HUD均120，dt0.05；不是实测FPS。
4. **已执行，完整模型验收不通过** `python3 browser.py studio`：真实Chrome运行原index/bundle的本地HTTP副本，内存响应额外注入harness；latest v3 Chrome退出0、API存在、成功GLB0/4、not ready，严格脚本非零退出。
5. **已执行，完整模型验收不通过** `python3 browser.py explode`：同样0/4且not ready。截图实看UI但中心无可见机器人，不冒称还原成功。

## 回归仪器与负面证据

原始index与bundle磁盘字节未改。注入仪器暂停自主requestAnimationFrame，中间回归暂时抑制renderer.render，最后恢复；不代表普通交互会话。初版1280×900/12s虚拟预算150秒超时；第二版结束清理卡住，约200秒主动终止隔离进程组；均保留失败记录。

较早v2：把4个ResourceTiming条目误当资源加载完成。警告实际上明确全部fetch失败。降级状态下32关节中29不同、4186对象局部位置移动、最大局部差619.5993434940839、收回残差0；注册项目14088只是构建表。步态字段先读walkPhase而非真实walkPhaseRad，缺字段导致断言失败，不能说步态冻结通过。较早截图仍中央无模型。

修订v3：使用不同GLB的HTTP200且encodedBodySize>0作为成功门槛，检查Fallback警告；修正walkPhaseRad。改为Python官方建议的ThreadingHTTPServer，30秒虚拟预算，仍0/4、未就绪，因此新姿势/步态回归未再进入。源构建完整视觉验收待验证，失败根因未确认。

最小同源fetch `/ok` 独立诊断返回FETCH_OK，说明不是所有localhost fetch均失败。官方Chrome CLI/线程服务器文档与有界检索记录见sources/research-notes.md。没有绕过网络/鉴权/安全检查。

## 待验证

完整GLB与可见机器人；修正字段后的行走/冻结；8视图全覆盖；普通交互、手机、高质量独立帧时间；作者模型生成30h、完整prompt/Blender创作工程；真实硬件/动力学/热学。所有BOM、温度和功率不作物理实测。

## 原始标准输出/错误（保留端口与真实命令）

### raw-experiment.txt
```text
执行日期 2026-11-11 01:24:10 Asia/Shanghai
$ python3 fetch.py
{
  "commit": "286d56ccbbb924c10812fc5e6cabb11906454afc",
  "files": 18,
  "bytes": 15705996
}
$ python3 assets.py
{
  "files": [
    {
      "file": "upstream/kestrel-k1/assets/body/head.glb",
      "bytes": 2888184,
      "nodes": 8,
      "meshes": 8,
      "skins": 0,
      "animations": 0,
      "generator": "Khronos glTF Blender I/O v5.2.40",
      "sha256": "b2abd480f7310646f28d20958c12f9bf99966cea102a95f97858a711e1efb317"
    },
    {
      "file": "upstream/kestrel-k1/assets/body/limbs.glb",
      "bytes": 3349064,
      "nodes": 40,
      "meshes": 40,
      "skins": 0,
      "animations": 0,
      "generator": "Khronos glTF Blender I/O v5.2.40",
      "sha256": "f1bd6997a65fd634c6ef4e3112535cf673639c75bc9debbe050fe2e299665265"
    },
    {
      "file": "upstream/kestrel-k1/assets/body/torso.glb",
      "bytes": 4248928,
      "nodes": 9,
      "meshes": 9,
      "skins": 0,
      "animations": 0,
      "generator": "Khronos glTF Blender I/O v5.2.40",
      "sha256": "d36f3fd1174eccdaa2e551f3f573a71415a3966173f55203834bd6643d340ea1"
    },
    {
      "file": "upstream/kestrel-k1/assets/shells.glb",
      "bytes": 2865440,
      "nodes": 90,
      "meshes": 90,
      "skins": 0,
      "animations": 0,
      "generator": "glTF-Transform v4.5.1",
      "sha256": "2f069fe278003bd44e7bf3022a4e929e17bc6e41fff2301545f5648d69ef48f4"
    }
  ],
  "total_nodes": 147,
  "total_meshes": 147
}
$ node clock.cjs
{
  "source": "exact extracted class T5; synthetic inputs, NOT measured FPS",
  "rows": [
    {
      "synthetic_interval_ms": 16.666666666666668,
      "reciprocal_hz": 59.99999999999999,
      "reported_hud_fps": 90,
      "simulation_dt": 0.01666666666666663
    },
    {
      "synthetic_interval_ms": 100,
      "reciprocal_hz": 10,
      "reported_hud_fps": 120,
      "simulation_dt": 0.05
    },
    {
      "synthetic_interval_ms": 1000,
      "reciprocal_hz": 1,
      "reported_hud_fps": 120,
      "simulation_dt": 0.05
    }
  ]
}
$ python3 browser.py studio
COMMAND ['/usr/bin/google-chrome', '--headless', '--no-sandbox', '--window-size=1280,900', '--virtual-time-budget=12000', '--screenshot=studio.png', '--dump-dom', 'http://127.0.0.1:56819/?quality=low&showcase=0&lab=studio']
Traceback (most recent call last):
  File "/workspace/xujia-batch/item07/exercise/browser.py", line 12, in <module>
    try:r=subprocess.run(cmd,capture_output=True,text=True,timeout=150)
          ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/subprocess.py", line 556, in run
    stdout, stderr = process.communicate(input, timeout=timeout)
                     ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/subprocess.py", line 1222, in communicate
    stdout, stderr = self._communicate(input, endtime, timeout)
                     ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/subprocess.py", line 2129, in _communicate
    self._check_timeout(endtime, orig_timeout, stdout, stderr)
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/subprocess.py", line 1269, in _check_timeout
    raise TimeoutExpired(
    ...<2 lines>...
            stderr=b''.join(stderr_seq) if stderr_seq else None)
subprocess.TimeoutExpired: Command '['/usr/bin/google-chrome', '--headless', '--no-sandbox', '--window-size=1280,900', '--virtual-time-budget=12000', '--screenshot=studio.png', '--dump-dom', 'http://127.0.0.1:56819/?quality=low&showcase=0&lab=studio']' timed out after 150 seconds

```

### browser-experiment.txt
```text
$ python3 browser.py studio (deterministic frame scheduler, 960x720)
COMMAND ['/usr/bin/google-chrome', '--headless', '--no-sandbox', '--window-size=960,720', '--virtual-time-budget=6500', '--screenshot=studio.png', '--dump-dom', 'http://127.0.0.1:39237/?quality=low&showcase=0&lab=studio']
chrome_exit 0
{
  "ok": false,
  "scenario": "studio",
  "glb_resources": 4,
  "joint_count": 32,
  "pose_options": [
    "stand_relaxed",
    "attention",
    "contrapposto",
    "crouch",
    "kneel",
    "reach_forward",
    "reach_up",
    "arms_crossed",
    "hands_on_hips",
    "thinking",
    "wave",
    "point",
    "inspect_hand",
    "calibration",
    "walk",
    "pinch",
    "fist",
    "open",
    "peace",
    "thumbs_up"
  ],
  "changed_joint_count": 29,
  "explode_moved_objects": 4186,
  "max_explode_local_delta": 619.5993434940839,
  "restore_local_delta": 0,
  "mode": "studio",
  "scene": "body",
  "registered_entries": 14088,
  "physical_items": 14088,
  "errors": [],
  "warnings": [
    "[KestrelBodyAssembly] Fallback to procedural shells for ./assets/body/head.glb: TypeError: Failed to fetch",
    "[KestrelBodyAssembly] Fallback to procedural shells for ./assets/body/torso.glb: TypeError: Failed to fetch",
    "[KestrelBodyAssembly] Fallback to procedural shells for ./assets/body/limbs.glb: TypeError: Failed to fetch",
    "[kestrel] Fallback to procedural shells: TypeError: Failed to fetch"
  ]
}
Traceback (most recent call last):
  File "/workspace/xujia-batch/item07/exercise/browser.py", line 14, in <module>
    out,err=proc.communicate(timeout=150)
    
AssertionError: {'ok': False, 'scenario': 'studio', 'glb_resources': 4, 'joint_count': 32, 'pose_options': ['stand_relaxed', 'attention', 'contrapposto', 'crouch', 'kneel', 'reach_forward', 'reach_up', 'arms_crossed', 'hands_on_hips', 'thinking', 'wave', 'point', 'inspect_hand', 'calibration', 'walk', 'pinch', 'fist', 'open', 'peace', 'thumbs_up'], 'changed_joint_count': 29, 'explode_moved_objects': 4186, 'max_explode_local_delta': 619.5993434940839, 'restore_local_delta': 0, 'mode': 'studio', 'scene': 'body', 'registered_entries': 14088, 'physical_items': 14088, 'errors': [], 'warnings': ['[KestrelBodyAssembly] Fallback to procedural shells for ./assets/body/head.glb: TypeError: Failed to fetch', '[KestrelBodyAssembly] Fallback to procedural shells for ./assets/body/torso.glb: TypeError: Failed to fetch', '[KestrelBodyAssembly] Fallback to procedural shells for ./assets/body/limbs.glb: TypeError: Failed to fetch', '[kestrel] Fallback to procedural shells: TypeError: Failed to fetch']}
$ python3 browser.py explode
COMMAND ['/usr/bin/google-chrome', '--headless', '--no-sandbox', '--window-size=960,720', '--virtual-time-budget=6500', '--screenshot=explode.png', '--dump-dom', 'http://127.0.0.1:47771/?quality=low&showcase=0&lab=explode']

```

### browser-experiment-v2.txt
```text
Earlier controlled redraw run was manually terminated after ~200s (subprocess timeout cleanup stalled); no result claimed.
$ python3 browser.py studio (autonomous RAF off; intermediate redraws suppressed; one restored final draw)
COMMAND ['/usr/bin/google-chrome', '--headless', '--no-sandbox', '--window-size=960,720', '--virtual-time-budget=6500', '--screenshot=studio.png', '--dump-dom', 'http://127.0.0.1:54079/?quality=low&showcase=0&lab=studio']
chrome_exit 0
{
  "ok": false,
  "scenario": "studio",
  "intermediate_redraws_suppressed": true,
  "final_renderer_restored": true,
  "glb_resources": 4,
  "joint_count": 32,
  "pose_options": [
    "stand_relaxed",
    "attention",
    "contrapposto",
    "crouch",
    "kneel",
    "reach_forward",
    "reach_up",
    "arms_crossed",
    "hands_on_hips",
    "thinking",
    "wave",
    "point",
    "inspect_hand",
    "calibration",
    "walk",
    "pinch",
    "fist",
    "open",
    "peace",
    "thumbs_up"
  ],
  "changed_joint_count": 29,
  "explode_moved_objects": 4186,
  "max_explode_local_delta": 619.5993434940839,
  "restore_local_delta": 0,
  "mode": "studio",
  "scene": "body",
  "registered_entries": 14088,
  "physical_items": 14088,
  "errors": [],
  "warnings": [
    "[KestrelBodyAssembly] Fallback to procedural shells for ./assets/body/head.glb: TypeError: Failed to fetch",
    "[KestrelBodyAssembly] Fallback to procedural shells for ./assets/body/torso.glb: TypeError: Failed to fetch",
    "[KestrelBodyAssembly] Fallback to procedural shells for ./assets/body/limbs.glb: TypeError: Failed to fetch",
    "[kestrel] Fallback to procedural shells: TypeError: Failed to fetch"
  ]
}
Traceback (most recent call last):
  File "/workspace/xujia-batch/item07/exercise/browser.py", line 19, in <module>
    Path(scenario+'-dom.html').write_text(r.stdout);Path(scenario+'-stderr.txt').write_text(r.stderr);Path(scenario+'-requests.txt').write_text('\n'.join(requests));print('chrome_exit',r.returncode);m=re.search(r'<pre id="lab-result"[^>]*>(.*?)</pre>',r.stdout,re.S);assert m,'missing harness result; inspect DOM/stderr';obj=json.loads(html.unescape(m.group(1)));print(json.dumps(obj,indent=2));Path(scenario+'-result.json').write_text(json.dumps(obj,indent=2));assert obj['ok'],obj
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     ~~~^^^^^^
AssertionError: {'ok': False, 'scenario': 'studio', 'intermediate_redraws_suppressed': True, 'final_renderer_restored': True, 'glb_resources': 4, 'joint_count': 32, 'pose_options': ['stand_relaxed', 'attention', 'contrapposto', 'crouch', 'kneel', 'reach_forward', 'reach_up', 'arms_crossed', 'hands_on_hips', 'thinking', 'wave', 'point', 'inspect_hand', 'calibration', 'walk', 'pinch', 'fist', 'open', 'peace', 'thumbs_up'], 'changed_joint_count': 29, 'explode_moved_objects': 4186, 'max_explode_local_delta': 619.5993434940839, 'restore_local_delta': 0, 'mode': 'studio', 'scene': 'body', 'registered_entries': 14088, 'physical_items': 14088, 'errors': [], 'warnings': ['[KestrelBodyAssembly] Fallback to procedural shells for ./assets/body/head.glb: TypeError: Failed to fetch', '[KestrelBodyAssembly] Fallback to procedural shells for ./assets/body/torso.glb: TypeError: Failed to fetch', '[KestrelBodyAssembly] Fallback to procedural shells for ./assets/body/limbs.glb: TypeError: Failed to fetch', '[kestrel] Fallback to procedural shells: TypeError: Failed to fetch']}
$ python3 browser.py explode
COMMAND ['/usr/bin/google-chrome', '--headless', '--no-sandbox', '--window-size=960,720', '--virtual-time-budget=6500', '--screenshot=explode.png', '--dump-dom', 'http://127.0.0.1:50031/?quality=low&showcase=0&lab=explode']
chrome_exit 0
{
  "ok": false,
  "scenario": "explode",
  "intermediate_redraws_suppressed": true,
  "final_renderer_restored": true,
  "glb_resources": 4,
  "joint_count": 32,
  "pose_options": [
    "stand_relaxed",
    "attention",
    "contrapposto",
    "crouch",
    "kneel",
    "reach_forward",
    "reach_up",
    "arms_crossed",
    "hands_on_hips",
    "thinking",
    "wave",
    "point",
    "inspect_hand",
    "calibration",
    "walk",
    "pinch",
    "fist",
    "open",
    "peace",
    "thumbs_up"
  ],
  "changed_joint_count": 29,
  "explode_moved_objects": 4186,
  "max_explode_local_delta": 619.5993434940839,
  "restore_local_delta": null,
  "mode": "exploded",
  "scene": "body",
  "registered_entries": 14088,
  "physical_items": 14088,
  "errors": [],
  "warnings": [
    "[KestrelBodyAssembly] Fallback to procedural shells for ./assets/body/head.glb: TypeError: Failed to fetch",
    "[KestrelBodyAssembly] Fallback to procedural shells for ./assets/body/torso.glb: TypeError: Failed to fetch",
    "[KestrelBodyAssembly] Fallback to procedural shells for ./assets/body/limbs.glb: TypeError: Failed to fetch",
    "[kestrel] Fallback to procedural shells: TypeError: Failed to fetch"
  ]
}
Traceback (most recent call last):
  File "/workspace/xujia-batch/item07/exercise/browser.py", line 19, in <module>
    Path(scenario+'-dom.html').write_text(r.stdout);Path(scenario+'-stderr.txt').write_text(r.stderr);Path(scenario+'-requests.txt').write_text('\n'.join(requests));print('chrome_exit',r.returncode);m=re.search(r'<pre id="lab-result"[^>]*>(.*?)</pre>',r.stdout,re.S);assert m,'missing harness result; inspect DOM/stderr';obj=json.loads(html.unescape(m.group(1)));print(json.dumps(obj,indent=2));Path(scenario+'-result.json').write_text(json.dumps(obj,indent=2));assert obj['ok'],obj
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     ~~~^^^^^^
AssertionError: {'ok': False, 'scenario': 'explode', 'intermediate_redraws_suppressed': True, 'final_renderer_restored': True, 'glb_resources': 4, 'joint_count': 32, 'pose_options': ['stand_relaxed', 'attention', 'contrapposto', 'crouch', 'kneel', 'reach_forward', 'reach_up', 'arms_crossed', 'hands_on_hips', 'thinking', 'wave', 'point', 'inspect_hand', 'calibration', 'walk', 'pinch', 'fist', 'open', 'peace', 'thumbs_up'], 'changed_joint_count': 29, 'explode_moved_objects': 4186, 'max_explode_local_delta': 619.5993434940839, 'restore_local_delta': None, 'mode': 'exploded', 'scene': 'body', 'registered_entries': 14088, 'physical_items': 14088, 'errors': [], 'warnings': ['[KestrelBodyAssembly] Fallback to procedural shells for ./assets/body/head.glb: TypeError: Failed to fetch', '[KestrelBodyAssembly] Fallback to procedural shells for ./assets/body/torso.glb: TypeError: Failed to fetch', '[KestrelBodyAssembly] Fallback to procedural shells for ./assets/body/limbs.glb: TypeError: Failed to fetch', '[kestrel] Fallback to procedural shells: TypeError: Failed to fetch']}

```

### browser-experiment-v3.txt
```text
Official Python http.server documentation: ThreadingHTTPServer handles browsers pre-opening sockets; corrected single-threaded test server, kept old failure evidence.
2026-11-11 01:36:33 Asia/Shanghai
$ python3 browser.py studio
COMMAND ['/usr/bin/google-chrome', '--headless', '--no-sandbox', '--window-size=960,720', '--virtual-time-budget=30000', '--screenshot=studio.png', '--dump-dom', 'http://127.0.0.1:34569/?quality=low&showcase=0&lab=studio']
chrome_exit 0
{
  "ok": false,
  "reason": "not ready",
  "has_api": true,
  "glb_resources": 0,
  "errors": []
}
Traceback (most recent call last):
  File "/workspace/xujia-batch/item07/exercise/browser.py", line 21, in <module>
    Path(scenario+'-dom.html').write_text(r.stdout);Path(scenario+'-stderr.txt').write_text(r.stderr);Path(scenario+'-requests.txt').write_text('\n'.join(requests));print('chrome_exit',r.returncode);m=re.search(r'<pre id="lab-result"[^>]*>(.*?)</pre>',r.stdout,re.S);assert m,'missing harness result; inspect DOM/stderr';obj=json.loads(html.unescape(m.group(1)));print(json.dumps(obj,indent=2));Path(scenario+'-result.json').write_text(json.dumps(obj,indent=2));assert obj['ok'],obj
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     ~~~^^^^^^
AssertionError: {'ok': False, 'reason': 'not ready', 'has_api': True, 'glb_resources': 0, 'errors': []}
$ python3 browser.py explode
COMMAND ['/usr/bin/google-chrome', '--headless', '--no-sandbox', '--window-size=960,720', '--virtual-time-budget=30000', '--screenshot=explode.png', '--dump-dom', 'http://127.0.0.1:33399/?quality=low&showcase=0&lab=explode']
chrome_exit 0
{
  "ok": false,
  "reason": "not ready",
  "has_api": true,
  "glb_resources": 0,
  "errors": []
}
Traceback (most recent call last):
  File "/workspace/xujia-batch/item07/exercise/browser.py", line 21, in <module>
    Path(scenario+'-dom.html').write_text(r.stdout);Path(scenario+'-stderr.txt').write_text(r.stderr);Path(scenario+'-requests.txt').write_text('\n'.join(requests));print('chrome_exit',r.returncode);m=re.search(r'<pre id="lab-result"[^>]*>(.*?)</pre>',r.stdout,re.S);assert m,'missing harness result; inspect DOM/stderr';obj=json.loads(html.unescape(m.group(1)));print(json.dumps(obj,indent=2));Path(scenario+'-result.json').write_text(json.dumps(obj,indent=2));assert obj['ok'],obj
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     ~~~^^^^^^
AssertionError: {'ok': False, 'reason': 'not ready', 'has_api': True, 'glb_resources': 0, 'errors': []}

```

## 收尾
2026-11-11 01:45:17 Asia/Shanghai：按用户新指令结束。停止指令前已经完成练习ZIP新解压的fetch/assets/clock三步重放，日志qa/fresh-replay-log.txt；不增加实验或重试。完整GLB与修正后的步态仍未验证，不设置自动恢复。
