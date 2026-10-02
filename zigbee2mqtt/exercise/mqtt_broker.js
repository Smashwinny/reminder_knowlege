// 实验步骤2：本地 MQTT broker（aedes），代替要单独安装的 Mosquitto
// aedes 1.x 必须用 Aedes.createBroker() 异步创建，直接 new 会导致客户端永远收不到 CONNACK
const { Aedes } = require('aedes');
const { createServer } = require('net');

async function main() {
    const aedes = await Aedes.createBroker();
    const server = createServer(aedes.handle);

    // 每有一条消息经过 broker 就打印主题和字节数（截断正文，避免刷屏）
    aedes.on('publish', (packet, client) => {
        const topic = packet.topic;
        if (topic.startsWith('$SYS')) return;
        const body = packet.payload.toString().slice(0, 120);
        const who = client ? client.id : '(broker内部)';
        console.log(`[broker] ${who} 发布 → ${topic} | ${body}`);
    });

    aedes.on('clientReady', (client) => console.log(`[broker] 客户端上线: ${client.id}`));

    server.listen(1883, () => console.log('[broker] 本地 MQTT broker 已启动: mqtt://127.0.0.1:1883'));
}

main().catch((e) => { console.error('broker 启动失败:', e); process.exit(1); });
