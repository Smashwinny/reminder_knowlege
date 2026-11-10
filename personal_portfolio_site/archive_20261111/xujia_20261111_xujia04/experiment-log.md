# 第4项真实实验日志
日期：2026-11-11（Asia/Shanghai）

实验是原创轻量网页，不是Step/WorkBuddy或完整3D生成复现。

## 准备（已执行）
`npm install --prefix ../test-tools playwright --ignore-scripts --no-audit --no-fund`；依赖版本已写package-lock。

## 1 固定实验输入（已执行）
目的/验证：读取文件与sha256，不执行上游安装器。
命令：`python3 audit.py`（Node实际用NODE_PATH=../test-tools/node_modules）
结果：无外部src、1个内联SVG、viewport与减弱运动规则存在，3913字节；哈希见JSON。

## 2 重现已知布局缺陷（已执行）
目的/验证：保存baseline-360.png；测试若未发现溢出会报错。
命令：`node test.cjs baseline`（Node实际用NODE_PATH=../test-tools/node_modules）
结果：360px视口，scrollWidth=1100，overflow=true；缺陷按预期出现。

## 3 修复后跨尺寸验收（已执行）
目的/验证：保存after-*.png，与缺陷版保留同内容对照。
命令：`node test.cjs responsive`（Node实际用NODE_PATH=../test-tools/node_modules）
结果：360/768/1440均scrollWidth=视口宽；3张作品卡存在；页面错误0。

## 4 键盘与悬停交互（已执行）
目的/验证：真实Chrome DOM与计算样式，不是源码关键词断言。
命令：`node test.cjs interaction`（Node实际用NODE_PATH=../test-tools/node_modules）
结果：Enter选择网页：可见2卡，pressed=true，焦点web；hover得到matrix3d。

## 5 减弱动态效果（已执行）
目的/验证：仅当前浏览器原型；未覆盖真机传感器和读屏。
命令：`node test.cjs reduced`（Node实际用NODE_PATH=../test-tools/node_modules）
结果：浏览器仿真reduce后，transform=none、transition=0s，页面错误0。

## 原始输出
```text
执行日期 2026-11-11 Asia/Shanghai
Python 3.13.5
v24.22.1
Google Chrome 156.0.8078.47 
$ python3 audit.py
{
  "bytes": 3913,
  "sha256": "51ec693782dd054695336404b429fa36c19319a1a2b4ed24b1191acbe343d099",
  "external_src": 0,
  "svg": 1,
  "has_reduced_motion": true,
  "has_viewport": true
}
$ NODE_PATH=../test-tools/node_modules node test.cjs baseline
{
  "mode": "baseline",
  "viewport": 360,
  "scrollWidth": 1100,
  "overflow": true,
  "errors": []
}
$ NODE_PATH=../test-tools/node_modules node test.cjs responsive
{
  "mode": "responsive",
  "samples": [
    {
      "viewport": 360,
      "scrollWidth": 360,
      "cards": 3
    },
    {
      "viewport": 768,
      "scrollWidth": 768,
      "cards": 3
    },
    {
      "viewport": 1440,
      "scrollWidth": 1440,
      "cards": 3
    }
  ],
  "errors": []
}
$ NODE_PATH=../test-tools/node_modules node test.cjs interaction
{
  "mode": "interaction",
  "visible": 2,
  "pressed": "true",
  "focus": "web",
  "transform": "matrix3d(0.978148, 0, -0.207912, 0.00025989, 0, 1, 0, 0, 0.207912, 0, 0.978148, -0.00122268, 0, 0, 0, 1)",
  "errors": []
}
$ NODE_PATH=../test-tools/node_modules node test.cjs reduced
{
  "mode": "reduced",
  "style": {
    "transform": "none",
    "transition": "0s"
  },
  "errors": []
}

```
## 待验证
付费/账户模型调用、真实3D、完整上游React组件、真机、部署、用户效果均未执行。

## 交付ZIP全新解压重放（已执行）
2026-11-11（Asia/Shanghai）。从exercise.zip新解压后执行README全部命令；npm ci --ignore-scripts；五步均成功，结果与初次相同。不是独立审核。完整输出：
```text
$ npm ci --ignore-scripts --no-audit --no-fund

added 2 packages in 337ms
{
  "bytes": 3913,
  "sha256": "51ec693782dd054695336404b429fa36c19319a1a2b4ed24b1191acbe343d099",
  "external_src": 0,
  "svg": 1,
  "has_reduced_motion": true,
  "has_viewport": true
}
{
  "mode": "baseline",
  "viewport": 360,
  "scrollWidth": 1100,
  "overflow": true,
  "errors": []
}
{
  "mode": "responsive",
  "samples": [
    {
      "viewport": 360,
      "scrollWidth": 360,
      "cards": 3
    },
    {
      "viewport": 768,
      "scrollWidth": 768,
      "cards": 3
    },
    {
      "viewport": 1440,
      "scrollWidth": 1440,
      "cards": 3
    }
  ],
  "errors": []
}
{
  "mode": "interaction",
  "visible": 2,
  "pressed": "true",
  "focus": "web",
  "transform": "matrix3d(0.978148, 0, -0.207912, 0.00025989, 0, 1, 0, 0, 0.207912, 0, 0.978148, -0.00122268, 0, 0, 0, 1)",
  "errors": []
}
{
  "mode": "reduced",
  "style": {
    "transform": "none",
    "transition": "0s"
  },
  "errors": []
}

```
