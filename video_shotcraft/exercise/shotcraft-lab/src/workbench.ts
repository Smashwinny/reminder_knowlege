import type { FC } from 'react';
import { Caption, CAPTION_DEFAULTS, FeatureShot, FEATURE_DEFAULTS, FlashCut, HeroShot, HERO_DEFAULTS, Main } from './Main';
import { CAPTIONS, FLASH_CUTS, SFX, SHOTS, TOTAL } from './timeline';

type Field = Record<string, unknown> & { type: string; key: string; label: string; default: unknown };
const text = (key: string, label: string, def: string): Field => ({ type: 'text', key, label, default: def });
const textarea = (key: string, label: string, def: string): Field => ({ type: 'textarea', key, label, default: def });
const color = (key: string, label: string, def: string): Field => ({ type: 'color', key, label, default: def });
const size = (key: string, label: string, def: number): Field => ({ type: 'slider', key, label, default: def, min: 14, max: 80, step: 1, unit: 'px' });

export const WORKBENCH = {
  name: 'Shotcraft learning lab',
  fps: 30,
  width: 960,
  height: 540,
  total: TOTAL,
  background: '#090d1c',
  shots: [
    {
      id: 'hero', label: 'S1 单主角产品镜头', from: SHOTS.hero.from, duration: SHOTS.hero.duration,
      component: HeroShot as FC<Record<string, unknown>>, props: { ...HERO_DEFAULTS },
      schema: [text('product', '产品名', HERO_DEFAULTS.product), text('kicker', '眉题', HERO_DEFAULTS.kicker), color('accent', '强调色', HERO_DEFAULTS.accent), size('fontSize', '产品名字号', HERO_DEFAULTS.fontSize)],
    },
    {
      id: 'features', label: 'S2 功能落点', from: SHOTS.features.from, duration: SHOTS.features.duration,
      component: FeatureShot as FC<Record<string, unknown>>, props: { ...FEATURE_DEFAULTS }, durationProp: 'duration',
      schema: [textarea('title', '标题', FEATURE_DEFAULTS.title), textarea('items', '功能（每行一条）', FEATURE_DEFAULTS.items), color('accent', '强调色', FEATURE_DEFAULTS.accent), size('fontSize', '标题字号', FEATURE_DEFAULTS.fontSize)],
    },
  ],
  transitions: FLASH_CUTS.map((cut, i) => ({
    id: `flash-${i}`, label: '跨切点暖白闪', from: cut - 5, duration: 10,
    component: FlashCut as FC<Record<string, unknown>>, durationProp: 'duration', cardId: 'flash-cut', cardName: '暖白闪转场',
  })),
  captions: CAPTIONS.map((c, i) => ({
    id: `caption-${i}`, label: c.text, from: c.from, duration: c.duration,
    component: Caption as FC<Record<string, unknown>>, props: { ...CAPTION_DEFAULTS, ...c }, durationProp: 'duration',
    schema: [text('text', '字幕', c.text), color('color', '文字色', CAPTION_DEFAULTS.color), color('accent', '方点色', CAPTION_DEFAULTS.accent), size('fontSize', '字号', CAPTION_DEFAULTS.fontSize)],
    cardId: 'caption', cardName: '解说字幕条',
  })),
  sfx: SFX.map((s) => ({ from: s.from, duration: s.duration, src: `audio/${s.src}`, volume: s.volume })),
  order: ['transitions', 'captions', 'overlays'] as const,
  original: Main as unknown as FC<Record<string, unknown>>,
};
