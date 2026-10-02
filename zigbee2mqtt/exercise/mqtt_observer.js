// 实验步骤3/5：MQTT 观察员——订阅 zigbee2mqtt/# 和 homeassistant/#
// 1. 抓 zigbee2mqtt 启动时真实发布的 bridge 消息（步骤3）
// 2. 验证 HA 自动发现协议（步骤5）：收到 homeassistant/.../config 说明 HA 能"看见"设备
const mqtt = require('mqtt');

const client = mqtt.connect('mqtt://127.0.0.1:1883', { clientId: 'observer_' + Date.now() });

client.on('connect', () => {
    console.log('[observer] 已连接 broker，订阅 zigbee2mqtt/# 和 homeassistant/#');
    client.subscribe(['zigbee2mqtt/#', 'homeassistant/#']);
});

client.on('message', (topic, payload) => {
    const body = payload.toString().slice(0, 300);
    console.log(`[observer] 收到 ${topic}\n           ${body}`);
});

const SECONDS = Number(process.argv[2] || 25);
setTimeout(() => { console.log(`[observer] ${SECONDS} 秒观察结束，退出`); client.end(); process.exit(0); }, SECONDS * 1000);
