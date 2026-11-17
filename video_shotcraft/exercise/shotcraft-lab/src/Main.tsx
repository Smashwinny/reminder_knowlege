import React from 'react';
import { AbsoluteFill, Audio, Easing, interpolate, Sequence, staticFile, useCurrentFrame } from 'remotion';
import { CAPTIONS, FLASH_CUTS, SFX, SHOTS } from './timeline';

const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;

export const HERO_DEFAULTS = {
  product: 'NOVA Focus',
  kicker: 'A CALMER WORKSPACE',
  accent: '#ffb703',
  fontSize: 42,
};

export const FEATURE_DEFAULTS = {
  title: 'Everything lands\nright on beat.',
  items: 'Capture the real product\nPin motion to frames\nEdit every layer',
  accent: '#ff4d8d',
  fontSize: 46,
  duration: 90,
};

export const CAPTION_DEFAULTS = {
  text: '',
  color: '#ffffff',
  accent: '#ffb703',
  fontSize: 18,
  duration: 48,
};

const ProductCard: React.FC<{ product: string; kicker: string; accent: string; fontSize: number }> = ({
  product, kicker, accent, fontSize,
}) => (
  <div style={{
    width: 560, borderRadius: 28, padding: 34, color: '#17213b',
    background: 'linear-gradient(145deg, #ffffff, #e8f2ff)',
    border: '2px solid rgba(255,255,255,0.8)',
    boxShadow: '0 35px 100px rgba(0,0,0,0.45)',
    fontFamily: 'Arial, sans-serif',
  }}>
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
      <div style={{ fontSize: 15, fontWeight: 800, letterSpacing: 3, color: '#53627d' }}>{kicker}</div>
      <div style={{ width: 18, height: 18, borderRadius: 18, background: accent, boxShadow: `0 0 30px ${accent}` }} />
    </div>
    <div style={{ marginTop: 28, fontSize, lineHeight: 1.05, fontWeight: 900 }}>{product}</div>
    <div style={{ marginTop: 28, display: 'grid', gridTemplateColumns: '1.4fr 1fr', gap: 16 }}>
      <div style={{ height: 122, borderRadius: 18, background: '#17213b', padding: 18, boxSizing: 'border-box' }}>
        {[0.82, 0.56, 0.7].map((w, i) => <div key={i} style={{ width: `${w * 100}%`, height: 10, marginBottom: 15, borderRadius: 8, background: i === 0 ? accent : '#7e8daa' }} />)}
      </div>
      <div style={{ height: 122, borderRadius: 18, background: accent, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 42, fontWeight: 900 }}>03</div>
    </div>
  </div>
);

export const HeroShot: React.FC<Partial<typeof HERO_DEFAULTS>> = (props) => {
  const p = { ...HERO_DEFAULTS, ...props };
  const frame = useCurrentFrame();
  const enter = interpolate(frame, [0, 24], [0, 1], { ...clamp, easing: Easing.bezier(0.16, 1, 0.3, 1) });
  const lift = interpolate(frame, [30, 44, 58, 70], [0, 1, 1, 0], { ...clamp, easing: Easing.inOut(Easing.ease) });
  const spotX = interpolate(frame, [0, 20, 34], [22, 72, 50], { ...clamp, easing: Easing.inOut(Easing.ease) });
  const scale = (0.78 + enter * 0.22) * (1 + lift * 0.055);
  return (
    <AbsoluteFill style={{ background: '#090d1c', overflow: 'hidden', fontFamily: 'Arial, sans-serif' }}>
      <AbsoluteFill style={{
        background: `radial-gradient(circle at ${spotX}% 44%, ${p.accent}55 0%, #354aa766 22%, transparent 58%)`,
        opacity: 0.45 + enter * 0.55,
      }} />
      <div style={{
        position: 'absolute', left: 200, top: 105,
        transform: `translateY(${70 * (1 - enter) - 26 * lift}px) scale(${scale}) rotateY(${-10 * lift}deg)`,
        transformOrigin: 'center center',
      }}>
        <ProductCard {...p} />
      </div>
      <div style={{ position: 'absolute', left: 62, bottom: 45, color: '#fff', fontSize: 16, letterSpacing: 4, fontWeight: 700, opacity: enter }}>
        SPOTLIGHT → LIFT → RESEAT
      </div>
    </AbsoluteFill>
  );
};

