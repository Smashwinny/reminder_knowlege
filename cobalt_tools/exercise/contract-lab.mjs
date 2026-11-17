import assert from "node:assert/strict";
import { fileURLToPath } from "node:url";

// version-info discovers the package root from cwd, just like the official API.
process.chdir(fileURLToPath(new URL("../repo/api/", import.meta.url)));

// All media URLs below use the reserved .example domain and are never fetched.
process.env.API_URL = "http://127.0.0.1:19000/";
process.env.API_PORT = "19000";
process.env.API_LISTEN_ADDRESS = "127.0.0.1";

const { normalizeRequest, createResponse } = await import(
  "../repo/api/src/processing/request.js"
);
const { default: matchAction } = await import(
  "../repo/api/src/processing/match-action.js"
);
const { createStream, verifyStream, destroyInternalStream } = await import(
  "../repo/api/src/stream/manage.js"
);

const results = {};
let checks = 0;
const check = (condition, message) => {
  assert.ok(condition, message);
  checks += 1;
};

// 1. Real cobalt schema: URL canonicalization + defaults + strict unknown keys.
const normalized = await normalizeRequest({
  url: "https://youtu.be/ABCDEFGHIJK?t=43&list=local-fixture",
});
check(normalized.success, "a valid public-shaped URL must normalize");
check(
  normalized.data.url.toString() === "https://youtube.com/watch?v=ABCDEFGHIJK",
  "short URL must become a canonical watch URL with only v retained",
);
check(normalized.data.audioBitrate === "128", "default audio bitrate");
check(normalized.data.audioFormat === "mp3", "default audio format");
check(normalized.data.downloadMode === "auto", "default download mode");
check(normalized.data.videoQuality === "1080", "default video quality");
check(normalized.data.localProcessing === "disabled", "default processing location");
results.normalized = {
  url: normalized.data.url.toString(),
  defaults: {
    audioBitrate: normalized.data.audioBitrate,
    audioFormat: normalized.data.audioFormat,
    downloadMode: normalized.data.downloadMode,
    videoQuality: normalized.data.videoQuality,
    localProcessing: normalized.data.localProcessing,
  },
};

const rejected = await normalizeRequest({
  url: "https://youtu.be/ABCDEFGHIJK",
  madeUpOption: true,
});
check(rejected.success === false, "strict schema must reject unknown options");
results.strictUnknownOptionRejected = !rejected.success;

// 2. Real cobalt action mapper with a local in-memory extractor result.
const base = {
  r: {
    urls: [
      "https://media.example/self-written-video.mp4",
      "https://media.example/self-written-audio.m4a",
    ],
    filenameAttributes: {
      service: "youtube",
      id: "ABCDEFGHIJK",
      title: "Public Fixture",
      author: "Local Lab",
      extension: "mp4",
      resolution: "1920x1080",
      qualityLabel: "1080p",
      youtubeFormat: "h264",
    },
    fileMetadata: { title: "Public Fixture", artist: "Local Lab" },
    type: "merge",
  },
  host: "youtube",
  audioFormat: "mp3",
  isAudioOnly: false,
  isAudioMuted: false,
  disableMetadata: false,
  filenameStyle: "basic",
  convertGif: true,
  audioBitrate: "128",
  alwaysProxy: false,
  localProcessing: "disabled",
};

const serverSide = matchAction(base);
check(serverSide.status === 200, "server-side fixture response HTTP status");
check(serverSide.body.status === "tunnel", "merge defaults to a tunnel");
check(
  serverSide.body.filename === "Public Fixture - Local Lab (1080p, h264).mp4",
  "basic filename style must be visible",
);

const browserSide = matchAction({ ...base, localProcessing: "preferred" });
check(browserSide.body.status === "local-processing", "preferred merge moves work to client");
check(browserSide.body.type === "merge", "local processing type must remain merge");
check(browserSide.body.tunnel.length === 2, "video and audio need two proxy tunnels");
check(browserSide.body.output.type === "video/mp4", "output MIME comes from filename");
results.parameterChange = {
  localProcessing: {
    disabled: {
      status: serverSide.body.status,
      filename: serverSide.body.filename,
    },
    preferred: {
      status: browserSide.body.status,
      type: browserSide.body.type,
      tunnelCount: browserSide.body.tunnel.length,
      outputType: browserSide.body.output.type,
    },
  },
};

const redirectBase = {
  ...base,
  r: {
    urls: "https://media.example/self-written-public.mp4",
    filename: "public-fixture.mp4",
  },
  host: "vimeo",
};
const direct = matchAction(redirectBase);
const proxied = matchAction({ ...redirectBase, alwaysProxy: true });
check(direct.body.status === "redirect", "single vimeo fixture normally redirects");
check(proxied.body.status === "tunnel", "alwaysProxy converts redirect to tunnel");
results.alwaysProxy = {
  false: direct.body.status,
  true: proxied.body.status,
};

const picker = createResponse("picker", {
  picker: [
    { type: "photo", url: "https://media.example/one.jpg" },
    { type: "photo", url: "https://media.example/two.jpg", thumb: "https://media.example/two-thumb.jpg" },
  ],
});
check(picker.body.status === "picker", "multi-item fixture returns picker");
check(picker.body.picker.length === 2, "picker preserves both fixture items");
results.pickerItems = picker.body.picker.length;

// 3. Real signed tunnel implementation. No HTTP fetch is performed.
const tunnelURL = new URL(createStream({
  type: "proxy",
  url: "https://media.example/self-written.txt",
  service: "local-fixture",
  filename: "fixture.txt",
}));
await new Promise((resolve) => setTimeout(resolve, 30));
const q = tunnelURL.searchParams;
const valid = await verifyStream(
  q.get("id"), q.get("sig"), q.get("exp"), q.get("sec"), q.get("iv"),
);
check(valid.service === "local-fixture", "valid signed tunnel decrypts to fixture metadata");
const tampered = await verifyStream(
  q.get("id"), "A".repeat(43), q.get("exp"), q.get("sec"), q.get("iv"),
);
check(tampered.status === 401, "a tampered signature must be rejected");
results.signedTunnel = {
  parameterNames: [...q.keys()].sort(),
  validService: valid.service,
  tamperedStatus: tampered.status,
};
if (typeof valid.urls === "string") destroyInternalStream(valid.urls);

console.log(JSON.stringify({
  suite: "cobalt official modules + local no-network fixtures",
  checks,
  results,
}, null, 2));
console.log(`PASS: ${checks} assertions; 0 external media requests`);
