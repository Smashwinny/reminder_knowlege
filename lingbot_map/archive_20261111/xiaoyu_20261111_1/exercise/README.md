# LingBot-Map 背景数学练习（原创）

这不是上游模型或完整SLAM/VIO实现。仅用公开论文概念、合成数据；无私密输入、无用户密钥、无网络API。

## 重放
需要Python3及NumPy（实测Python3.13.5/NumPy2.5.4）。

```bash
python3 -m venv .venv
.venv/bin/pip install numpy==2.5.4
.venv/bin/python exercise/lab.py env
.venv/bin/python exercise/lab.py scale
.venv/bin/python exercise/lab.py context
.venv/bin/python exercise/lab.py graph
.venv/bin/python exercise/lab.py imu
.venv/bin/python exercise/lab.py verify
```
解压ZIP后从exercise上级运行。已安装numpy时可直接python3；不会安装torch、下载权重或访问GPU。

scale：理想针孔尺度歧义；context：论文公式token账本，不是显存实测；graph：二维平移线性加权最小二乘与正确/错误回环；imu：固定姿态、已去重力、一维常加速度预积分直觉。
verify运行五组并保存results.json；graph-data.npz为合成轨迹，不使用pickle。

源公式：arXiv2604.14141v3 §3.2、1512.02363v3 §V–VI；实现由本worker原创，不复用上游代码。结果与断言均非独立审核、非上游测试。
