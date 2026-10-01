#!/bin/bash
# 手动按 Docker registry v2 协议拉取 qwen3:0.6b 到 ollama 模型目录
# 用法: bash manual_pull.sh
set -e
MANIFEST=F:/reminder/ollama_local_llm/exercise/qwen3_0.6b_manifest.json
MODELS_DIR=~/.ollama/models
BLOBS=$MODELS_DIR/blobs
MAN_DIR=$MODELS_DIR/manifests/registry.ollama.ai/library/qwen3

# 清理上次失败留下的 partial 残片
rm -f "$BLOBS"/sha256-*-partial*

# 下载一个 blob 并用 sha256 校验，通过后改名到 blobs 目录
fetch_blob() {
  local digest=$1
  local hex=${digest#sha256:}
  local dest=$BLOBS/sha256-$hex
  if [ -f "$dest" ]; then echo "skip (exists): $hex"; return 0; fi
  local tmp=$dest.tmp
  curl -sL --max-time 3600 -o "$tmp" "https://registry.ollama.ai/v2/library/qwen3/blobs/$digest"
  local actual=$(sha256sum "$tmp" | cut -d' ' -f1)
  if [ "$actual" != "$hex" ]; then
    echo "HASH MISMATCH for $hex: got $actual"; rm -f "$tmp"; exit 1
  fi
  mv "$tmp" "$dest"
  echo "ok: $hex ($(stat -c%s "$dest") bytes)"
}

python -c "
import json
m = json.load(open(r'F:\reminder\ollama_local_llm\exercise\qwen3_0.6b_manifest.json'))
print(m['config']['digest'])
for l in m['layers']: print(l['digest'])
" | while read -r d; do fetch_blob "$d"; done

mkdir -p "$MAN_DIR"
cp "$MANIFEST" "$MAN_DIR/0.6b"
echo "DONE: manifest placed at $MAN_DIR/0.6b"
