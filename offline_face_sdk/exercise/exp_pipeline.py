# -*- coding: utf-8 -*-
"""
实验2：全链路流水线观察 —— 对一张图跑 检测→关键点→姿态→特征 全流程
逐阶段计时，检查特征维度，画出检测框+68关键点保存成标注图。
用法：python exp_pipeline.py <图片路径>
"""
import sys, os, time
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'repo'))
os.chdir(REPO)  # SDK 里全是相对路径，必须切到 repo 根目录
sys.path.insert(0, REPO)

import cv2
import numpy as np
from face_detect.detect_imgs import get_face_boundingbox
from face_landmark.GetLandmark import get_face_landmark
from face_feature.GetFeature import get_face_feature
from face_pose.GetPose import get_face_pose

img_path = sys.argv[1] if len(sys.argv) > 1 else 'test/1.jpg'
img = cv2.imread(img_path, cv2.IMREAD_COLOR)
assert img is not None, f'读图失败: {img_path}'
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

t0 = time.time(); boxes, scores = get_face_boundingbox(img); t1 = time.time()
print(f'[检测]   {len(boxes)} 张脸, 耗时 {(t1-t0)*1000:.1f} ms')
for b, s in zip(boxes, scores):
    print(f'  bbox={np.round(b.numpy()).astype(int)} score={float(s):.3f}')

t0 = time.time()
landmarks = [get_face_landmark(gray, b) for b in boxes]
t1 = time.time()
print(f'[关键点] 每脸 {len(landmarks[0])//2} 点, 耗时 {(t1-t0)*1000:.1f} ms')

t0 = time.time()
poses = [get_face_pose(b, l) for b, l in zip(boxes, landmarks)]
t1 = time.time()
print(f'[姿态]   rx/ry/rz = {np.round(poses,1)}, 耗时 {(t1-t0)*1000:.1f} ms')

t0 = time.time()
feats = []
for b, l in zip(boxes, landmarks):
    _, f = get_face_feature(img, l)
    feats.append(f)
t1 = time.time()
f = feats[0]
print(f'[特征]   维度 {f.shape}, L2范数 {np.linalg.norm(f):.4f}, 耗时 {(t1-t0)*1000:.1f} ms')
print(f'  特征前8维: {np.round(f[:8],4)}')

annotated = img.copy()
for b in boxes:
    x1, y1, x2, y2 = np.round(b.numpy()).astype(int)
    cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 220, 60), 2)
for lm in landmarks:
    pts = lm.reshape(-1, 2).detach().numpy().astype(int)
    for i, (x, y) in enumerate(pts):
        color = (60, 160, 255) if i < 17 else (255, 200, 40)  # 下颌蓝，五官黄
        cv2.circle(annotated, (x, y), 2, color, -1)
out = os.path.join(os.path.dirname(__file__), 'annotated_output.jpg')
cv2.imwrite(out, annotated)
print(f'[标注图] 已保存 {out}')
