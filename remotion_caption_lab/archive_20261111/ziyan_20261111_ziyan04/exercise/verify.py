"""Verify the real MP4 with ffprobe, or a bounded stdlib ISO-BMFF check.

The fallback reads container metadata only; it does not decode frames or prove
visual continuity. No mocks and no self-issued independent review.
"""
from pathlib import Path
import json, shutil, struct, subprocess, sys

TARGET = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'caption-lab-replay.mp4'

def ffprobe_checks(path):
    raw = subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)])
    x = json.loads(raw)
    v = [s for s in x['streams'] if s['codec_type'] == 'video']
    a = [s for s in x['streams'] if s['codec_type'] == 'audio']
    observed = {'streams': len(x['streams']), 'video': len(v), 'audio': len(a)}
    checks = {'one_video': len(v) == 1, 'no_audio': not a}
    if v:
        observed.update(codec=v[0].get('codec_name'), width=v[0].get('width'), height=v[0].get('height'), fps=v[0].get('r_frame_rate'), seconds=float(x['format']['duration']), frames=v[0].get('nb_frames'))
        checks.update(h264=v[0].get('codec_name') == 'h264', **{'1080p': (v[0]['width'], v[0]['height']) == (1920, 1080), '30fps': v[0]['r_frame_rate'] == '30/1', '12s': float(x['format']['duration']) == 12.0, '360frames': v[0].get('nb_frames') == '360'})
    return observed, checks

def container_checks(path):
    data = path.read_bytes()
    def atoms(start, end):
        while start + 8 <= end:
            size, typ = struct.unpack_from('>I4s', data, start); head = 8
            if size == 1:
                if start + 16 > end: raise ValueError('truncated extended box')
                size = struct.unpack_from('>Q', data, start + 8)[0]; head = 16
            if size == 0: size = end - start
            if size < head or start + size > end: raise ValueError('invalid MP4 box size')
            yield typ.decode('latin1'), start + head, start + size
            start += size
        if start != end: raise ValueError('trailing partial MP4 box')
    def child(box, name):
        return next((x for x in atoms(box[1], box[2]) if x[0] == name), None)
    moov = next((x for x in atoms(0, len(data)) if x[0] == 'moov'), None)
    if moov is None: raise ValueError('missing moov box')
    tracks = []
    for box in atoms(moov[1], moov[2]):
        if box[0] != 'trak': continue
        mdia = child(box, 'mdia'); hdlr = child(mdia, 'hdlr'); mdhd = child(mdia, 'mdhd')
        if not mdia or not hdlr or not mdhd: raise ValueError('incomplete track')
        p = mdhd[1]
        if data[p] == 0: timescale, duration = struct.unpack_from('>II', data, p + 12)
        elif data[p] == 1: timescale, duration = struct.unpack_from('>IQ', data, p + 20)
        else: raise ValueError('unsupported mdhd version')
        if not timescale: raise ValueError('zero timescale')
        kind = data[hdlr[1] + 8:hdlr[1] + 12].decode('ascii')
        stbl = child(child(mdia, 'minf'), 'stbl')
        stsd = child(stbl, 'stsd'); stsz = child(stbl, 'stsz')
        sample = next(atoms(stsd[1] + 8, stsd[2]))
        count = struct.unpack_from('>I', data, stsz[1] + 8)[0]
        track = {'type': kind, 'codec': sample[0], 'timescale': timescale, 'seconds': duration / timescale, 'samples': count}
        if kind == 'vide':
            track['width'], track['height'] = struct.unpack_from('>HH', data, sample[1] + 24)
            track['fps'] = count / track['seconds']
        tracks.append(track)
    videos = [t for t in tracks if t['type'] == 'vide']; audio = [t for t in tracks if t['type'] == 'soun']
    observed = {'tracks': tracks, 'bytes': len(data)}
    checks = {'one_video': len(videos) == 1, 'no_audio': not audio}
    if videos:
        v = videos[0]
        checks.update(h264=v['codec'] == 'avc1', **{'1080p': (v.get('width'), v.get('height')) == (1920, 1080), '30fps': abs(v.get('fps', 0) - 30) < 1e-9, '12s': v['seconds'] == 12.0, '360frames': v['samples'] == 360})
    return observed, checks

if not TARGET.is_file(): raise SystemExit(f'missing video: {TARGET}')
mode = 'ffprobe' if shutil.which('ffprobe') else 'stdlib ISO-BMFF container (no decode)'
observed, checks = ffprobe_checks(TARGET) if mode == 'ffprobe' else container_checks(TARGET)
print('probe_mode:', mode)
print('target:', TARGET)
print('observed:', json.dumps(observed, ensure_ascii=False, sort_keys=True))
for name, value in checks.items(): print(name, 'PASS' if value else 'FAIL')
print('scope:', 'decoded stream metadata' if mode == 'ffprobe' else 'container metadata only; no full-frame decode or playback claim')
raise SystemExit(0 if all(checks.values()) else 1)
