import fs from 'node:fs';
import assert from 'node:assert/strict';
import {validateRig,validateAvatarFiles,parseManifest,packAvatar,unpackAvatar} from './runtime/node_modules/mesh-avatar/dist/index.js';
const s=process.argv[2];
const files={};
function walk(d,base=''){for(const entry of fs.readdirSync(d,{withFileTypes:true})){const key=base+entry.name;if(entry.isDirectory())walk(d+'/'+entry.name,key+'/');else files[key]=new Uint8Array(fs.readFileSync(d+'/'+entry.name));}}
walk(new URL('./avatar',import.meta.url).pathname);
if(s==='version')console.log(JSON.parse(fs.readFileSync(new URL('./runtime/node_modules/mesh-avatar/package.json',import.meta.url))).version);
if(s==='validate'){const rig=JSON.parse(new TextDecoder().decode(files['rig.json']));const errors=validateRig(rig);console.log('rig_errors=',errors);assert.equal(errors.length,0);const errs=validateAvatarFiles(files);console.log('file_errors=',errs);assert.equal(errs.length,0);}
if(s==='pack'){const packed=packAvatar(files);fs.writeFileSync(new URL('./demo.mavatar',import.meta.url),packed);const back=unpackAvatar(packed);assert.deepEqual(Object.keys(back).sort(),Object.keys(files).sort());for(const k of Object.keys(files))assert.deepEqual(back[k],files[k]);console.log('roundtrip files=',Object.keys(files).length,'archive bytes=',packed.length);}
if(s==='negative'){let rejected=0;for(const manifest of [{format:'bad',version:1,name:'x'},{format:'mesh-avatar',version:999,name:'x'},{format:'mesh-avatar',version:1,name:''}]){try{parseManifest(manifest);}catch(e){rejected++;console.log(e.message);}}assert.equal(rejected,3);console.log('invalid_manifests_rejected=',rejected);}
