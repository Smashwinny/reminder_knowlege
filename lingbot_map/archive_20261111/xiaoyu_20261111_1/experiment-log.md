# experiment-log：真实云端运行

运行日：2026-11-11（Asia/Shanghai）。仅CPU合成数学实验，没有LingBot-Map网络推理、GPU测速、真实视频/IMU或硬件验证。

## 六步主实验
完整命令、目的、结果与验证已写入指南第8–9页；下面保留实际标准输出，而非手写预期输出。

```text

=== 2026-11-11T00:57:25+08:00 | python3 exercise/lab.py env ===
{
  "python": "3.13.5",
  "numpy": "2.5.4",
  "platform": "Linux-6.12.113+-x86_64-with-glibc2.41",
  "cuda_devices": 0,
  "scope": "CPU synthetic numerical experiments; no model weights"
}

=== 2026-11-11T00:57:25+08:00 | python3 exercise/lab.py scale ===
{
  "points": 200,
  "scale": 3.7,
  "max_pixel_difference": 5.684341886080802e-14,
  "claim": "same projections do not identify metric scale"
}

=== 2026-11-11T00:57:25+08:00 | python3 exercise/lab.py context ===
{
  "M": 999,
  "anchors": 8,
  "window": 64,
  "rows": [
    {
      "frames": 320,
      "causal_tokens": 321600,
      "gca_tokens": 73848,
      "ratio": 4.354891127721807
    },
    {
      "frames": 1000,
      "causal_tokens": 1005000,
      "gca_tokens": 77928,
      "ratio": 12.8965198644903
    },
    {
      "frames": 10000,
      "causal_tokens": 10050000,
      "gca_tokens": 131928,
      "ratio": 76.17791522648717
    },
    {
      "frames": 100000,
      "causal_tokens": 100500000,
      "gca_tokens": 671928,
      "ratio": 149.56959674250814
    }
  ],
  "increment_per_frame": 6,
  "scope": "analytical token counts, not GPU memory measurement"
}

=== 2026-11-11T00:57:25+08:00 | python3 exercise/lab.py graph ===
{
  "poses": 61,
  "odometry": {
    "rmse_m": 0.9681459453642363,
    "endpoint_error_m": 1.6894439193870525
  },
  "correct_loop": {
    "rmse_m": 0.04135381029076943,
    "endpoint_error_m": 0.0031228168565373957
  },
  "wrong_loop": {
    "rmse_m": 2.296375946233451,
    "endpoint_error_m": 3.9951718828451463
  },
  "normal_equation_residual": 4.206037219940414e-11,
  "scope": "linear weighted least squares = one exact Gauss-Newton step; no rotation/visual front-end"
}

=== 2026-11-11T00:57:25+08:00 | python3 exercise/lab.py imu ===
{
  "samples": 400,
  "dt_s": 0.005,
  "duration_s": 2.0,
  "raw_delta_p_m": 0.899999999999995,
  "raw_delta_v_m_s": 0.8999999999999928,
  "true_delta_p_m": 0.8,
  "true_delta_v_m_s": 0.8,
  "bias_corrected_delta_p_m": 0.799999999999995,
  "bias_corrected_delta_v_m_s": 0.7999999999999928,
  "bias_position_error_m": 0.09999999999999498,
  "scope": "1D preintegration intuition only; no SO(3), covariance, noise or full VIO"
}

=== 2026-11-11T00:57:26+08:00 | python3 exercise/lab.py verify ===
{
  "groups_passed": 5,
  "scope": "author-written deterministic checks, not independent audit or upstream tests"
}

```

## 执行边界
- scale的输入为seed42生成200个三维点；graph为seed7的61位姿圆形轨迹，叠加固定偏置与小噪声。没有训练或评价真实模型。
- 因子图仅估2D平移，固定p0；每条里程计σ=0.03、回环σ=0.01，正规方程采用numpy.linalg.lstsq求解。
- IMU为已去重力且固定姿态的1D演示；偏置被作为已知量修正，没有实现SO(3)、协方差传播、外参或VIO。
- verify的5组是同一作者自写检查，不能称独立审核，也不能称上游测试套件通过。

## 非主实验的工具过程
- 首次环境命令用了python，返回127（不存在），更正为python3后执行成功；没有隐藏这一失败。
- 上游LICENSE和requirements.txt首次请求404，随后从README确认LICENSE.txt和pyproject.toml并成功获取。不存在一个叫requirements.txt的下载成果。
- GitHub账户工具needsAuth；本任务无需账户访问，公开raw及api.github.com的无凭据只读请求成功。没有尝试认证、使用密钥、提交或推送。
- 背景IMU PDF pdftotext打印xref重建警告，随后成功提取正文；原始PDF保留，解读只覆盖明确读取段落。

## PDF真实打印
2026-11-11 00:59:43（Asia/Shanghai），Chromium158.0.8127.18经Playwright输出A4 PDF，pdfinfo确认10页，约989KB。
打印命令：`.print-env/bin/python print_guide.py`。
逐页渲染命令：`pdftoppm -scale-to 1200 -png LingBot-Map-增量学习指南.pdf qa/page`。
检查方法：逐一读取qa/page-01.png至page-10.png图像；各页中文、图、表、命令完整可见，无横向溢出、截字或额外空白页。完整检查见qa/page-check.md。
