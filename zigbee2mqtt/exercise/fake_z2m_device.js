// 实验步骤5：模拟 Zigbee2MQTT + Home Assistant 的"自动发现"握手
// 这一步手动复刻 Z2M（homeassistant.enabled=true 时）对每台设备做的事：
//   1) 向 homeassistant/<组件>/<设备ID>/<对象ID>/config 发布发现消息 → HA 据此自动创建传感器
//   2) 向 zigbee2mqtt/<设备名> 发布设备状态 → HA 订阅后实时刷新数值
// 运行的同时保持 mqtt_observer.js 订阅，就能亲眼看到 HA"看见"设备的全过程。
const mqtt = require('mqtt');
const client = mqtt.connect('mqtt://127.0.0.1:1883', { clientId: 'fake_z2m_' + Date.now() });

const DEVICE = 'livingroom_aqara_sensor';

client.on('connect', () => {
    console.log('[fake-z2m] 已连接 broker，开始模拟一台 Aqara 温湿度传感器上线\n');

    // ① HA MQTT discovery：三条 config 消息 = HA 里自动多出 3 个传感器
    const discoveryMsgs = [
        ['homeassistant/sensor/' + DEVICE + '/temperature/config', {
            name: 'Temperature', uniq_id: DEVICE + '_temperature',
            dev_cla: 'temperature', unit_of_meas: '°C',
            stat_t: 'zigbee2mqtt/' + DEVICE, val_tpl: '{{ value_json.temperature }}',
            dev: { ids: [DEVICE], name: 'Aqara 温湿度传感器', mf: 'Aqara', mdl: 'WSDCGQ11LM' },
        }],
        ['homeassistant/sensor/' + DEVICE + '/humidity/config', {
            name: 'Humidity', uniq_id: DEVICE + '_humidity',
            dev_cla: 'humidity', unit_of_meas: '%',
            stat_t: 'zigbee2mqtt/' + DEVICE, val_tpl: '{{ value_json.humidity }}',
            dev: { ids: [DEVICE] },
        }],
        ['homeassistant/sensor/' + DEVICE + '/battery/config', {
            name: 'Battery', uniq_id: DEVICE + '_battery',
            dev_cla: 'battery', unit_of_meas: '%',
            stat_t: 'zigbee2mqtt/' + DEVICE, val_tpl: '{{ value_json.battery }}',
            dev: { ids: [DEVICE] },
        }],
    ];
    for (const [topic, payload] of discoveryMsgs) {
        client.publish(topic, JSON.stringify(payload), { retain: true });
        console.log('[fake-z2m] 发布发现消息 →', topic);
    }

    // ② 设备状态上报（就像传感器真的每 5 秒上报一次）
    const readings = [
        { temperature: 24.5, humidity: 55, battery: 87 },
        { temperature: 24.6, humidity: 54, battery: 87 },
        { temperature: 24.8, humidity: 53, battery: 86 },
    ];
    let i = 0;
    const timer = setInterval(() => {
        const state = readings[i % readings.length];
        i++;
        client.publish('zigbee2mqtt/' + DEVICE, JSON.stringify(state));
        console.log('[fake-z2m] 上报状态 → zigbee2mqtt/' + DEVICE, JSON.stringify(state));
        if (i >= 6) { clearInterval(timer); setTimeout(() => { client.end(); console.log('\n[fake-z2m] 模拟结束'); process.exit(0); }, 500); }
    }, 2000);
});
