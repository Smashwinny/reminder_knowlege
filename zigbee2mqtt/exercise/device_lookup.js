// 实验步骤4：zigbee-herdsman-converters —— Zigbee2MQTT 的"万国翻译官"
// 加载 repo 自带依赖里的设备定义库，统计规模，并按型号查两个典型设备：
//   小米 Aqara 温湿度传感器（电池供电传感器）+ 宜家 TRADFRI 灯泡（市电供电执行器）
// 注意：原始设备定义里 exposes 未必直接给出（老定义用 extend 组合特性），
//       要用 converters 自带的 prepareDefinition() 展开成最终特性列表——这正是 Z2M 运行时的做法。
const path = require('path');
const repoNodeModules = path.resolve(__dirname, '../repo/node_modules');
const zh = require(path.join(repoNodeModules, 'zigbee-herdsman-converters'));
const pkg = require(path.join(repoNodeModules, 'zigbee-herdsman-converters/package.json'));
const definitions = require(path.join(repoNodeModules, 'zigbee-herdsman-converters/dist/devices/index.js')).default;

console.log('zigbee-herdsman-converters 版本:', pkg.version);
console.log(`内置设备定义总数: ${definitions.length}`);

const vendors = new Set(definitions.map((d) => d.vendor));
console.log(`覆盖厂商数: ${vendors.size}`);

const countVendor = (kw) => definitions.filter((d) => (d.vendor || '').toLowerCase().includes(kw)).length;
console.log(`其中 Xiaomi: ${countVendor('xiaomi')} 款，Aqara: ${countVendor('aqara')} 款，IKEA: ${countVendor('ikea')} 款`);

function show(model, title) {
    const raw = definitions.find((x) => x.model === model);
    console.log(`\n===== ${title}（model: ${model}）=====`);
    if (!raw) { console.log('  未找到！'); return; }
    console.log(`  厂商: ${raw.vendor} | 描述: ${raw.description}`);
    const d = zh.prepareDefinition(raw);
    const exposes = typeof d.exposes === 'function' ? d.exposes(d, {}) : d.exposes;
    console.log('  支持的 Zigbee 特性（exposes）:');
    for (const e of exposes) {
        const access = e.access ? ` [读写属性: ${e.access}]` : '';
        console.log(`    - ${e.type}${e.name ? ' ' + e.name : ''}${access}${e.unit ? ' 单位:' + e.unit : ''}`);
    }
}

show('WSDCGQ11LM', '小米 Aqara 温湿度传感器');
show('LED1623G12', '宜家 TRADFRI 灯泡');
