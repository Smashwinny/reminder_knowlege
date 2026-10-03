// 实验2：书 §12 最小壳的本地化改写。共用壳 + env 开关参数。
// ?env=0 -> 无环境贴图（复现"白底 PBR 金属死黑"）
// ?env=1 -> canvas 渐变环境贴图（书里的 studioEnv 修法）
// ?model=sphere_smooth.glb|tower_lattice.glb
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const q = new URLSearchParams(location.search);
const ENV_ON = q.get('env') !== '0';
const MODEL = q.get('model') || 'sphere_smooth.glb';

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(1);
renderer.setSize(640, 480);
document.body.appendChild(renderer.domElement);
const status = document.getElementById('status');
status.textContent = 'env=' + (ENV_ON ? 'ON' : 'OFF') + ' model=' + MODEL;

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xffffff); // 白底：死黑坑的触发条件
if (ENV_ON) scene.environment = studioEnv(renderer);

const camera = new THREE.PerspectiveCamera(45, 640 / 480, 0.01, 100);
camera.position.set(3.2, 2.2, 3.6);
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 0.8, 0);

const sun = new THREE.DirectionalLight(0xffffff, 2.5);
sun.position.set(3, 5, 2);
scene.add(sun, new THREE.AmbientLight(0xffffff, 0.5));

new GLTFLoader().load('./' + MODEL, g => {
  const root = g.scene;
  const b = new THREE.Box3().setFromObject(root);
  const c = b.getCenter(new THREE.Vector3());
  const s = 1.6 / Math.max(...b.getSize(new THREE.Vector3()).toArray());
  root.scale.setScalar(s);
  root.position.set(-c.x * s, -b.min.y * s, -c.z * s); // 底面压到地面
  scene.add(root);
  status.textContent += ' loaded';
});

// 书里原样的 studioEnv：canvas 画渐变当 equirect，PMREM 转环境光照
function studioEnv(rd) {
  const c = document.createElement('canvas'); c.width = 128; c.height = 128;
  const g = c.getContext('2d'), grd = g.createLinearGradient(0, 0, 0, 128);
  grd.addColorStop(0, '#ffffff');
  grd.addColorStop(.34, '#e8e4da');
  grd.addColorStop(.52, '#928d82');
  grd.addColorStop(.75, '#5c574e');
  grd.addColorStop(1, '#403c35'); // 必须有暗部：金属才有明暗对比
  g.fillStyle = grd; g.fillRect(0, 0, 128, 128);
  g.fillStyle = 'rgba(255,255,255,.9)';
  g.beginPath(); g.ellipse(40, 24, 26, 13, 0, 0, Math.PI * 2); g.fill();
  const t = new THREE.CanvasTexture(c);
  t.mapping = THREE.EquirectangularReflectionMapping;
  const pm = new THREE.PMREMGenerator(rd);
  const env = pm.fromEquirectangular(t).texture;
  pm.dispose(); t.dispose(); return env;
}

renderer.setAnimationLoop(() => { controls.update(); renderer.render(scene, camera); });
