// 12306-mcp 学习实验客户端
// 通过 MCP stdio 协议启动 ../repo/build/index.js，依次调用工具链：
//   1) listTools                    — 看服务器注册了哪些工具
//   2) get-current-date             — 基础工具：上海时区当前日期
//   3) get-station-code-of-citys    — 基础工具：城市名 -> 车站代码
//   4) get-tickets                  — 核心工具：查明天 北京->上海 高铁余票
//   5) get-train-route-stations     — 核心工具：查第一个车次的经停站
// 每步打印真实返回，失败即非零退出。
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { fileURLToPath } from 'node:url';

const SERVER = fileURLToPath(new URL('../repo/build/index.js', import.meta.url));

function fmt(title, obj, max = 1200) {
    let s = typeof obj === 'string' ? obj : JSON.stringify(obj, null, 1);
    if (s.length > max) s = s.slice(0, max) + ` …(截断，共 ${s.length} 字符)`;
    console.log(`\n===== ${title} =====\n${s}`);
}

async function call(client, name, args) {
    const r = await client.callTool({ name, arguments: args });
    if (r.isError) throw new Error(`${name} 返回错误: ${JSON.stringify(r.content).slice(0, 300)}`);
    return r.content?.map(c => c.text ?? JSON.stringify(c)).join('\n');
}

const transport = new StdioClientTransport({ command: 'node', args: [SERVER] });
const client = new Client({ name: 'experiment-client', version: '1.0.0' }, { capabilities: {} });
await client.connect(transport);
try {
    // 1) 工具清单
    const tools = await client.listTools();
    fmt('1) listTools：服务器注册的工具', tools.tools.map(t => `${t.name} — ${t.description.slice(0, 60)}`), 2000);

    // 2) 当前日期
    const date = await call(client, 'get-current-date', {});
    fmt('2) get-current-date', date, 300);

    // 3) 城市 -> 车站代码
    const codes = await call(client, 'get-station-code-of-citys', { citys: '北京|上海' });
    fmt('3) get-station-code-of-citys(北京|上海)', codes, 600);

    // 4) 明天 北京->上海 高铁余票
    const tomorrow = new Date(Date.now() + 86400000).toISOString().slice(0, 10);
    const tickets = await call(client, 'get-tickets', {
        date: tomorrow, fromStation: '北京', toStation: '上海', trainFilterFlags: 'G',
    });
    fmt(`4) get-tickets(明天 ${tomorrow} 北京->上海 高铁G)`, tickets, 1500);

    // 5) 第一个车次的经停站（该工具入参为 trainCode + departDate）
    const m = tickets.match(/^([GDCKTZ]\d{1,5})\s/m);
    if (m) {
        const route = await call(client, 'get-train-route-stations', {
            trainCode: m[1], departDate: tomorrow,
        });
        fmt(`5) get-train-route-stations(${m[1]}次)`, route, 1200);
    } else {
        console.log('\n===== 5) 跳过：第 4 步结果中未解析到车次号 =====');
    }
    console.log('\n✅ 全部调用成功');
} finally {
    await client.close();
}
