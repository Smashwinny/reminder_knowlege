decoder_lab —— wx-cli-again 上游图片解码器的合成交互实验
==========================================================
隐私红线：全程零真实微信数据。合成材料 = Pillow 生成的 87 字节 PNG（8x8 橙底蓝点）。

src/decoder/ 下 mod.rs / v1_xor.rs / v2.rs 为上游仓库 src/attachment/decoder/ 的原样拷贝
（jackwener/wx-cli-again, Apache-2.0），未改一行；本目录只新增 main.rs 实验驱动。

复现：cargo run --release
实测输出（2026-10-03，Windows 11）：
  实验1 legacy_xor 往返：decoder=legacy_xor format=png 87 字节逐字节一致 ✅
  实验2 v1_aes 往返：真实容器格式 + 固定 key cfcd208495d565ef，逐字节一致 ✅
  实验3 负向：全零垃圾/空文件/V2 缺 key 三拒 ✅
