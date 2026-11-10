首次真实 validateRig 输出：rig.view: margins must leave a positive viewport。
原夹具误把 padTop/padSide=10 当像素；改为归一化 .05 后重试。没有改上游代码。
