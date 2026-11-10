# 真实实验日志

执行时间：2026-11-11 01:34:55（北京时间 UTC+8）。范围：本目录 exercise/sandbox，全为本次生成的合成文件。

五个 demo 命令均真实退出0；步骤2备份函数返回23是预期安全阻断，demo断言后返回0。未调用任何模型、用户凭证、网络Git远端、提醒或真实配置。

```text
===== 2026-11-11T01:34:55+08:00 python3 exercise/ma-laoshi-20261111-demo.py 1 =====
STEP 1
$ git init --bare --initial-branch=main /workspace/ma-laoshi-20261111/ma-laoshi-20261111-item-7-bot-config-github-backup/exercise/sandbox/remote.git
Initialized empty Git repository in /workspace/ma-laoshi-20261111/ma-laoshi-20261111-item-7-bot-config-github-backup/exercise/sandbox/remote.git/
SEEDED 10 synthetic regular files + 1 symlink; remote empty
===== 2026-11-11T01:34:55+08:00 python3 exercise/ma-laoshi-20261111-demo.py 2 =====
STEP 2
BLOCKED before add/commit/push; paths only: notes/planted.md
PASS: rc=23; no staging repository, commit, or remote ref
===== 2026-11-11T01:34:55+08:00 python3 exercise/ma-laoshi-20261111-demo.py 3 =====
STEP 3
SCAN PASS; selected files=4 bytes=452
$ git init -b main /workspace/ma-laoshi-20261111/ma-laoshi-20261111-item-7-bot-config-github-backup/exercise/sandbox/snapshot
Initialized empty Git repository in /workspace/ma-laoshi-20261111/ma-laoshi-20261111-item-7-bot-config-github-backup/exercise/sandbox/snapshot/.git/
$ git config user.name Synthetic Backup Lab
$ git config user.email sandbox@example.invalid
$ git rev-list --all --objects
$ git add --all
$ git commit -m Synthetic approved snapshot
[main (root-commit) 9d79e83] Synthetic approved snapshot
 5 files changed, 16 insertions(+)
 create mode 100644 MANIFEST.json
 create mode 100644 config/settings.json
 create mode 100644 docs/RESTORE.md
 create mode 100644 notes/study.md
 create mode 100644 skills/writing.md
$ git push /workspace/ma-laoshi-20261111/ma-laoshi-20261111-item-7-bot-config-github-backup/exercise/sandbox/remote.git HEAD:refs/heads/main
To /workspace/ma-laoshi-20261111/ma-laoshi-20261111-item-7-bot-config-github-backup/exercise/sandbox/remote.git
 * [new branch]      HEAD -> main
$ git ls-tree --name-only -r main
MANIFEST.json
config/settings.json
docs/RESTORE.md
notes/study.md
skills/writing.md
PASS: remote has exactly 5 approved files; symlink/excluded paths absent
===== 2026-11-11T01:34:55+08:00 python3 exercise/ma-laoshi-20261111-demo.py 4 =====
STEP 4
$ git rev-parse main
9d79e835a8e3e03c90bc1ef7e8eb80299722b44e
SCAN PASS; selected files=4 bytes=452
$ git rev-list --all --objects
9d79e835a8e3e03c90bc1ef7e8eb80299722b44e
45e9f40de651b7399269c0e8b0d3bea7797021b2 
fbac47c52e1d34e7ec9f4ad2f13244f87622491d MANIFEST.json
613d00a40fe6c2e34fbcfc366170862579df1a81 config
7d21d8ad20321829a8eb21e14fa520226096ff21 config/settings.json
991ce977abad423759d991c815ded73f4ae61299 docs
9607165b1fc243c40dfb243e0b6444bf46fcce21 docs/RESTORE.md
b5541bc2c4fa53171748c6f38ce8ee947217bddf notes
7983e15063a81faf1927ecd9b521a7b3bab58987 notes/study.md
7abf5154108e6a7912db2b9785fd8c385734f7f8 skills
c69faa5dbb532305821fb25bd1519552942630b6 skills/writing.md
$ git cat-file -t 9d79e835a8e3e03c90bc1ef7e8eb80299722b44e
commit
$ git cat-file -t 45e9f40de651b7399269c0e8b0d3bea7797021b2
tree
$ git cat-file -t fbac47c52e1d34e7ec9f4ad2f13244f87622491d
blob
$ git cat-file -t 613d00a40fe6c2e34fbcfc366170862579df1a81
tree
$ git cat-file -t 7d21d8ad20321829a8eb21e14fa520226096ff21
blob
$ git cat-file -t 991ce977abad423759d991c815ded73f4ae61299
tree
$ git cat-file -t 9607165b1fc243c40dfb243e0b6444bf46fcce21
blob
$ git cat-file -t b5541bc2c4fa53171748c6f38ce8ee947217bddf
tree
$ git cat-file -t 7983e15063a81faf1927ecd9b521a7b3bab58987
blob
$ git cat-file -t 7abf5154108e6a7912db2b9785fd8c385734f7f8
tree
$ git cat-file -t c69faa5dbb532305821fb25bd1519552942630b6
blob
$ git add --all
NO CHANGE: no new commit
$ git push /workspace/ma-laoshi-20261111/ma-laoshi-20261111-item-7-bot-config-github-backup/exercise/sandbox/remote.git HEAD:refs/heads/main
Everything up-to-date
$ git rev-parse main
9d79e835a8e3e03c90bc1ef7e8eb80299722b44e
PASS: idempotent commit; 5/5 synthetic secret-pattern positive controls
===== 2026-11-11T01:34:55+08:00 python3 exercise/ma-laoshi-20261111-demo.py 5 =====
STEP 5
$ git clone --branch main /workspace/ma-laoshi-20261111/ma-laoshi-20261111-item-7-bot-config-github-backup/exercise/sandbox/remote.git /workspace/ma-laoshi-20261111/ma-laoshi-20261111-item-7-bot-config-github-backup/exercise/sandbox/restore-preview
Cloning into '/workspace/ma-laoshi-20261111/ma-laoshi-20261111-item-7-bot-config-github-backup/exercise/sandbox/restore-preview'...
done.
HASH MATCH config/settings.json
HASH MATCH docs/RESTORE.md
HASH MATCH notes/study.md
HASH MATCH skills/writing.md
PASS: dry-run restore 4/4 file hashes; no real configuration overwritten
```

研究读取失败：X WebFetch 403（之后已有X公开工具完整正文）；GitHub releases/tag/v2.47.3 404（以官方tag peeled SHA和raw文档固定源码，不据此推断版本不存在）。

前一轮仅收到协调者“被平台rate limiting停止”的转述，本worker未收到可记录的额度耗尽精确工具原文；不伪造该提示。

环境 Git 2.47.3 / Python 3.13.5。复跑须解压至新目录，demo 1 对现有 sandbox 会拒绝覆盖。

## PDF产物
实际打印为8页A4；pdftoppm转PNG并逐页Read检查，见 ma-laoshi-20261111-pdf-check.md。无空白页、截断或SVG缺失。
