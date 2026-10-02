"""torchmcubes 兼容 shim（experiment 用，避免本地编译 CUDA 扩展）。

接口对齐 tatsy/torchmcubes：
    marching_cubes(volume: Tensor[D,H,W], iso: float) -> (verts [N,3] float, faces [M,3] int64)
实现：scikit-image 的 lewiner marching cubes（纯 CPU，256^3 体积秒级完成）。
GPU 上的主计算（DINOv2 + transformer + triplane 查询）不受影响，只在最后
"密度场 -> 网格"一步落到 CPU，与上游 isosurface.py 的 CPU 回退路径行为一致。
"""
import numpy as np
import torch
from skimage import measure


def marching_cubes(volume, isolevel=0.0):
    vol = volume.detach().cpu().numpy().astype(np.float64)
    verts, faces, _normals, _values = measure.marching_cubes(vol, level=float(isolevel))
    v = torch.from_numpy(np.ascontiguousarray(verts, dtype=np.float32))
    f = torch.from_numpy(np.ascontiguousarray(faces, dtype=np.int64))
    return v, f


def grid_interp(grid, verts):
    """三线性插值（torchmcubes 的另一个导出函数，上游代码未用到，补齐以防万一）。"""
    g = grid.detach().cpu().numpy().astype(np.float64)
    p = verts.detach().cpu().numpy()
    out = torch.nn.functional.grid_sample(
        torch.from_numpy(g)[None, None].float(),
        (p / torch.tensor([g.shape[0] - 1, g.shape[1] - 1, g.shape[2] - 1])).float()[None, None] * 2 - 1,
        align_corners=True,
        mode="bilinear",
        padding_mode="border",
    )
    return out.reshape(-1, 1)
