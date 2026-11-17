export const SHOTS = {
  hero: { from: 0, duration: 90 },
  features: { from: 90, duration: 90 },
} as const;

export const TOTAL = SHOTS.hero.duration + SHOTS.features.duration;
export const FLASH_CUTS = [SHOTS.features.from];
export const CAPTIONS = [
  { from: SHOTS.features.from + 18, duration: 48, text: 'ONE TIMELINE · EVERY BEAT EDITABLE' },
] as const;

// Filled from the measured 10 ms RMS peaks of the actual local files.
export const PEAK_F: Record<string, number> = {
  'whoosh-fast.mp3': 21.75,
  'impact-cine.mp3': 16.65,
  'transition-soft.mp3': 13.65,
};

// Baseline render intentionally starts at zero; the rendered-output probe replaces it.
export const OUTPUT_AUDIO_OFFSET_F = 0;

export const sfxFrom = (targetPeakF: number, src: string) =>
  Math.max(0, Math.round(targetPeakF - (PEAK_F[src] ?? 0) - OUTPUT_AUDIO_OFFSET_F));

export const SFX = [
  { target: SHOTS.hero.from + 36, src: 'whoosh-fast.mp3', volume: 0.45, action: 'hero card lift' },
  { target: SHOTS.hero.from + 70, src: 'impact-cine.mp3', volume: 0.5, action: 'hero card reseat' },
  { target: SHOTS.features.from + 24, src: 'transition-soft.mp3', volume: 0.4, action: 'feature rows land' },
].map((s) => ({ ...s, from: sfxFrom(s.target, s.src), duration: 90 }));
