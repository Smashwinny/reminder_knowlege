"""Assemble only explicitly allowed, credential-free explanatory files."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'output/pdf'
SRC = OUT / 'source'
PACK = OUT / 'companion'
PACK.mkdir(exist_ok=True)

def write(relative, content):
    destination = PACK / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding='utf-8')
    return destination

def copy(source, relative):
    destination = PACK / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)

copy(SRC/'companion_readme.md', 'README.md')
copy(SRC/'setup_commands.md', '逐终端补充命令.md')
copy(OUT/'workflow_guide.html', 'workflow_guide.html')
copy(OUT/'拾遗到知识网络-架构与搭建指南.md', '拾遗到知识网络-架构与搭建指南.md')
for filename in ('build_workflow_guide.py','verify_workflow_guide.py'):
    copy(SRC/filename, '讲解源码/'+filename)
copy(SRC/'document_qa.json', '讲解源码/document_qa.json')
copy(SRC/'layout_qa.json', '讲解源码/layout_qa.json')
for i in range(1,37):
    copy(SRC/'diagrams'/f'page_{i:02}.svg', 'diagrams/'+f'page_{i:02}.svg')

files = [
    'AGENTS.md', 'CLAUDE.md', '.claude/skills/learn-project/SKILL.md',
    'tools/reminder_pipeline.py', 'tools/reminder_coordinator.py', 'tools/reminder_history.py',
    'tools/shiyi_sync.py', 'tools/shiyi_worker_guide.md',
    'tools/reminder_workflow_policy.json', 'tools/reminder_dot_http.py',
    'tools/reminder_dot_backup.py', 'tools/reminder_dot_agent.py', 'tools/reminder_dot_reference.py',
    'tools/reminder_dot_on_login.ps1', 'tools/reminder_dot_backup_job.ps1',
    'tools/install_reminder_dot_backup_trigger.ps1',
    'tools/test_reminder_pipeline.py', 'tools/test_reminder_coordinator.py',
    'tools/test_reminder_dot_backup.py', 'tools/test_reminder_dot_agent.py',
    'reminder-dot/dot-backup-config.example.json', 'reminder-dot/cloud-reference/RUNNING_IN_DOT.md'
]
for filename in files:
    copy(ROOT/filename, '本机工具补齐/'+filename)
copy(SRC/'private_login_example.py', '本机工具补齐/tools/private_login_example.py')
files.append('tools/private_login_example.py')
write('本机工具补齐/tools/reminder_workflow.md', '''# 分发版工作流摘要

本文件是教学包的流程摘要，替代本机工作区含历史状态的长工作流；不是历史日志的原件复制。规则来自当前 AGENTS、worker 指南和 RUNNING_IN_DOT。

本人 Dot 在云端执行；网站正式保存原记录、分类和完整学习报告。本机登录只复制并校验六类原件。唯一协调者核对当前来源、允许范围与 owner，按 start / ready / 真实独立 review / confirm-analysis 收尾，合并 vault，再只提交明确学习文件并回读远端 SHA。

初步分类包含真实来源、理由、知识关联与下一步；learning 可在本人授权范围内继续完整学习。原文不可读时明确证据不足，不能冒充非学习或强行关联搜索命中。每份报告有独立 owner，服务端租约和本机 SQLite 不互相替代，过期 owner 不自动抢占。所有学习文件由真实实验与逐页 PDF 及独立审核验收。

分析标签不修改用户任务 state。任务完成由本人点击；新流程禁止旧 done/viewed/publish。网站保存、本机校验、知识入库、Git commit 与 push 分阶段记账，电脑离线或失败保留待同步。云端只读取实际获得的固定知识索引与获准报告；F: 不是云端路径。

共享 vault、纲要和 Git 只由唯一协调者修改。先检查暂存区；归属不明即停；只 add 明确文件，不强推、不跳 hooks、不 reset/rebase 正被其他执行者使用的工作区。公开知识仓库只接收审核过的学习成果，私密原记录、分类与运行数据库不提交。

具体新手命令见教学包《逐终端补充命令》，云端方法见 RUNNING_IN_DOT，质量要求见原 learn-project。原方法中让 worker 全仓 add 或共享工作区 rebase 的动作由当前 AGENTS 覆盖。
''')
files.append('tools/reminder_workflow.md')
write('本机工具补齐/install-files.json', json.dumps(files, ensure_ascii=False, indent=2)+'\n')
copy(SRC/'toolpack_readme.md', '本机工具补齐/README.md')

copy(ROOT/'reminder-dot/cloud-reference/RUNNING_IN_DOT.md', '云端方法/RUNNING_IN_DOT.md')
published='109ffa9763c24f6ff05d2b7f1b1d9ed14e7d79e0'
result = subprocess.run([
    __import__('sys').executable, str(ROOT/'tools/reminder_dot_reference.py'),
    '--root', str(ROOT/'完成/.pipeline/knowledge-publication'),
    '--source-commit', published, '--output', str(PACK/'云端方法')
], capture_output=True, text=True, encoding='utf-8')
if result.returncode:
    raise RuntimeError('Public-only reference generation failed. No archive generated.')
reference=json.loads((PACK/'云端方法/knowledge-index.json').read_text(encoding='utf-8'))
assert reference['sourceCommit']==published and reference['privateRecordsIncluded'] is False
fixed_skill = subprocess.check_output(['git','-C',str(ROOT/'完成/.pipeline/knowledge-publication'),
    'show',published+':'+reference['skill']['path']])
assert hashlib.sha256(fixed_skill).hexdigest()==reference['skill']['sha256']
(PACK/'云端方法/原learn-project-SKILL.md').write_bytes(fixed_skill)
assert hashlib.sha256((PACK/'云端方法/原learn-project-SKILL.md').read_bytes()).hexdigest()==reference['skill']['sha256']

write('模板/概念笔记.md', '''---
aliases: [概念别名]
tags: [concept]
---
# 概念名

## 一句话定义
用自己的话填写，不直接复制 AI 摘要。

## 工作机制
输入 → 核心步骤 → 输出；为什么适用？

## 证据与实验
- 已实际读取的作者或官方文档：[标题](https://AUTHOR_OR_OFFICIAL_SOURCE)
- 固定版本 / 实际命令 / 观察结果 / 边界。

## 关联
- 前提：[[已有概念]]，说明为什么依赖它。
- 比较：[[相近概念]]，说明差异及何时选择。
- 应用：[[项目笔记]]，说明此次如何用到它。

## 闭卷问题
1. 定义是什么，解决哪类问题？
2. 一个不适用的反例？
3. 换一个场景如何验证？

首次写入前查重；把占位链接替换为真实笔记。关联边需要理由，图谱节点数量不代表掌握程度。
''')
write('模板/项目笔记.md', '''# 项目名

## 为什么学习
真实目标、已核实原项目与版本。

## 资料与证据
- [彩色指南](https://github.com/YOUR_REPOSITORY/blob/COMMIT/PROJECT/guide.pdf)
- [真实实验日志](https://github.com/YOUR_REPOSITORY/blob/COMMIT/PROJECT/experiment_log.txt)
- 作者 / 官方仓库与固定版本。

## 已经能够做什么
写实际验证过的用途、操作和限制。

## 核心概念
[[概念A]] → [[概念B]]；解释两者的关系。

## 我仍没懂的地方
待检验疑问、环境与下一步。

## 复习入口
[[复习/实际日期]]；本人回答、错因与迁移实验。

先替换占位 URL / 笔记名，不把私人任务链接发布到公开仓库。
''')
write('模板/每日复习.md', '''# 每日复习 · YYYY-MM-DD

状态：建议草稿，待本人确认。
来源：已发布知识固定 commit；实际读取笔记。

| 概念 | 问题 | 本人原回答 | 证据与错因 | 评分建议0/1/2 | 本人确认 | 下次日期 |
| --- | --- | --- | --- | --- | --- | --- |
| [[概念名]] | 定义、机制、反例或迁移？ | 先闭卷填写 | 回链原笔记 / 实验 | 待填写 | 待确认 | 待确定 |

## 今日迁移练习
改变一个输入或场景；记录命令、预期和真实结果。

## 下次重点
本人答错或没能动手的内容。1/3/7/14/30 天只是可调示例，不是已部署算法。

公开知识仓库只保存本人确认可以公开的笔记；个人答题原文或私密评分默认保留私有草稿 / 本机排除目录，不能整目录默认推送。
''')
manifest=dict(topic='真实项目主题',project_dir='PROJECT',pdf='PROJECT/guide.pdf',
    html='PROJECT/guide.html',exercise_dir='PROJECT/exercise',
    experiment_log='PROJECT/experiment_log.txt',vault_note='vault/项目笔记/PROJECT.md',
    source_urls=['https://AUTHOR_OR_OFFICIAL_SOURCE'])
write('模板/manifest.example.json', json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
receipt=dict(schema='reminder-analysis-confirmation-v1',accountId='ACCOUNT_UUID',listId='LIST_UUID',
    taskId='TASK_UUID',reportId='REPORT_UUID',sourceHash='真实当前sourceHash',
    backupBundle='完成/.pipeline/dot/ACCOUNT_UUID/LIST_UUID/exports/BACKUP_SHA256.json',
    backupSha256='BACKUP_SHA256',handoff='完成/.pipeline/dot/ACCOUNT_UUID/LIST_UUID/handoff.json')
write('模板/receipt.example.json', json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
write('模板/使用边界.md', '这些是格式样例，不能作为验收证据。manifest 的每份产物须真实存在并已审；receipt 的值须来自同账户 / 列表 / 当前来源的真实网站 full 报告与本机校验备份。审核后改产物需重新 ready / review。个人复习回答与评分是否公开由本人明确选择。\n')

# All members must remain inside the package and exclude private runtime paths.
members=sorted(p for p in PACK.rglob('*') if p.is_file() and p.name!='package_manifest.json')
for p in members:
    rel=p.relative_to(PACK).as_posix()
    if any(v in rel for v in ('.shiyi_token','.env','.pipeline','__pycache__','/repo/','.git/')):
        raise RuntimeError('Forbidden distribution member.')
    assert p.resolve().is_relative_to(PACK.resolve())
records=[{'path':p.relative_to(PACK).as_posix(),'bytes':p.stat().st_size,
          'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in members]
write('package_manifest.json',json.dumps({'schema':'reminder-guide-package-v1',
    'privateRuntimeIncluded':False,'publicReferenceCommit':published,'files':records},ensure_ascii=False,indent=2)+'\n')
archive=OUT/'可编辑讲解与命令包.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(PACK.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(PACK).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(set(z.namelist()))
    stored=json.loads(z.read('package_manifest.json'))
    for item in stored['files']:
        assert hashlib.sha256(z.read(item['path'])).hexdigest()==item['sha256']
print(json.dumps({'archive':str(archive),'members':len(records)+1,
    'bytes':archive.stat().st_size,'privateRuntimeIncluded':False,
    'publicNotes':len(reference['notes'])},ensure_ascii=False))
