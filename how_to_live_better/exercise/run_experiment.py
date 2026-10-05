#!/usr/bin/env python3
"""Read-only evidence tracing on pinned real HowToLiveBetter Markdown.

Only the explicitly supplied output directory is written. Upstream code is never
executed. An offline snapshot can reproduce the same checks without network.
"""
import argparse, hashlib, json, re, sys
from datetime import datetime, timezone
from pathlib import Path

PIN = 'bc149af3a02e721f0e3d03a673a0ec64fca765c4'
REPO = 'https://github.com/eternity4719/HowToLiveBetter'
REQUIRED = ['README.md', 'book/04-不要浪费时间.md', 'docs/核实记录/04-不要浪费时间.md']

def sha(b): return hashlib.sha256(b).hexdigest()
def stamp(): return datetime.now(timezone.utc).isoformat()
VISIBLE = 'all'
def emit(label, value):
    if VISIBLE != 'all' and not label.startswith(VISIBLE+' '): return
    print('\n## ' + label)
    print(json.dumps(value, ensure_ascii=False, indent=2))

def verify_bytes(data, expected):
    if sha(data) != expected:
        raise ValueError('SHA256_MISMATCH')

def parse_entries(text):
    lines = text.splitlines()
    starts = [(i, re.match(r'^### (\d+)\. (.+)$', x)) for i, x in enumerate(lines)]
    starts = [(i,m) for i,m in starts if m]
    result = {}
    for j,(i,m) in enumerate(starts):
        end = starts[j+1][0] if j+1<len(starts) else len(lines)
        fields, loc = {}, {}
        for k in range(i+1,end):
            f = re.match(r'^- ([^：]+)：(.*)',lines[k])
            if f:
                fields[f.group(1)] = f.group(2)
                loc[f.group(1)] = k+1
        result[int(m.group(1))] = {'id':int(m.group(1)), 'title':m.group(2),
          'start_line':i+1, 'end_line':end, 'fields':fields, 'field_lines':loc,
          'text':'\n'.join(lines[i:end])}
    return result

def trace(entry, record):
    if entry is None:
        return {'status':'UNKNOWN_ENTRY','number':None,'reason':'固定样本没有该条目；不补写'}
    urls = re.findall(r'https://doi\.org/([^>\s；]+)',entry['fields'].get('来源',''))
    lines = record.splitlines()
    refs = []
    for doi in urls:
        refs.append({'doi':doi,'url':'https://doi.org/'+doi,
            'record_lines':[i+1 for i,line in enumerate(lines) if doi in line],
            'external_read_this_experiment':False})
    return {'status':'TRACEABLE_REPOSITORY_CITATION' if refs else 'UNKNOWN_SOURCE',
            'sources':refs,'claim_verification':'NOT_INDEPENDENTLY_VERIFIED',
            'scope':'定位到仓库引用与核实记录；不等于重新核验论文结论'}

def numeric_answer(entry):
    note = entry['fields'].get('备注','') if entry else ''
    if not entry:
        return {'status':'UNKNOWN_ENTRY','value':None}
    if '具体百分比没核到原文' in note:
        return {'status':'ABSTAIN','value':None,'reason':'备注明确百分比未核到原文',
                'source_line':entry['field_lines']['备注']}
    return {'status':'ABSTAIN','value':None,'reason':'本实验没有定义可验证的个人效果数值'}

