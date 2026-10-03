import {readFileSync} from 'node:fs';
import {stripTypeScriptTypes} from 'node:module';
import path from 'node:path';
const repo=path.resolve(process.argv[2]||'F:/reminder/aihot/repo');
let source=readFileSync(path.join(repo,'tests/architecture.test.ts'),'utf8');
// Study fixture only: normalize Windows separators where upstream compares POSIX strings.
// ROOT points to the unchanged upstream checkout; no upstream files are edited.
source=source.replace('path.resolve(import.meta.dirname, "..")',JSON.stringify(repo))
 .replace('path.relative(ROOT, full)','path.relative(ROOT, full).replaceAll("\\\\", "/")')
 .replace('path.relative(BACKEND, path.resolve(ROOT, path.dirname(file), spec))','path.relative(BACKEND, path.resolve(ROOT, path.dirname(file), spec)).replaceAll("\\\\", "/")')
 .replace('path.relative("packages/backend/src", file)','path.relative("packages/backend/src", file).replaceAll("\\\\", "/")');
await import('data:text/javascript;base64,'+Buffer.from(stripTypeScriptTypes(source,{mode:'strip'})).toString('base64'));
