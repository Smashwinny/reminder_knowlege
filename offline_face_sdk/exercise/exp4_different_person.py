# -*- coding: utf-8 -*-
"""
实验4：区分度真伪测试 —— 用公开授权样例头像（randomuser.me，允许mockup使用）
当"另一个人"，检验 1.jpg/2.png 是否同一人、以及 SDK 能否把不同人分开。
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
import run as sdk

def get_feature(img, name):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    boxes, scores = get_face_boundingbox(img)
    if len(boxes) == 0:
        print(f'  !! 未检出人脸: {name}')
        return None
    lm = get_face_landmark(gray, boxes[0])
    _, f = get_face_feature(img, lm)
    return f

EXER = os.path.dirname(os.path.abspath(__file__))
names = {'1.jpg': os.path.join(REPO, 'test/1.jpg'), '2.png': os.path.join(REPO, 'test/2.png'),
         '头像男32': os.path.join(EXER, 'avatar_m32.jpg'), '头像女47': os.path.join(EXER, 'avatar_w47.jpg')}
feats = {}
for k, p in names.items():
    img = cv2.imread(p, cv2.IMREAD_COLOR)
    feats[k] = get_feature(img, k)

ks = list(feats.keys())
print('相似度矩阵（score>=75 判同一人）:')
print(f'{"":10s}' + ''.join(f'{k:>10s}' for k in ks))
for a in ks:
    row = f'{a:10s}'
    for b in ks:
        if feats[a] is None or feats[b] is None:
            row += f'{"n/a":>10s}'
        else:
            s = sdk.get_similarity(feats[a], feats[b])
            row += f'{s:9.1f}' + ('*' if s >= 75 else ' ')
    print(row)

print('\n余弦相似度对照: score = (cos+1)*50')
for a, b in [('1.jpg', '2.png'), ('1.jpg', '头像男32'), ('1.jpg', '头像女47'), ('头像男32', '头像女47')]:
    if feats[a] is not None and feats[b] is not None:
        cos = float(np.sum(feats[a] * feats[b]))
        print(f'  {a} vs {b}: cos = {cos:.3f} (score {(cos+1)*50:.1f})')
