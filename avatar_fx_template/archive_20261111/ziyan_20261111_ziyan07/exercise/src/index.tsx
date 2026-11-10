import React from 'react';
import {AbsoluteFill,Composition,Sequence,interpolate,spring,useCurrentFrame,useVideoConfig,registerRoot} from 'remotion';
import cfg from './template.json';
const Avatar:React.FC=()=>{const f=useCurrentFrame();return <div style={{position:'absolute',left:cfg.avatar.rect[0],top:cfg.avatar.rect[1],width:cfg.avatar.rect[2],height:cfg.avatar.rect[3],background:'#102b43',border:'3px solid #00d9ee',borderRadius:30,boxSizing:'border-box',textAlign:'center'}}>
 <div style={{fontSize:30,color:'#00d9ee',paddingTop:30}}>AVATAR SLOT</div>
 <svg width="360" height="390" viewBox="0 0 360 390" style={{transform:`translateY(${Math.sin(f/15)*8}px)`}}>
  <circle cx="180" cy="108" r="65" fill="#43b9d0"/><path d="M65 325 Q60 190 180 195 Q300 190 295 325 Z" fill="#2471bc"/>
  <circle cx="158" cy="104" r="7" fill="#10243a"/><circle cx="202" cy="104" r="7" fill="#10243a"/><path d="M160 136 Q180 147 200 136" stroke="#10243a" strokeWidth="6" fill="none"/>
  <circle cx="180" cy="225" r="150" stroke="#ff922b" strokeWidth="3" strokeDasharray="12 18" fill="none" opacity=".7" transform={`rotate(${f*1.5} 180 225)`}/>
 </svg><div style={{fontSize:32,fontWeight:800,color:'#ffb55a'}}>{cfg.avatar.label}</div><div style={{fontSize:25,color:'#b8ccdf',marginTop:20}}>无克隆音色 · 无口型模型</div>
 </div>};
const Scene:React.FC<{s:typeof cfg.sections[number]}>=({s})=>{const f=useCurrentFrame();const {fps}=useVideoConfig();const enter=spring({frame:f,fps,config:{damping:18}});return <div style={{position:'absolute',left:cfg.contentRect[0],top:cfg.contentRect[1],width:cfg.contentRect[2],height:cfg.contentRect[3]}}>
 <h1 style={{fontSize:66,margin:'15px 0 65px',opacity:enter,transform:`translateY(${(1-enter)*40}px)`}}>{s.title}</h1>
 {s.labels.map((l,i)=><div key={l} style={{height:75,marginBottom:20,borderRadius:15,background:'#173752',borderLeft:`12px solid ${s.color}`,fontSize:40,padding:'12px 30px',boxSizing:'border-box',opacity:spring({frame:f-8-i*6,fps,config:{damping:20}})}}>{l}<span style={{float:'right',color:s.color}}>0{i+1}</span></div>)}
 <div style={{height:8,background:s.color,width:`${interpolate(f,[0,59],[0,100])}%`,marginTop:30}}/>
 </div>};
const Video:React.FC=()=> <AbsoluteFill style={{background:'linear-gradient(125deg,#07172d,#103b62)',color:'white',fontFamily:'"Noto Sans CJK SC",sans-serif',overflow:'hidden'}}>
 <div style={{position:'absolute',top:75,left:100,fontSize:37,color:'#00d9ee'}}>三层模板验证 · 人物层 × 内容层 × 动效层</div>
 <Avatar/>{cfg.sections.map((s,i)=><Sequence key={i} from={s.from} durationInFrames={s.duration}><Scene s={s}/></Sequence>)}
 <div style={{position:'absolute',left:100,right:100,bottom:105,padding:'22px 30px',background:'#f8fbff',color:'#10243a',fontSize:32,borderRadius:16}}>仅占位层与动效实跑；数字人 / 音色克隆 / Opus 均待验证</div>
 <div style={{position:'absolute',bottom:35,left:100,fontSize:24,color:'#b8ccdf'}}>非作者原模板 · 未验证“4条视频约100客资” · 未发布</div>
 </AbsoluteFill>;
registerRoot(()=> <Composition id="TemplateLab" component={Video} durationInFrames={cfg.durationFrames} fps={cfg.fps} width={cfg.width} height={cfg.height}/>);
