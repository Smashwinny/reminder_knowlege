// 实验二：模拟 ai-website-cloner-template 五阶段流水线的"Phase 1 侦察"
// 用法: node recon.mjs <url>
// 输出: 侦察 JSON（图片/视频/背景图/SVG/字体/favicon 清点）——这是 SKILL.md 中
// "Asset Discovery Script Pattern" 的无浏览器简化版：用 fetch+正则代替浏览器 MCP。
import { writeFileSync } from 'node:fs';

const url = process.argv[2];
if (!url) { console.error('用法: node recon.mjs <url>'); process.exit(1); }

const res = await fetch(url, { headers: { 'User-Agent': 'Mozilla/5.0 (recon-demo)' } });
const html = await res.text();

const count = (re) => (html.match(re) || []).length;
const uniq = (reSource, flags, g = 1) => {
  const reG = new RegExp(reSource, flags);           // 全局版找所有匹配
  const re1 = new RegExp(reSource, flags.replace('g', '')); // 非全局版取捕获组
  return [...new Set((html.match(reG) || []).map(m => m.match(re1)?.[g] ?? m))];
};

const report = {
  target: url,
  httpStatus: res.status,
  htmlBytes: html.length,
  images: {
    totalImgTags: count(/<img\b/gi),
    srcSet: count(/srcset=/gi),
    sampleSrcs: uniq('<img[^>]+src=["\']([^"\']+)["\']', 'gi').slice(0, 5),
  },
  videos: count(/<video\b/gi),
  backgroundImages: uniq('background(?:-image)?\\s*:\\s*[^;]*url\\(([\'"]?)([^)\'"]+)\\1\\)', 'gi', 2).slice(0, 5),
  svgInline: count(/<svg\b/gi),
  fonts: {
    googleFontsLinks: uniq('fonts\\.googleapis\\.com\\/css2?\\?family=([^"\'&]+)', 'gi'),
    fontFaceDecls: count(/@font-face/gi),
  },
  favicons: uniq('<link[^>]+rel=["\'][^"\']*icon[^"\']*["\'][^>]*href=["\']([^"\']+)["\']', 'gi').slice(0, 5),
  techHints: {
    isNextJs: /__NEXT_DATA__|\/_next\//.test(html),
    isNuxt: /__NUXT__/.test(html),
    tailwindClasses: count(/class="[^"]*\b(?:flex|grid|hidden)\b[^"]*"/gi),
  },
};

writeFileSync('recon-report.json', JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
console.log('\n[OK] 报告已写入 recon-report.json —— 对应真实流程中的 docs/research/<site-key>/ 侦察产物');
