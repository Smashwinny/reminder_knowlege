import {readFileSync,readdirSync,statSync,writeFileSync,mkdirSync} from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
const repo=path.resolve(process.argv[2]||'D:/做大做强/my_website');
const pkg=JSON.parse(readFileSync(path.join(repo,'package.json'),'utf8'));
const sources=['app/world-view.tsx','app/scene/characters.ts','app/scene/avatar-download.mjs','app/world.tsx'].map(name=>({name,source:readFileSync(path.join(repo,name),'utf8')}));
const models=readdirSync(path.join(repo,'public/models')).filter(n=>/-web\.vrm$|-lite\.vrm$/.test(n)).map(name=>{
 const bytes=readFileSync(path.join(repo,'public/models',name));
 const json=JSON.parse(bytes.subarray(20,20+bytes.readUInt32LE(12)).toString('utf8').trim());
 const compressed=readFileSync(path.join(repo,'public/models',name+'.bin'));
 const decoded=zlib.gunzipSync(compressed);if(!bytes.equals(decoded))throw Error('gzip mismatch '+name);
 return {name,rawBytes:bytes.length,gzipBytes:compressed.length,embeddedImages:json.images?.length||0,meshes:json.meshes?.length||0,
  imageBufferBytes:(json.images||[]).reduce((n,i)=>n+(json.bufferViews?.[i.bufferView]?.byteLength||0),0),
  idealTransferMsAt4Mbps:Math.round(compressed.length*8/4e6*1000)};
});
const evidence={date:'2026-10-03',threeVersion:pkg.dependencies.three,vrmVersion:pkg.dependencies['@pixiv/three-vrm'],models,
 lazyWorlds:sources[0].source.includes('lazy(()=>import('),compressedDownload:sources[2].source.includes("DecompressionStream('gzip')"),
 avatarParser:'GLTFLoader + VRMLoaderPlugin + parseAsync',
 compileAsyncInSceneModules:readdirSync(path.join(repo,'app')).filter(n=>/-world\.tsx$|^world\.tsx$/.test(n)).filter(n=>readFileSync(path.join(repo,'app',n),'utf8').includes('compileAsync')),
 warning:'Asset inventory and idealized transfer math only. NOT current browser performance or a measured speedup; 4Mbps is a hypothetical link, excluding latency/competition/decode/render.'};
const out=new URL('./output/',import.meta.url);mkdirSync(out,{recursive:true});writeFileSync(new URL('website-audit.json',out),JSON.stringify(evidence,null,2)+'\n');console.log(JSON.stringify(evidence,null,2));
