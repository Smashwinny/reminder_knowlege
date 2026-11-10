import React from 'react';
import {AbsoluteFill,Composition,Sequence,interpolate,spring,useCurrentFrame,useVideoConfig,registerRoot} from 'remotion';
const scenes=[
 {title:'别等准备好，先做一次',caption:'原创学习文案 · 小步行动比空想更具体',tag:'01 / 规格',color:'#00d9ee',words:['16:9','1080p','30fps']},
 {title:'把目标拆成一小步',caption:'不复制热门作品，用自己的话重新组织',tag:'02 / 时间轴',color:'#ff922b',words:['主张','证据','结论']},
 {title:'让证据跟着行动走',caption:'留下输入、输出与失败记录',tag:'03 / 动效',color:'#458bff',words:['位移','缓动','错峰']},
 {title:'今天开始，明天再改进',caption:'一个小实验，就是可验证的进步',tag:'04 / 证据',color:'#00d9ee',words:['ffprobe','抽帧','复查']},
];
const Scene:React.FC<{data:typeof scenes[number]}>=({data})=>{
 const frame=useCurrentFrame();const {fps}=useVideoConfig();
 const enter=spring({frame,fps,config:{damping:18,stiffness:110}});
 return <AbsoluteFill style={{padding:'100px 120px',color:'#fff',fontFamily:'"Noto Sans CJK SC",sans-serif'}}>
  <div style={{fontSize:32,color:data.color,letterSpacing:6}}>{data.tag} · Vibe文案重制 · 无配音</div>
  <h1 style={{fontSize:76,margin:'60px 0 65px',transform:`translateY(${(1-enter)*55}px)`,opacity:enter}}>{data.title}</h1>
  <div style={{display:'flex',gap:36}}>{data.words.map((word,i)=>{
   const s=spring({frame:frame-i*7-8,fps,config:{damping:16}});
   return <div key={word} style={{width:500,padding:'55px 20px',textAlign:'center',border:`3px solid ${data.color}`,background:'#122840',borderRadius:26,fontSize:52,transform:`scale(${s})`,opacity:s}}>{word}</div>
  })}</div>
  <div style={{marginTop:88,padding:'25px 35px',background:'#f8fbff',borderRadius:18,color:'#10243a',fontSize:44,borderLeft:`14px solid ${data.color}`}}>{data.caption}</div>
 </AbsoluteFill>
};
const Video:React.FC=()=>{const f=useCurrentFrame();return <AbsoluteFill style={{background:'linear-gradient(125deg,#07172d,#103b62)',overflow:'hidden'}}>
 <div style={{position:'absolute',width:850,height:850,border:'2px solid #1e6280',borderRadius:'50%',right:-250,top:-450,transform:`rotate(${f}deg)`,borderStyle:'dashed'}}/>
 <div style={{position:'absolute',right:55,top:45,width:45,height:45,borderRadius:'50%',background:'#ff922b',transform:`scale(${1+(1-(f%15)/15)*0.5})`}}/>{scenes.map((data,i)=><Sequence key={i} from={i*60} durationInFrames={60}><Scene data={data}/></Sequence>)}
 <div style={{position:'absolute',bottom:58,left:120,right:120,height:8,background:'#203e58'}}><div style={{height:8,width:`${interpolate(f,[0,239],[0,100])}%`,background:'#ff922b'}}/></div>
 <div style={{position:'absolute',bottom:15,right:120,color:'#9ec3df',fontSize:22}}>Remotion · 人工编写组件 · 8秒 · 合成BGM另行混流</div>
 </AbsoluteFill>};
registerRoot(()=> <Composition id="VibeLab" component={Video} durationInFrames={240} fps={30} width={1920} height={1080}/>);
