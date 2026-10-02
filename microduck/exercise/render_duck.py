# -*- coding: utf-8 -*-
"""渲染鸭子 STAND 姿态图像（供 PDF 图文并茂）"""
import mujoco
import numpy as np

SCENE = r"F:\reminder\microduck\repo_rl\src\mjlab_microduck\robot\microduck\scene.xml"
model = mujoco.MjModel.from_xml_path(SCENE)
data = mujoco.MjData(model)
mujoco.mj_resetDataKeyframe(model, data, mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_KEY, "STAND"))
# 先跑 0.5 秒让它进入自然站立状态
for _ in range(250):
    mujoco.mj_step(model, data)

try:
    rend = mujoco.Renderer(model, height=480, width=640)
    cam = mujoco.MjvCamera()
    cam.lookat[:] = [0, 0, 0.08]
    cam.distance = 0.55
    cam.azimuth = 150
    cam.elevation = -12
    mujoco.mj_forward(model, data)
    rend.update_scene(data, cam)
    png = rend.render()
    from PIL import Image
    Image.fromarray(png).save("duck_stand.png")
    print("saved duck_stand.png", png.shape)
except Exception as e:
    print("render failed:", type(e).__name__, e)