def main():
    global VISIBLE
    ap=argparse.ArgumentParser()
    ap.add_argument('--source-root',type=Path,default=Path('source'))
    ap.add_argument('--manifest',type=Path,default=Path('manifest.json'))
    ap.add_argument('--output-dir',type=Path,default=Path('results'))
    ap.add_argument('--show',choices=['all','1','2','3','4','5','6'],default='all')
    args=ap.parse_args()
    VISIBLE=args.show
    start=stamp()
    manifest=json.loads(args.manifest.read_text())
    if manifest['commit']!=PIN: raise ValueError('WRONG_COMMIT')
    bypath={x['path']:x for x in manifest['files']}
    before={}
    texts={}
    for path in REQUIRED:
        b=(args.source_root/path).read_bytes()
        verify_bytes(b,bypath[path]['sha256'])
        before[path]=sha(b)
        texts[path]=b.decode('utf-8')
    emit('1 固定真实输入',{'started_at_utc':start,'commit':PIN,'repository':REPO,
          'input_hashes':before,'python':sys.version,'writes':'only --output-dir',
          'executed_upstream_scripts':False,'network_used_by_this_script':False})
    entries=parse_entries(texts[REQUIRED[1]])
    readme=texts['README.md'].splitlines()
    entry_link_lines=[i+1 for i,s in enumerate(readme) if '(book/04-不要浪费时间.md)' in s]
    assert entry_link_lines, 'NO_README_ENTRY'
    for i in [3,6,7]:
        assert i in entries, 'MISSING_SAMPLE'
        assert set(['成本','说人话','收益','证据等级','来源','备注']) <= set(entries[i]['fields']), 'MISSING_FIELD'
    emit('2 从原始入口定位完整条目',{'readme_link_lines':entry_link_lines,
         'chapter_entries':len(entries),'sample':[{'id':entries[i]['id'],
         'title':entries[i]['title'],'lines':[entries[i]['start_line'],entries[i]['end_line']],
         'field_lines':entries[i]['field_lines']} for i in [3,6,7]]})
    chains={str(i):trace(entries[i],texts[REQUIRED[2]]) for i in [3,6,7]}
    assert sum(len(x['sources']) for x in chains.values()) == 6, 'EXPECTED_SIX_DOIS'
    assert all(len(x['sources']) == 2 for x in chains.values()), 'EXPECTED_TWO_DOIS_PER_SAMPLE'
    assert all(all(s['record_lines'] for s in x['sources']) for x in chains.values()), 'DOI_NOT_IN_RECORD'
    emit('3 追到来源字段与核实记录',chains)
    six=entries[6]
    assert six['fields']['证据等级']=='B', 'UNEXPECTED_REPOSITORY_GRADE'
    assert six['fields']['收益'].endswith('省下的时间，等于你砍掉的会议时长本身。'), 'ACCOUNTING_CLAIM_NOT_LOCATED'
    assert '作者自己的推论' in six['fields']['备注'], 'AUTHOR_MARKER_MISSING'
    separation={
      'repository_fact':{'text':'第4节第6条存在，证据等级标为 B，来源字段有两个 DOI。',
         'verification':'本次直接读取固定版本可验证'},
      'reported_empirical_claim':{'text':six['fields']['收益'].replace('省下的时间，等于你砍掉的会议时长本身。',''),
         'verification':'仓库转述研究，当前实验未独立验证原论文',
         'line':six['field_lines']['收益']},
      'author_accounting_assumption':{'text':'省下的时间，等于你砍掉的会议时长本身。', 'verification':'作者的时间账表述；不自动计入替代沟通耗时，不当作实测净收益', 'line':six['field_lines']['收益']},
      'author_judgment':{'text':'将会议改为文字异步沟通的建议',
         'explicit_label':six['fields']['备注'],
         'line':six['field_lines']['备注']},
      'reader_application':{'text':'是否适合某个团队、节省多少时间','status':'NOT_ESTABLISHED'}
    }
    assert separation['reported_empirical_claim']['verification'] != separation['repository_fact']['verification']
    assert separation['author_accounting_assumption']['text'] not in separation['reported_empirical_claim']['text']
    assert separation['author_accounting_assumption']['text'] in six['fields']['收益']
    emit('4 隔离事实断言和作者判断',separation)
    unknown=numeric_answer(entries[7])
    missing=trace(entries.get(999),texts[REQUIRED[2]])
    stripped={**six,'fields':{k:v for k,v in six['fields'].items() if k!='来源'}}
    missing_source=trace(stripped,texts[REQUIRED[2]])
    damaged=(args.source_root/REQUIRED[1]).read_bytes()+b'\nCONTROL_ONLY'
    try:
        verify_bytes(damaged,before[REQUIRED[1]])
        mutation_detected=False
    except ValueError as e:
        mutation_detected=str(e)=='SHA256_MISMATCH'
    assert unknown['status']=='ABSTAIN' and unknown['value'] is None
    assert missing['status']=='UNKNOWN_ENTRY'
    assert missing_source['status']=='UNKNOWN_SOURCE'
    assert mutation_detected
    # These two observations can coexist in one pinned revision. We flag an
    # unresolved provenance discrepancy; this is not proof the number is false.
    mismatch='4.11' in entries[3]['fields']['备注'] and any('4.11' in line and '**未确认**' in line for line in texts[REQUIRED[2]].splitlines())
    assert mismatch, 'EXPECTED_PROVENANCE_DISCREPANCY_NOT_FOUND'
    controls={'actual_entry_7_unknown_percentage':unknown,'absent_entry_999':missing,
       'removed_source_in_memory':missing_source,'appended_bytes_mutation_detected':mutation_detected,
       'cross_file_discrepancy':{'entry':3,'current_number':'4.11',
         'record_note':'旧核实记录写具体场次未确认且未写数字；当前正文已出现该数值',
         'status':'UNRESOLVED_PROVENANCE_GAP','number_correctness':'NOT_DECIDED'},
       'control_scope':'主样本都是真实文件；删来源和改字节仅为内存中的负向对照'}
    emit('5 未知弃权与失败对照',controls)
    after={p:sha((args.source_root/p).read_bytes()) for p in REQUIRED}
    assert before==after,'SOURCE_MUTATED'
    checks=['fixed_commit_and_sha256','readme_to_real_entry','six_fields_present',
      'six_dois_present_in_record','author_judgment_not_promoted_to_fact',
      'unknown_percentage_abstention','absent_entry_abstention','missing_source_abstention',
      'tampered_bytes_rejected','provenance_gap_exposed','source_unchanged']
    summary={'started_at_utc':start,'ended_at_utc':stamp(),'commit':PIN,
       'checks_passed':checks,'checks_count':len(checks),'scope':'repository traceability only',
       'source_unchanged':True,'new_medical_legal_financial_conclusions':False,
       'external_papers_read_by_script':False,
       'release_claim':'实验通过不表示仓库全部结论、外部论文或个人适用性通过'}
    emit('6 只读不变性与结论',summary)
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/'experiment_result.json').write_text(json.dumps({
       'summary':summary,'inputs':before,'entry_links':entry_link_lines,
       'entries':{str(i):entries[i] for i in [3,6,7]},'chains':chains,
       'separation':separation,'controls':controls},ensure_ascii=False,indent=2))
    return 0

if __name__=='__main__':
    try: sys.exit(main())
    except Exception as e:
        print('EXPERIMENT_FAILED: '+type(e).__name__+': '+str(e),file=sys.stderr)
        sys.exit(1)
