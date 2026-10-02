// 实验3：真实调用 @bryllim/workout-guide 的四个 API（Node ESM，零额外依赖）
// 运行：node 02_api_demo.mjs
import { exercises, getExercise, searchExercises, getAssetUrl, normalizeSearchText } from '@bryllim/workout-guide';

console.log('[1] exercises 总数 =', exercises.length);

console.log('\n[2] getExercise 按 slug 精确取:');
const pushUp = getExercise('push-up');
console.log('   ', pushUp.name, '|', pushUp.equipment, '|', pushUp.primaryMuscle,
  '| 帧数', pushUp.frames.length);

console.log('\n[3] getExercise 按 id 取（同一动作）:');
console.log('   ', getExercise('exercise-push-up')?.slug);

console.log('\n[4] searchExercises 组合查询: "press" + 器械=Dumbbell');
const hits = searchExercises('press', { equipment: 'Dumbbell' });
console.log('    命中', hits.length, '个:', hits.slice(0, 5).map(e => e.name).join(' / '), '...');

console.log('\n[5] searchExercises 过滤: 主肌群=Chest 且 徒手(bodyweight)');
const chest = searchExercises('', { primaryMuscle: 'chest', equipment: 'bodyweight' });
console.log('    命中', chest.length, '个:', chest.slice(0, 4).map(e => e.slug).join(', '));

console.log('\n[6] getAssetUrl 生成 CDN 地址（默认 jsDelivr）:');
console.log('   ', getAssetUrl('push-up', 1));
console.log('   ', getAssetUrl('push-up', 3, { baseUrl: 'https://myapp.com/assets/' }));

console.log('\n[7] normalizeSearchText 归一化演示（重音/大小写/符号）:');
console.log('    "Café & Lunge!" ->', JSON.stringify(normalizeSearchText('Café & Lunge!')));

console.log('\n[8] 查不到时返回 null（不抛异常）:');
console.log('   ', getExercise('not-a-real-exercise'));
