"""本地智能体经原队列和网站共享领取锁写分析标签，永不勾选任务完成。"""
import argparse
import base64
import contextlib
import io
import json
from pathlib import Path
import urllib.error
import urllib.request
import zipfile

from reminder_pipeline import ROOT, Pipeline, PipelineError, IGNORED_EXERCISE_DIRS
from reminder_dot_backup import SITE, MAX_BUNDLE_BYTES


def post(list_id, name, arguments):
    from shiyi_sync import get_token
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *args): return None
    request = urllib.request.Request(SITE + '/api/dot/agent', data=json.dumps({'listId': list_id, 'tool': name, 'arguments': arguments}, ensure_ascii=False).encode('utf-8'), headers={'Authorization': 'Bearer ' + get_token(), 'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.build_opener(NoRedirect).open(request, timeout=45) as response:
            data = response.read(MAX_BUNDLE_BYTES + 1)
        if len(data) > MAX_BUNDLE_BYTES: raise PipelineError('网站响应过大，未读取截断内容。')
        return json.loads(data)
    except urllib.error.HTTPError as error:
        raise PipelineError(f'网站标签接口拒绝操作 HTTP {error.code}；原任务状态未修改。') from None
    except (OSError, ValueError):
        raise PipelineError('网站标签接口不可用；未把本地缓存当本次网站结果。') from None


def owned(pipeline, task_id, owner):
    record = pipeline.status(task_id)
    if record['owner'] != owner or record['unresolved_publication']:
        raise PipelineError('先通过原 reminder_pipeline 领取；不能使用其他 owner 或未决发布。')
    return record


def attach_reviewed_artifacts(pipeline, record, analysis):
    """Actual files come from the reviewed manifest, not caller-provided base64."""
    review = record['quality_review']
    if not record['learning_started'] or not record['manifest'] or not review or not review.get('approved') or review['reviewer'] == record['owner']:
        raise PipelineError('须先 start、ready 和实际独立 review；标签不能绕过学习验收。')
    with contextlib.closing(pipeline._connection()) as connection:
        row = dict(connection.execute('SELECT * FROM tasks WHERE task_id=?', (record['task_id'],)).fetchone())
    manifest, fingerprint = pipeline._validate_manifest(row, record['manifest'])
    if fingerprint != record['artifact_fingerprint'] or fingerprint != review['artifact_fingerprint']:
        raise PipelineError('审核后产物已变化，须重新 ready 和 review。')
    completion = dict(analysis.get('completion', {}))
    completion.update(project=manifest['project_dir'], reviewer=review['reviewer'], reviewNotes=review['notes'], pdfRendered=True, experimentChecked=True, knowledgeChecked=True)
    data = {role: pipeline._path(manifest[key]).read_bytes() for role, key in [('guide_pdf','pdf'), ('guide_html','html'), ('experiment_log','experiment_log'), ('knowledge_notes','vault_note')]}
    data['review_log'] = json.dumps(review, ensure_ascii=False, indent=2).encode('utf-8')
    exercise = pipeline._path(manifest['exercise_dir'], is_dir=True)
    files = [pipeline._path(name) for name in manifest.get('experiment_files', [])] or [file for file in exercise.rglob('*') if file.is_file() and not any(part.casefold() in IGNORED_EXERCISE_DIRS for part in file.relative_to(exercise).parts)]
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as stream:
        for file in sorted(files):
            checked = pipeline._path(file.relative_to(pipeline.root).as_posix())
            info = zipfile.ZipInfo(checked.relative_to(exercise).as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            stream.writestr(info, checked.read_bytes())
    data['exercise_archive'] = archive.getvalue()
    if sum(len(value) for value in data.values()) > 1000000:
        raise PipelineError('实际产物合计超过网站 1 MB 上限；保留待同步，不能只交文件路径冒充完整产物。')
    completion['artifacts'] = [{'role': role, 'base64': base64.b64encode(value).decode('ascii')} for role, value in data.items()]
    return {**analysis, 'completion': completion}


def hide_blobs(value):
    if isinstance(value, dict): return {k: hide_blobs(v) for k,v in value.items() if k != 'base64'}
    if isinstance(value, list): return [hide_blobs(v) for v in value]
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['list-pending','list-learning','read','claim','renew','release','save','block'])
    parser.add_argument('--account-id', required=True)
    parser.add_argument('--list-id', required=True)
    parser.add_argument('--task')
    parser.add_argument('--owner')
    parser.add_argument('--lease-id')
    parser.add_argument('--stage', choices=['preliminary','full'], default='preliminary')
    parser.add_argument('--report-id', help='完整学习领取必须绑定当前初步报告')
    parser.add_argument('--analysis', type=Path, help='结构化分析 JSON；完整阶段还需实际实验元数据')
    parser.add_argument('--reason', help='block 的实际阻碍')
    parser.add_argument('--coordinator', help='完整标签保存由既有全局协调者负责')
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        identity = post(args.list_id, 'reminder_identity', {})
        if identity.get('accountId') != args.account_id or identity.get('listId') != args.list_id:
            raise PipelineError('当前凭据对应账户/列表不符，停止操作。')
        name = {'list-pending':'reminder_list_pending','list-learning':'reminder_list_learning','read':'reminder_read_record','claim':'reminder_claim','renew':'reminder_renew','release':'reminder_release','save':'reminder_save_analysis','block':'reminder_record_blocker'}[args.operation]
        payload = {}
        if args.operation not in ['list-pending','list-learning']:
            if not args.task: parser.error('此操作需要 --task')
            payload['taskId'] = args.task
        if args.operation in ['claim','renew','release','save','block']:
            if not args.owner: parser.error('写入需要 --owner')
            payload.update(owner=args.owner, leaseId=args.lease_id)
            if args.operation != 'release':
                pipeline = Pipeline(root=args.root)
                record = owned(pipeline, args.task, args.owner)
                payload['sourceHash'] = record['source_hash']
            if args.operation == 'claim': payload.update(stage=args.stage, reportId=args.report_id)
            if args.operation == 'block':
                if not args.reason: parser.error('block 需要 --reason')
                payload['reason'] = args.reason
            if args.operation == 'save':
                if not args.analysis: parser.error('save 需要 --analysis')
                analysis = json.loads(args.analysis.read_text(encoding='utf-8-sig'))
                analysis['stage'] = args.stage
                if args.stage == 'full':
                    from reminder_coordinator import require_owner
                    require_owner(args.root, args.coordinator or '')
                    analysis = attach_reviewed_artifacts(pipeline, record, analysis)
                payload['analysis'] = analysis
        result = post(args.list_id, name, payload)
        print(json.dumps(hide_blobs(result), ensure_ascii=False))
    except (PipelineError, OSError, ValueError, RuntimeError) as error:
        parser.exit(2, '错误：' + str(error) + '\n')


if __name__ == '__main__': main()
