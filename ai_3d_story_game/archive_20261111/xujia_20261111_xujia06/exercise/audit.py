from pathlib import Path
import hashlib,json
r={'story_sha256':hashlib.sha256(Path('story.cjs').read_bytes()).hexdigest(),'scene_sha256':hashlib.sha256(Path('scene.html').read_bytes()).hexdigest(),'three_version':json.loads(Path('node_modules/three/package.json').read_text())['version'],'is_original_game_source':False,'author_html_downloaded':False};print(json.dumps(r,indent=2));assert r['three_version']=='0.170.0';Path('audit-result.json').write_text(json.dumps(r,indent=2))
