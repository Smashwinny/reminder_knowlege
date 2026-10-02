/**
 * 实验入口：在 Node 里直接驱动火星编辑器的渲染管线（repo/src/markdown.ts 的 renderArticle）。
 * 用法：node render.mjs <markdown文件> <主题名>
 * 主题名取 repo/src/theme.ts 里的导出名（classic/editorial/cream/dark/indigo/ink/sakura/minimal/typewriter）
 */
import { readFileSync } from 'node:fs';
import * as theme from '../repo/src/theme';

// markdown.ts 默认走 getTheme()（localStorage），Node 环境没有，
// 所以显式传入主题对象，绕开浏览器依赖。
const { renderArticle } = await import('../repo/src/markdown');

const file = process.argv[2] ?? 'sample.md';
const themeName = process.argv[3] ?? 'classicTheme';

const md = readFileSync(file, 'utf-8');
const th = (theme as Record<string, unknown>)[themeName];
if (!th) {
  console.error(`未知主题: ${themeName}`);
  process.exit(1);
}

const result = renderArticle(md, th as never);

// ---- 自动验证：公众号兼容性检查 ----
const checks: Array<[string, boolean, string]> = [
  ['正文不含 class 属性（微信会丢弃）', !/ class=/.test(result.body), 'class= 应为 0 处'],
  ['正文不含 <style> 标签（微信会丢弃）', !/<style/i.test(result.body), '<style> 应为 0 处'],
  ['正文不含 <script> 标签', !/<script/i.test(result.body), '<script> 应为 0 处'],
  ['块级标签全部带内联 style', (() => {
    const tags = [...result.body.matchAll(/<(p|h[1-6]|li|blockquote|pre|section|td|th)[ >]/g)].length;
    const styled = [...result.body.matchAll(/<(p|h[1-6]|li|blockquote|pre|section|td|th)[^>]*?style="/g)].length;
    return tags > 0 && styled === tags;
  })(), '带 style 的块级标签数应等于块级标签总数'],
];

console.log('=== 验证结果 ===');
let allPass = true;
for (const [name, ok, note] of checks) {
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}  (${note})`);
  if (!ok) allPass = false;
}

const styleCount = (result.body.match(/style="/g) ?? []).length;
console.log(`\n内联 style 总数: ${styleCount}`);
console.log(`hasImage: ${result.hasImage}`);

console.log('\n=== 输出 HTML 前 1200 字符 ===');
console.log(result.html.slice(0, 1200));

import { writeFileSync } from 'node:fs';
writeFileSync(file.replace(/\.md$/, '') + `.${themeName}.html`, result.html, 'utf-8');
console.log(`\n完整 HTML 已写出: ${file.replace(/\.md$/, '')}.${themeName}.html`);

process.exit(allPass ? 0 : 2);
