// mock-jev-server.mjs — 本地假 TypeSafe Jev API
// 用途：jev-router 的 askJev() 通过 @typesafe-ai/sdk 向 {TYPESAFE_BASE_URL}/v1/systemone
// 发 POST。本服务器实现该端点，按提示词关键词返回"类型化决策"，并记录收到的请求，
// 让我们在没有 Jev API key 的情况下也能驱动 jev-router 的真实路由代码路径。
//
// 运行: node mock-jev-server.mjs [端口]
// 决策规则（看 state.request 里的用户提示词）:
//   含 "architecture" / "refactor everything"  ->  opus,  置信度 0.92
//   含 "unit test" 等普通工程任务             ->  sonnet, 置信度 0.80
//   含 "uncertain"                            ->  opus,  但置信度只有 0.10（触发低置信策略）
//   其他（琐碎问答）                          ->  haiku,  置信度 0.95
import { createServer } from "node:http";
import { appendFileSync } from "node:fs";

const PORT = Number(process.argv[2] ?? 8377);
const LOG = new URL("./mock-jev-requests.jsonl", import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1");

const server = createServer((req, res) => {
  if (req.method !== "POST" || req.url !== "/v1/systemone") {
    res.writeHead(404).end(JSON.stringify({ error: "not found" }));
    return;
  }
  let raw = "";
  req.on("data", (c) => (raw += c));
  req.on("end", () => {
    const body = JSON.parse(raw);
    const prompt = body?.state?.request ?? "";
    appendFileSync(LOG, JSON.stringify({ time: new Date().toISOString(), prompt, questions: Object.keys(body?.questions ?? {}) }) + "\n");

    let choice = "claude-haiku-4-5-20251001", confidence = 0.95, scores = [1, 1, 0];
    if (/architecture|refactor everything/i.test(prompt)) {
      choice = "claude-opus-5"; confidence = 0.92; scores = [7, 8, 5];
    } else if (/uncertain/i.test(prompt)) {
      choice = "claude-opus-5"; confidence = 0.1; scores = [5, 5, 5];
    } else if (/unit test|implement|fix/i.test(prompt)) {
      choice = "claude-sonnet-5"; confidence = 0.8; scores = [4, 4, 3];
    }

    // 模拟 Jev 的真实响应形态：answers 按问题名给类型化答案
    res.writeHead(200, { "Content-Type": "application/json" }).end(
      JSON.stringify({
        answers: {
          model: { choice, confidence },
          task_complexity: { score: scores[0] },
          reasoning_required: { score: scores[1] },
          tool_complexity: { score: scores[2] },
        },
        usage: { input_tokens: 500, output_tokens: 0 },
      }),
    );
  });
});
server.listen(PORT, "127.0.0.1", () => console.log(`mock Jev API listening on http://127.0.0.1:${PORT}/v1/systemone`));
