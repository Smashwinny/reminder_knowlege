"""烘焙贴图实验：复用上游 bake_texture 模块，仅修一个上游 bug。

上游 tsr/bake_texture.py 的 positions_to_colors() 里
    positions = torch.tensor(positions_texture.reshape(-1, 4)[:, :-1])
没有 .to(device)，--device cuda:0 时 query_triplane 报
"grid is on cpu, different from other tensors on cuda:0"。
本脚本原样复刻 bake 路径，只把这一行钉到 scene_code 所在设备。

用法（在 repo 目录下）：
  PYTHONPATH=../exercise python ../exercise/run_bake.py <image> <out_dir>
"""
import logging
import os
import sys
import time

import numpy as np
import torch
import xatlas
from PIL import Image

from tsr.bake_texture import make_atlas, rasterize_position_atlas
from tsr.system import TSR

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)


def positions_to_colors_fixed(model, scene_code, positions_texture, texture_resolution):
    positions = torch.tensor(
        positions_texture.reshape(-1, 4)[:, :-1], device=scene_code.device
    )  # <-- 上游唯一的差异：钉设备
    with torch.no_grad():
        queried_grid = model.renderer.query_triplane(model.decoder, positions, scene_code)
    rgb_f = queried_grid["color"].cpu().numpy().reshape(-1, 3)
    rgba_f = np.insert(rgb_f, 3, positions_texture.reshape(-1, 4)[:, -1], axis=1)
    rgba_f[rgba_f[:, -1] == 0.0] = [0, 0, 0, 0]
    return rgba_f.reshape(texture_resolution, texture_resolution, 4)


def main():
    image_path, output_dir = sys.argv[1], sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    model = TSR.from_pretrained("pretrained", config_name="config.yaml", weight_name="model.ckpt")
    model.renderer.set_chunk_size(8192)
    model.to(device)

    import rembg
    from tsr.utils import remove_background, resize_foreground

    image = remove_background(Image.open(image_path), rembg.new_session())
    image = resize_foreground(image, 0.85)
    image = np.array(image).astype(np.float32) / 255.0
    image = image[:, :, :3] * image[:, :, 3:4] + (1 - image[:, :, 3:4]) * 0.5
    image = Image.fromarray((image * 255.0).astype(np.uint8))

    with torch.no_grad():
        scene_codes = model([image], device=device)
    meshes = model.extract_mesh(scene_codes, has_vertex_color=False, resolution=256)
    mesh = meshes[0]

    t0 = time.time()
    texture_resolution = 1024
    texture_padding = round(max(2, texture_resolution / 256))
    atlas = make_atlas(mesh, texture_resolution, texture_padding)
    positions_texture = rasterize_position_atlas(
        mesh, atlas["vmapping"], atlas["indices"], atlas["uvs"],
        texture_resolution, texture_padding,
    )
    colors_texture = positions_to_colors_fixed(model, scene_codes[0], positions_texture, texture_resolution)
    logging.info("bake finished in %.2fms", (time.time() - t0) * 1000)

    out_mesh = os.path.join(output_dir, "mesh_tex.glb")
    xatlas.export(
        out_mesh,
        mesh.vertices[atlas["vmapping"]],
        atlas["indices"],
        atlas["uvs"],
        mesh.vertex_normals[atlas["vmapping"]],
    )
    Image.fromarray((colors_texture * 255.0).astype(np.uint8)).transpose(
        Image.FLIP_TOP_BOTTOM
    ).save(os.path.join(output_dir, "texture.png"))
    logging.info("saved %s", out_mesh)


if __name__ == "__main__":
    main()
