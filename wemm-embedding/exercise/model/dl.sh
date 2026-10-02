#!/bin/bash
URL="https://hf-mirror.com/tencent/WeMM-Embedding-2B/resolve/main/model.safetensors"
SIZE=5441695216
N=16
CHUNK=$(( SIZE / N + 1 ))
expected() { local i=$1; local s=$((i * CHUNK)); local e=$(( (i+1) * CHUNK - 1 )); [ $e -ge $SIZE ] && e=$((SIZE-1)); echo $((e - s + 1)); }
for round in 1 2 3 4 5 6 7 8; do
  pids=()
  for i in $(seq 0 $((N-1))); do
    f="part_$i"; want=$(expected $i); have=0
    [ -f "$f" ] && have=$(stat -c %s "$f")
    if [ "$have" -ne "$want" ]; then
      s=$((i * CHUNK)); e=$(( (i+1) * CHUNK - 1 )); [ $e -ge $SIZE ] && e=$((SIZE-1))
      curl -sL --retry 5 --retry-delay 2 -r "$s-$e" -o "$f" "$URL" &
      pids+=($!)
    fi
  done
  [ ${#pids[@]} -eq 0 ] && break
  wait "${pids[@]}"
  ok=1
  for i in $(seq 0 $((N-1))); do want=$(expected $i); have=$(stat -c %s "part_$i" 2>/dev/null || echo 0); [ "$have" -ne "$want" ] && ok=0; done
  [ $ok -eq 1 ] && break
  echo "round $round incomplete, retrying..."
done
ok=1
for i in $(seq 0 $((N-1))); do want=$(expected $i); have=$(stat -c %s "part_$i" 2>/dev/null || echo 0); [ "$have" -ne "$want" ] && { echo "part_$i BAD: $have != $want"; ok=0; }; done
[ $ok -eq 1 ] && cat $(for i in $(seq 0 $((N-1))); do echo part_$i; done) > model.safetensors && rm -f part_* && echo "MERGE_OK $(stat -c %s model.safetensors)"
