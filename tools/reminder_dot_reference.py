"""Build cloud references from the already-published knowledge Git snapshot only.

No network calls, working-tree note reads, full-vault copy, or learning queue writes.
The caller verifies the current public main SHA first; it must equal origin/main.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
from urllib.parse import quote

REPOSITORY = 'Smashwinny/reminder_knowlege'
SKILL_PATH = '.claude/skills/learn-project/SKILL.md'
NOTE_PREFIXES = ('vault/概念/', 'vault/项目笔记/')


def git(root, *arguments):
    result = subprocess.run(['git', '-C', str(root), *arguments],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise ValueError('Git snapshot read failed; no files published.')
    return result.stdout


def raw_url(commit, path):
    return f'https://raw.githubusercontent.com/{REPOSITORY}/{commit}/{quote(path, safe="/")}'


def build(root, commit):
    if not re.fullmatch(r'[0-9a-f]{40}', commit):
        raise ValueError('Supply a full public main commit SHA.')
    remote = git(root, 'remote', 'get-url', 'origin').decode().strip()
    if remote not in (f'https://github.com/{REPOSITORY}.git',
                      f'https://github.com/{REPOSITORY}',
                      f'git@github.com:{REPOSITORY}.git'):
        raise ValueError('Origin is not the explicitly allowed knowledge repository.')
    published = git(root, 'rev-parse', '--verify', 'refs/remotes/origin/main^{commit}').decode().strip()
    if published != commit:
        raise ValueError('Supplied SHA is not origin/main; fetch/verify public main first.')
    paths = git(root, 'ls-tree', '-r', '-z', '--name-only', commit, '--', 'vault').decode('utf-8').split('\0')
    notes = []
    for item in sorted(paths):
        if not item.endswith('.md') or not item.startswith(NOTE_PREFIXES):
            continue
        parsed = PurePosixPath(item)
        if '..' in parsed.parts or len(parsed.parts) != 3:
            continue
        body = git(root, 'show', f'{commit}:{item}')
        notes.append({'path': item, 'title': parsed.stem,
                      'category': 'concept' if item.startswith(NOTE_PREFIXES[0]) else 'project',
                      'url': raw_url(commit, item), 'bytes': len(body),
                      'sha256': hashlib.sha256(body).hexdigest()})
    skill = git(root, 'show', f'{commit}:{SKILL_PATH}')
    snapshot = {'schema': 'reminder-dot-public-reference-v1',
                'repository': REPOSITORY, 'sourceCommit': commit,
                'sourceRef': 'origin/main', 'publishedSnapshotOnly': True,
                'workingTreeIncluded': False, 'privateRecordsIncluded': False,
                'knowledgeScope': list(NOTE_PREFIXES),
                'skill': {'path': SKILL_PATH, 'url': raw_url(commit, SKILL_PATH),
                          'sha256': hashlib.sha256(skill).hexdigest(), 'bytes': len(skill)},
                'notes': notes}
    lines = ['# 已发布学习知识的只读索引', '',
             f'来源：`{REPOSITORY}`，固定版本 `{commit}`。', '',
             '这是已发布版本的参考索引，不是当前本机 vault 的完整视图。'
             '未提交笔记、总览、私密原记录、浏览器配置与运行队列未纳入。', '',
             '按主题读取相关链接并记录实际读取的版本；链接打不开则明确待核对，不能声称已读。', '']
    for category, heading in [('concept', '概念'), ('project', '项目笔记')]:
        lines += [f'## {heading}', '']
        for entry in notes:
            if entry['category'] == category:
                label = entry['title'].replace('[', '\\[').replace(']', '\\]')
                lines.append(f'- [{label}]({entry["url"]})')
        lines.append('')
    return snapshot, '\n'.join(lines), skill


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--source-commit', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        snapshot, markdown, _ = build(args.root, args.source_commit)
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output / 'knowledge-index.json').write_text(
            json.dumps(snapshot, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (args.output / 'knowledge-index.md').write_text(markdown, encoding='utf-8')
        print(json.dumps({'sourceCommit': snapshot['sourceCommit'],
                          'concepts': sum(x['category'] == 'concept' for x in snapshot['notes']),
                          'projects': sum(x['category'] == 'project' for x in snapshot['notes']),
                          'privateRecordsIncluded': False, 'workingTreeIncluded': False}, ensure_ascii=False))
    except (ValueError, OSError, UnicodeError) as error:
        parser.exit(2, f'Error: {error}\n')


if __name__ == '__main__':
    main()
