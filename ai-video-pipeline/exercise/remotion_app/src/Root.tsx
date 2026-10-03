import React from "react";
import { Composition, staticFile, Audio, Sequence, AbsoluteFill, interpolate, useCurrentFrame } from "remotion";

type Sentence = { index: number; text: string; start: number; end: number; dur: number };
type Timeline = { voice: string; sentences: Sentence[]; total: number };

const FPS = 30;

// 每句一张"证据卡"配色（高饱和，对标文章"把需要比较的数据放在同一画面"）
const COLORS = [
  ["#e63946", "#ffd166"],
  ["#1d6fd1", "#8ecae6"],
  ["#2a9d8f", "#caf0f8"],
  ["#7b2cbf", "#e0aaff"],
  ["#e76f51", "#ffe8d6"],
];

const TitleCard: React.FC<{ total: number }> = ({ total }) => {
  const frame = useCurrentFrame();
  const rise = interpolate(frame, [0, 15], [60, 0], { extrapolateRight: "clamp" });
  const opacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ background: "linear-gradient(135deg, #1d3557 0%, #457b9d 100%)", justifyContent: "center", alignItems: "center" }}>
      <div style={{ transform: `translateY(${rise}px)`, opacity, textAlign: "center" }}>
        <div style={{ fontSize: 72, fontWeight: 900, color: "#ffffff" }}>物业费到底花在了哪里？</div>
        <div style={{ fontSize: 34, color: "#ffb703", marginTop: 24, fontWeight: 700 }}>
          一次可核查的深度解读 · 全流程 AI 流水线产出
        </div>
        <div style={{ fontSize: 26, color: "#cbd5e1", marginTop: 18 }}>
          旁白 {total.toFixed(1)} 秒 · edge-tts 配音 · Remotion 逐帧渲染
        </div>
      </div>
    </AbsoluteFill>
  );
};

const EvidenceCard: React.FC<{ s: Sentence }> = ({ s }) => {
  const frame = useCurrentFrame();
  const local = frame; // 已在 Sequence 内，local 从 0 起
  const slide = interpolate(local, [0, 12], [80, 0], { extrapolateRight: "clamp" });
  const opacity = interpolate(local, [0, 12], [0, 1], { extrapolateRight: "clamp" });
  const [bg, accent] = COLORS[s.index % COLORS.length];
  const hasSource = s.index >= 1; // 演示：第 2 句起挂"出处条"，对标文章"画面保留素材出处"
  return (
    <AbsoluteFill style={{ background: `linear-gradient(150deg, ${bg} 0%, #10243e 130%)` }}>
      <div style={{ padding: 80, transform: `translateX(${slide}px)`, opacity }}>
        <div style={{ display: "inline-block", background: accent, color: "#10243e", fontSize: 28, fontWeight: 900, padding: "8px 24px", borderRadius: 999 }}>
          关键事实 {s.index + 1}/{5}
        </div>
        <div style={{ fontSize: 52, fontWeight: 900, color: "#ffffff", lineHeight: 1.45, marginTop: 36, maxWidth: 1080 }}>
          {s.text}
        </div>
        {hasSource && (
          <div style={{ marginTop: 48, fontSize: 22, color: "#e2e8f0", background: "rgba(16,36,62,0.55)", padding: "12px 20px", borderRadius: 12, display: "inline-block" }}>
            出处：《民法典》第943条 物业服务人公开义务 · flk.npc.gov.cn
          </div>
        )}
        {/* 底部进度条：本句时长占比 */}
        <div style={{ position: "absolute", bottom: 40, left: 80, right: 80, height: 10, background: "rgba(255,255,255,0.25)", borderRadius: 5 }}>
          <div style={{ width: `${Math.min(100, (local / (s.dur * FPS)) * 100)}%`, height: "100%", background: accent, borderRadius: 5 }} />
        </div>
      </div>
    </AbsoluteFill>
  );
};

const DeepDive: React.FC<{ timeline: Timeline }> = ({ timeline }) => {
  return (
    <AbsoluteFill style={{ background: "#10243e" }}>
      <Sequence from={0} durationInFrames={3 * FPS}>
        <TitleCard total={timeline.total} />
      </Sequence>
      {/* 片头 3 秒后旁白+逐句证据卡入场：出入点全部来自真实 TTS 时长（词锚定语义时间），
          旁白整体延后 3 秒，与画面对齐。 */}
      <Sequence from={3 * FPS}>
        <Audio src={staticFile("narration.mp3")} />
        {timeline.sentences.map((s) => (
          <Sequence key={s.index} from={Math.round(s.start * FPS)} durationInFrames={Math.ceil(s.dur * FPS)}>
            <EvidenceCard s={s} />
          </Sequence>
        ))}
      </Sequence>
    </AbsoluteFill>
  );
};

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="DeepDive"
      component={DeepDive}
      fps={FPS}
      width={1280}
      height={720}
      defaultProps={{
        timeline: {
          voice: "zh-CN-YunxiNeural",
          total: 30.38,
          sentences: [
            { index: 0, text: "占位句", start: 0, end: 1, dur: 1 },
          ],
        } as Timeline,
      }}
      calculateMetadata={({ props }) => ({
        durationInFrames: Math.ceil((props.timeline.total + 3) * FPS),
      })}
    />
  );
};
