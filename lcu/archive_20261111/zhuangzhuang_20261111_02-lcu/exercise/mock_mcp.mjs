// 自编教学模拟：只有内存文档，无桌面/网络/用户账户接口。
// node:vm 不是安全沙箱。只接受本练习受信任的固定代码；不要接入模型或不可信输入。
import readline from 'node:readline';
import vm from 'node:vm';
const VERSION='2025-11-25';
const model={text:'',saved:false,revision:0,cursor:{x:0,y:0}};
let context, initialized=false, ready=false;
const copy=x=>JSON.parse(JSON.stringify(x));
function reset(){
 const app={
  getState:()=>({kind:'SIMULATED_APP',appId:'demo.notes',...copy(model),elements:[{id:'editor',role:'textbox'},{id:'save',role:'button',name:'保存'}]}),
  typeText(text){if(typeof text!=='string'||text.length>1000)throw new Error('模拟文本参数错误');model.text+=text;model.saved=false;model.revision++;return copy(model);},
  click({elementId}){if(elementId!=='save')throw new Error('模拟元素不存在');model.saved=true;return {simulated:true,saved:true};},
  pressKey(key){if(key!=='CTRL+S')throw new Error('模拟器只实现CTRL+S');model.saved=true;return {simulated:true,saved:true};},
  getScreenshot:()=>({kind:'SYNTHETIC_DESCRIPTOR',actualCapture:false,width:800,height:600,note:'仅模拟元数据，无真实截图像素'})
 };
 const cua=Object.freeze({
  getState:()=>({kind:'SIMULATED_DESKTOP',applications:[{id:'demo.notes',name:'模拟记事本'}],actualDesktopAccess:false}),
  getApp(id){if(id!=='demo.notes')throw new Error('模拟白名单拒绝：'+id);return app;},
  move({x,y}){if(!Number.isFinite(x)||!Number.isFinite(y)||x<0||x>=800||y<0||y>=600)throw new Error('模拟坐标越界');model.cursor={x,y};return copy(model.cursor);}
 });
 context=vm.createContext({cua,console:{log:(...x)=>process.stderr.write('模拟日志：'+x.map(String).join(' ')+'\n')}},{codeGeneration:{strings:false,wasm:false}});
}
reset();
const tools=[
 {name:'js',description:'教学模拟：执行受信任的同步JavaScript；保留变量。不是LCU原始运行时。',inputSchema:{type:'object',properties:{code:{type:'string'}},required:['code'],additionalProperties:false}},
 {name:'js_reset',description:'只清空模拟JS上下文；不撤销模拟文档副作用。',inputSchema:{type:'object',properties:{},additionalProperties:false}}
];
const send=x=>process.stdout.write(JSON.stringify(x)+'\n');
const error=(id,code,message)=>send({jsonrpc:'2.0',id,error:{code,message}});
const result=(id,value)=>send({jsonrpc:'2.0',id,result:value});
const toolResult=(value,isError=false)=>({content:[{type:'text',text:JSON.stringify(value??null)}],isError});
const rl=readline.createInterface({input:process.stdin,crlfDelay:Infinity});
for await(const line of rl){
 let msg;try{msg=JSON.parse(line);}catch{error(null,-32700,'Parse error');continue;}
 if(!msg||Array.isArray(msg)||msg.jsonrpc!=='2.0'||typeof msg.method!=='string'){error(msg?.id??null,-32600,'Invalid Request');continue;}
 if(!('id' in msg)){
  if(msg.method==='notifications/initialized'&&initialized)ready=true;
  continue; // 通知无响应；未实现的通知忽略。
 }
 const {id,method,params={}}=msg;
 if(method==='ping'){result(id,{});continue;}
 if(method==='initialize'){
  if(initialized){error(id,-32600,'Already initialized');continue;}
  if(params.protocolVersion!==VERSION){error(id,-32602,'仅支持教学版本 '+VERSION);continue;}
  initialized=true;result(id,{protocolVersion:VERSION,serverInfo:{name:'学习用模拟MCP',version:'0.1.0'},capabilities:{tools:{}},instructions:'只操作模拟记事本；同步JS变量跨调用保留。js_reset不撤销文档。不接入真实桌面。'});continue;
 }
 if(!ready){error(id,-32002,'初始化未完成');continue;}
 if(method==='tools/list'){result(id,{tools});continue;}
 if(method!=='tools/call'){error(id,-32601,'Method not found');continue;}
 const args=params.arguments??{};
 if(!tools.some(t=>t.name===params.name)){error(id,-32602,'未知工具');continue;}
 if(typeof args!=='object'||Array.isArray(args)||args===null){error(id,-32602,'arguments应为对象');continue;}
 if(params.name==='js_reset'){
  if(Object.keys(args).length){error(id,-32602,'js_reset不接收参数');continue;}
  reset();result(id,toolResult({reset:true,externalDocumentPreserved:true}));continue;
 }
 if(typeof args.code!=='string'||Object.keys(args).some(k=>k!=='code')||args.code.length>4000){error(id,-32602,'js需要code字符串且无额外参数');continue;}
 try{
  const value=new vm.Script(args.code,{filename:'trusted-fixture.js'}).runInContext(context,{timeout:80});
  if(value&&typeof value.then==='function')throw new Error('模拟器不支持异步/顶层await');
  result(id,toolResult(value));
 }catch(e){result(id,toolResult({error:e.message,rollback:false},true));}
}
process.stderr.write('模拟服务stdin已关闭，正常退出\n');
