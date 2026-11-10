import * as T from 'three';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {AnimationStateMachine} from './upstream/AnimationStateMachine.js';
import {BarrelRotationController} from './upstream/TurretController.js';
import {LegIKSolver} from './upstream/LegIKSolver.js';
import {QuadrupedGaitController} from './upstream/QuadrupedGaitController.js';
const mode=process.argv[2]; let result;
function rig(){let rootNode=new T.Group(), chassisNode=new T.Group();rootNode.add(chassisNode);let legs={}; for(const [id,x,z] of [['FL',-.3,.3],['FR',.3,.3],['RL',-.3,-.3],['RR',.3,-.3]]){let h=new T.Group(),f=new T.Group(),t=new T.Group(),a=new T.Group(),tip=new T.Group();h.position.set(x,0,z);f.position.x=.115;t.position.x=.5;a.position.x=.48;tip.position.x=.31;chassisNode.add(h);h.add(f);f.add(t);t.add(a);a.add(tip);legs[id]={id,hipYawNode:h,femurPitchNode:f,tibiaPitchNode:t,anklePitchNode:a,footTipNode:tip,hipLocalPos:h.position.clone(),baseYaw:Math.atan2(-z,x)};}return {rootNode,chassisNode,legs};}
if(mode==='states'){
 let m=new AnimationStateMachine();let cases=[ [{},'IDLE','STANDBY'],[{fwdInput:1,isFastInput:true},'FAST_WALK','STANDBY'],[{fwdInput:-1},'WALK_BACKWARD','STANDBY'],[{strafeInput:1},'STRAFE_RIGHT','STANDBY'],[{turnInput:1},'TURN_LEFT','STANDBY'],[{isFiringInput:true,spinSpeed:9},'IDLE','FIRING_ACTIVE'] ];for(let [inp,l,w] of cases){let s=m.evaluate(inp);assert.equal(s.locomotionState,l);assert.equal(s.weaponState,w);}
 let frames=[];for(let hz of [20,30,60,120]){let b=new BarrelRotationController(),count=0,first=null;for(let i=0;i<hz*2;i++){if(b.update(1/hz,null,true)){count++;first??=(i+1)/hz;}}let heat=b.heatLevel;for(let i=0;i<hz*4;i++)b.update(1/hz,null,false);assert.equal(b.spinSpeed,0);assert.equal(b.heatLevel,0);frames.push({hz,trigger_count_2s:count,first_trigger_s:first,heat_after_2s:heat});}
 let b=new BarrelRotationController();b.spinSpeed=9;let actual=b.update(1/120,null,true);assert.equal(actual,false);
 result={state_cases:cases.length,state_at_speed9:'FIRING_ACTIVE',actual_trigger_at_speed9:actual,frames,note:'UI threshold 8 differs from actual trigger threshold 10; Hz are synthetic timesteps, not measured FPS'};
}else if(mode==='ik'){
 let s=new LegIKSolver(),r=rig(),leg=r.legs.FR;let maxErr=0;for(let i=0;i<101;i++){let radial=.55+i*.002;let target=new T.Vector3(.3+radial*Math.cos(leg.baseYaw),-.56,.3-radial*Math.sin(leg.baseYaw));s.solveLegWorld(leg,r.chassisNode,target);r.rootNode.updateMatrixWorld(true);maxErr=Math.max(maxErr,leg.footTipNode.getWorldPosition(new T.Vector3()).distanceTo(target));}assert.ok(maxErr<1e-10);
 let far=new T.Vector3(10,-.56,.3);let sol=s.solveLegWorld(leg,r.chassisNode,far);r.rootNode.updateMatrixWorld(true);let farErr=leg.footTipNode.getWorldPosition(new T.Vector3()).distanceTo(far);assert.ok(Object.values(sol).every(Number.isFinite));assert.ok(farErr>1);
 result={reachable_samples:101,max_fk_error:maxErr,unreachable_target_error:farErr,angles_finite:true,note:'synthetic hierarchy follows solver comments; not a loaded-GLB animation test'};
}else if(mode==='gait'){
 let s=new LegIKSolver(),r=rig(),g=new QuadrupedGaitController(s),position=new T.Vector3();let stance=0,swings=0,maxDrift=0;for(let i=0;i<600;i++){position.z+=.5/60;g.update(1/60,r,{position,yaw:0,linearVel:new T.Vector3(0,0,.5),angularVel:0,isMoving:true,isFastWalk:false});for(let st of Object.values(g.legStates)){if(st.isSwinging)swings++;else{stance++;maxDrift=Math.max(maxDrift,st.currentWorldPos.distanceTo(st.plantedWorldPos));}}}assert.equal(maxDrift,0);assert.ok(swings>0&&stance>0);result={steps:600,simulated_seconds:10,stance_samples:stance,swing_samples:swings,max_target_plant_drift:maxDrift,note:'target planting only, not actual solved mesh feet or physical balance'};
}else throw Error('states|ik|gait required');
fs.writeFileSync(new URL(`./${mode}-result.json`,import.meta.url),JSON.stringify(result,null,2));console.log(JSON.stringify(result));
