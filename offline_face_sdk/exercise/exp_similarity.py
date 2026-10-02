# -*- coding: utf-8 -*-
"""
实验3：相似度矩阵 —— 同一张脸的"变装"会不会被认出来？
对 1.jpg 检出的人脸区域做5种变换（水平翻转/旋转10度/高斯模糊/提亮/缩小再放大），
再和 2.png（另一个人）互相打分，输出 7x7 分数矩阵和是否同一人的判定。
阈值75 => score=(cos+1)*50, cos>=0.5 判同一人。
"""
import os, sys
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'repo'))
os.chdir(REPO)
sys.path.insert(0, REPO)

import cv2
import numpy as np
from face_detect.detect_imgs import get_face_boundingbox
from face_landmark.GetLandmark import get_face_landmark
from face_feature.GetFeature import get_face_feature
import run as sdk  # 复用 GetImageInfo + get_similarity

def get_feature(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    boxes, scores = get_face_boundingbox(img)
    if len(boxes) == 0:
        return None
    lm = get_face_landmark(gray, boxes[0])
    _, f = get_face_feature(img, lm)
    return f

def cosine(a, b):
    return float(np.sum(a * b) / (np.linalg.norm(a) * np.linalg.norm(b)))

img1 = cv2.imread('test/1.jpg', cv2.IMREAD_COLOR)
img2 = cv2.imread('test/2.png', cv2.IMREAD_COLOR)

# 取 1.jpg 第一张脸的 bbox，切出来做变换
gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
boxes, _ = get_face_boundingbox(img1)
x1, y1, x2, y2 = np.round(boxes[0].numpy()).astype(int)
pad = int(0.3 * max(x2 - x1, y2 - y1))
H, W = img1.shape[:2]
crop = img1[max(0, y1-pad):min(H, y2+pad), max(0, x1-pad):min(W, x2+pad)].copy()

variants = {
    '原图脸':   crop,
    '水平翻转': cv2.flip(crop, 1),
    '旋转10度': cv2.resize(cv2.warpAffine(crop, cv2.getRotationMatrix2D((crop.shape[1]//2, crop.shape[0]//2), 10, 1.0), (crop.shape[1], crop.shape[0])), (crop.shape[1], crop.shape[0])),
    '高斯模糊': cv2.GaussianBlur(crop, (9, 9), 0),
    '提亮1.4x': np.clip(crop.astype(np.float32) * 1.4, 0, 255).astype(np.uint8),
    '缩小再放大': cv2.resize(cv2.resize(crop, (crop.shape[1]//4, crop.shape[0]//4)), (crop.shape[1], crop.shape[0])),
}

names = list(variants.keys()) + ['2.png(另一人)']
feats = [get_feature(v) for v in variants.values()]
f2 = get_feature(img2)
feats.append(f2)

print(f'{"":12s}' + ''.join(f'{n[:8]:>10s}' for n in names))
for i, na in enumerate(names):
    row = f'{na[:12]:12s}'
    for j, nb in enumerate(names):
        s = sdk.get_similarity(feats[i], feats[j])
        mark = '*' if s >= 75 else ' '
        row += f'{s:9.1f}{mark}'
    print(row)
print('\n* = 判为同一人 (score>=75, 即 cos>=0.5)')
