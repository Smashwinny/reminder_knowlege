//! 实验主程序：用**上游 wx-cli-again 的真实 decoder 源码**（src/decoder/ 下三文件，
//! 原样拷贝自 repo/src/attachment/decoder/，Apache-2.0）对**合成数据**做往返解码。
//!
//! 实验设计（拾遗 task 1c5dba8b，隐私红线：全程零真实微信数据）：
//!   1. legacy_xor 往返：把一张合成 PNG（8x8 橙底蓝点，Pillow 生成）逐字节 XOR 成
//!      伪 .dat → 上游 dispatch() 自动反推 key 并还原，逐字节比对原图。
//!   2. v1_aes 往返：按上游 v2.rs 注释里的真实 V2 文件格式手工封一个容器
//!      （magic 换成 V1 + 固定 key "cfcd208495d565ef"）→ 上游 decode() 解出，比对原图。
//!   3. 负向：全零字节必须被所有 magic 探测拒绝；空文件必须报"空 .dat 文件"。

mod decoder;

use anyhow::{Context, Result};
use decoder::{dispatch, V2KeyMaterial};

/// 合成 PNG：8x8 RGB，橙底 (255,80,40) + 蓝点 (0,200,255) at (3,3)。87 字节。
const SYNTH_PNG: [u8; 87] = [
    0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0x00, 0x00, 0x00, 0x0d, 0x49, 0x48, 0x44,
    0x52, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x08, 0x08, 0x02, 0x00, 0x00, 0x00, 0x4b,
    0x6d, 0x29, 0xdc, 0x00, 0x00, 0x00, 0x1e, 0x49, 0x44, 0x41, 0x54, 0x78, 0x9c, 0x63, 0xfc,
    0x1f, 0xa0, 0xc1, 0x80, 0x0d, 0x30, 0x61, 0x15, 0x25, 0x4e, 0x82, 0xb1, 0xe2, 0x3a, 0xb2,
    0x04, 0x23, 0x2d, 0xec, 0x40, 0x03, 0x00, 0x4e, 0xd2, 0x04, 0x4d, 0x2b, 0x20, 0x6e, 0xfb,
    0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82,
];

/// 微信 legacy XOR 的模拟加密：全文件单字节 XOR（与上游 v1_xor.rs 的解密互逆）。
fn legacy_xor_encode(plain: &[u8], key: u8) -> Vec<u8> {
    plain.iter().map(|b| b ^ key).collect()
}

/// 按上游 v2.rs 注释的容器格式封包：
/// `[6B magic][4B aes_size LE][4B xor_size LE][1B padding][AES-ECB(PKCS7) 密文][raw][xor 段]`
/// xor_size = 0、raw 段为空；aes_size 记录 PKCS7 之前的明文长度。
fn v1_container_encode(plain: &[u8], key: &[u8; 16], magic: [u8; 6]) -> Vec<u8> {
    use aes::cipher::{generic_array::GenericArray, BlockEncrypt, KeyInit};

    // PKCS7：明文先补齐到 16 的倍数（正好整除时再加一整块 0x10）
    let mut padded = plain.to_vec();
    let pad = 16 - (padded.len() % 16);
    padded.extend(std::iter::repeat(pad as u8).take(pad));

    let aes = aes::Aes128::new(GenericArray::from_slice(key));

    let mut cipher = Vec::with_capacity(padded.len());
    for chunk in padded.chunks_exact(16) {
        let mut block = GenericArray::clone_from_slice(chunk);
        aes.encrypt_block(&mut block);
        cipher.extend_from_slice(&block);
    }

    let mut out = Vec::new();
    out.extend_from_slice(&magic);
    out.extend_from_slice(&(plain.len() as u32).to_le_bytes()); // aes_size = 原始明文长
    out.extend_from_slice(&0u32.to_le_bytes()); // xor_size = 0
    out.push(0u8); // padding 占位字节
    out.extend_from_slice(&cipher);
    out
}

fn check_roundtrip(name: &str, dat: &[u8], v2_key: V2KeyMaterial) -> Result<()> {
    let img = dispatch(dat, v2_key).context(format!("{}：dispatch 返回 Err", name))?;
    println!(
        "  [{}] decoder={} format={} 解码 {} 字节",
        name,
        img.decoder,
        img.format,
        img.data.len()
    );
    anyhow::ensure!(
        img.data == SYNTH_PNG,
        "{}：解码产物与原图不一致（{} vs {} 字节）",
        name,
        img.data.len(),
        SYNTH_PNG.len()
    );
    anyhow::ensure!(img.format == "png", "{}：格式探测应为 png，实际 {}", name, img.format);
    println!("  [{}] 逐字节比对原图：一致 ✅", name);
    Ok(())
}

fn main() -> Result<()> {
    println!("=== 实验 1：legacy_xor 往返（合成 PNG → XOR 伪 .dat → 上游 dispatch 解码）===");
    let xor_key = 0x5Au8; // 任意假想微信 key，上游应自动反推
    let dat = legacy_xor_encode(&SYNTH_PNG, xor_key);
    check_roundtrip("legacy_xor", &dat, V2KeyMaterial::default())?;

    println!();
    println!("=== 实验 2：v1_aes 往返（真实 V1 容器格式 + 固定 key cfcd208495d565ef）===");
    let fixed_key: [u8; 16] = *b"cfcd208495d565ef"; // md5("0")[:16]，上游源码里的常量
    let v1_dat = v1_container_encode(&SYNTH_PNG, &fixed_key, decoder::V1_MAGIC);
    check_roundtrip("v1_aes", &v1_dat, V2KeyMaterial::default())?;

    println!();
    println!("=== 实验 3：负向测试（必须全部被拒）===");
    let zeros = vec![0u8; 64];
    match dispatch(&zeros, V2KeyMaterial::default()) {
        Err(e) => println!("  [全零垃圾] 正确拒绝：{} ✅", e),
        Ok(img) => anyhow::bail!("全零垃圾居然被解成 {}，异常！", img.format),
    }
    match dispatch(&[], V2KeyMaterial::default()) {
        Err(e) => println!("  [空文件] 正确拒绝：{} ✅", e),
        Ok(_) => anyhow::bail!("空文件居然解码成功，异常！"),
    }
    // V2 magic 但谎称超长 aes_size → 应报"超过文件长度"
    let mut bad_v2 = decoder::V2_MAGIC.to_vec();
    bad_v2.extend_from_slice(&10_000u32.to_le_bytes());
    bad_v2.extend_from_slice(&0u32.to_le_bytes());
    bad_v2.push(0);
    bad_v2.extend_from_slice(&[0u8; 32]);
    match dispatch(&bad_v2, V2KeyMaterial::default()) {
        Err(e) => println!("  [V2 超长声明] 正确拒绝：{} ✅", e),
        Ok(_) => anyhow::bail!("超长声明居然解码成功，异常！"),
    }

    println!();
    println!("全部实验通过：上游 decoder 源码 + 合成数据，双向解码与负向护栏均符合预期。");
    Ok(())
}