export const FeatureShot: React.FC<Partial<typeof FEATURE_DEFAULTS>> = (props) => {
  const p = { ...FEATURE_DEFAULTS, ...props };
  const frame = useCurrentFrame();
  const exit = interpolate(frame, [p.duration - 8, p.duration], [1, 0], clamp);
  return (
    <AbsoluteFill style={{ background: 'linear-gradient(135deg, #27104f, #071a38)', color: '#fff', fontFamily: 'Arial, sans-serif', opacity: exit }}>
      <div style={{ position: 'absolute', width: 520, height: 520, right: -170, top: -190, borderRadius: 520, background: p.accent, opacity: 0.28, filter: 'blur(20px)' }} />
      <div style={{ position: 'absolute', left: 66, top: 60, whiteSpace: 'pre-line', fontSize: p.fontSize, lineHeight: 1.08, fontWeight: 900 }}>
        {p.title}
      </div>
      <div style={{ position: 'absolute', left: 68, top: 230, width: 825 }}>
        {p.items.split('\n').map((item, i) => {
          const on = interpolate(frame, [12 + i * 12, 28 + i * 12], [0, 1], { ...clamp, easing: Easing.bezier(0.16, 1, 0.3, 1) });
          return <div key={item} style={{
            display: 'flex', alignItems: 'center', gap: 20, marginBottom: 15, padding: '16px 22px',
            borderRadius: 16, background: 'rgba(255,255,255,0.1)', border: '1px solid rgba(255,255,255,0.18)',
            fontSize: 23, fontWeight: 700, opacity: on, transform: `translateX(${90 * (1 - on)}px)`,
          }}><span style={{ color: p.accent, fontSize: 28 }}>0{i + 1}</span>{item}</div>;
        })}
      </div>
    </AbsoluteFill>
  );
};

export const FlashCut: React.FC<{ duration?: number }> = ({ duration = 10 }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, duration * 0.4, duration], [0, 0.85, 0], clamp);
  return <AbsoluteFill style={{ pointerEvents: 'none', opacity, background: 'radial-gradient(ellipse at 50% 45%, rgba(255,248,235,0.98), rgba(255,244,224,0.55) 55%, transparent 80%)' }} />;
};

export const Caption: React.FC<Partial<typeof CAPTION_DEFAULTS>> = (props) => {
  const p = { ...CAPTION_DEFAULTS, ...props };
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 7, p.duration - 7, p.duration], [0, 1, 1, 0], clamp);
  return <AbsoluteFill style={{ pointerEvents: 'none', opacity }}>
    <div style={{ position: 'absolute', bottom: 28, left: 70, right: 70, color: p.color, fontFamily: 'Arial, sans-serif', fontSize: p.fontSize, fontWeight: 800, letterSpacing: 2, textAlign: 'center' }}>
      <span style={{ color: p.accent }}>■</span> {p.text}
    </div>
  </AbsoluteFill>;
};

export const Main: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: '#090d1c' }}>
    {SFX.map((s) => <Sequence key={s.src} from={s.from} durationInFrames={s.duration}>
      <Audio src={staticFile(`audio/${s.src}`)} volume={s.volume} />
    </Sequence>)}
    <Sequence from={SHOTS.hero.from} durationInFrames={SHOTS.hero.duration}><HeroShot /></Sequence>
    <Sequence from={SHOTS.features.from} durationInFrames={SHOTS.features.duration}><FeatureShot /></Sequence>
    {CAPTIONS.map((c) => <Sequence key={c.from} from={c.from} durationInFrames={c.duration}><Caption {...c} /></Sequence>)}
    {FLASH_CUTS.map((cut) => <Sequence key={cut} from={cut - 5} durationInFrames={10}><FlashCut duration={10} /></Sequence>)}
  </AbsoluteFill>
);
