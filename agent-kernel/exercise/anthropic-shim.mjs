#!/usr/bin/env node
// OpenAI chat/completions -> Anthropic /v1/messages 协议适配 shim（零依赖）
// 用途：让 build-your-own-coding-agent 的 mini-agent 跑在 z.ai Anthropic 兼容端点上。
// 用法：ANTHROPIC_BASE_URL=... ANTHROPIC_AUTH_TOKEN=... node anthropic-shim.mjs [port]
//       然后给 agent 设 LLM_BASE_URL=http://localhost:8787 DEEPSEEK_API_KEY=anything
//
// 特性：
// - 支持 stream:true（把 Anthropic 非流式响应合成 OpenAI SSE 分片吐回）和 stream:false
// - 429/限流自动等待 65s 重试（z.ai 端点约 1 次/分钟，与 Claude Code 会话共享配额）
// - 跳过 thinking 等 Anthropic 特有 content block，只映射 text / tool_use

import http from "node:http";

const PORT = Number(process.argv[2] ?? 8787);
const BASE = process.env.ANTHROPIC_BASE_URL ?? "https://api.z.ai/api/anthropic";
const TOKEN = process.env.ANTHROPIC_AUTH_TOKEN;
if (!TOKEN) {
	console.error("需要 ANTHROPIC_AUTH_TOKEN");
	process.exit(1);
}
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// ---- OpenAI 请求 -> Anthropic 请求 ----
function toAnthropic(body) {
	const system = [];
	const messages = [];
	for (const m of body.messages ?? []) {
		if (m.role === "system") {
			system.push(m.content);
		} else if (m.role === "user") {
			messages.push({ role: "user", content: [{ type: "text", text: m.content ?? "" }] });
		} else if (m.role === "assistant") {
			const content = [];
			if (m.content) content.push({ type: "text", text: m.content });
			for (const tc of m.tool_calls ?? []) {
				content.push({
					type: "tool_use",
					id: tc.id,
					name: tc.function.name,
					input: safeParse(tc.function.arguments),
				});
			}
			messages.push({ role: "assistant", content });
		} else if (m.role === "tool") {
			// OpenAI 的 tool 结果 -> Anthropic 的 user/tool_result
			const last = messages[messages.length - 1];
			const block = {
				type: "tool_result",
				tool_use_id: m.tool_call_id,
				content: m.content ?? "",
			};
			if (last?.role === "user" && Array.isArray(last.content) && last.content[0]?.type === "tool_result") {
				last.content.push(block); // 同一轮多个结果合并进一条 user 消息
			} else {
				messages.push({ role: "user", content: [block] });
			}
		}
	}
	return {
		model: body.model ?? "glm-4.6",
		max_tokens: body.max_tokens ?? 8192,
		system: system.join("\n") || undefined,
		messages,
		tools: (body.tools ?? [])
			.filter((t) => t.type === "function")
			.map((t) => ({
				name: t.function.name,
				description: t.function.description,
				input_schema: t.function.parameters,
			})),
	};
}

function safeParse(s) {
	try {
		return JSON.parse(s || "{}");
	} catch {
		return { _raw: s };
	}
}

// ---- Anthropic 响应 -> OpenAI 响应 ----
function toOpenAI(anyc, model) {
	let text = "";
	const toolCalls = [];
	for (const block of anyc.content ?? []) {
		if (block.type === "text") text += block.text;
		else if (block.type === "tool_use")
			toolCalls.push({
				id: block.id,
				type: "function",
				function: { name: block.name, arguments: JSON.stringify(block.input) },
			});
		// thinking / redacted_thinking 等块直接丢弃
	}
	const message = { role: "assistant", content: text || null };
	if (toolCalls.length) message.tool_calls = toolCalls;
	return {
		id: anyc.id ?? `chatcmpl-${Date.now()}`,
		object: "chat.completion",
		created: Math.floor(Date.now() / 1000),
		model,
		choices: [
			{
				index: 0,
				message,
				finish_reason: anyc.stop_reason === "tool_use" ? "tool_calls" : "stop",
			},
		],
		usage: {
			prompt_tokens: anyc.usage?.input_tokens ?? 0,
			completion_tokens: anyc.usage?.output_tokens ?? 0,
			total_tokens: (anyc.usage?.input_tokens ?? 0) + (anyc.usage?.output_tokens ?? 0),
		},
	};
}

// 带限流重试的上游调用
async function callUpstream(anthropicBody) {
	for (let attempt = 1; attempt <= 6; attempt++) {
		const res = await fetch(`${BASE}/v1/messages`, {
			method: "POST",
			headers: {
				"content-type": "application/json",
				"x-api-key": TOKEN,
				authorization: `Bearer ${TOKEN}`,
				"anthropic-version": "2023-06-01",
			},
			body: JSON.stringify(anthropicBody),
		});
		if (res.ok) return res.json();
		const errText = await res.text();
		if (res.status === 429 || /rate|limit|frequency/i.test(errText)) {
			console.error(`[shim] 上游限流（第 ${attempt} 次），65s 后重试`);
			await sleep(65_000);
			continue;
		}
		throw new Error(`上游 HTTP ${res.status}: ${errText.slice(0, 300)}`);
	}
	throw new Error("上游连续限流，放弃");
}

const server = http.createServer(async (req, res) => {
	if (req.method !== "POST" || !req.url.includes("/chat/completions")) {
		res.writeHead(404).end("not found");
		return;
	}
	let raw = "";
	for await (const chunk of req) raw += chunk;
	const openaiBody = JSON.parse(raw);
	const model = openaiBody.model ?? "glm-4.6";
	try {
		const anyc = await callUpstream(toAnthropic(openaiBody));
		const openaiResp = toOpenAI(anyc, model);
		if (!openaiBody.stream) {
			res.writeHead(200, { "content-type": "application/json" });
			res.end(JSON.stringify(openaiResp));
			return;
		}
		// 合成 SSE：一帧 role + 一帧内容 + tool_calls 帧 + 收尾帧
		res.writeHead(200, { "content-type": "text/event-stream" });
		const msg = openaiResp.choices[0].message;
		const frame = (delta, finish) =>
			`data: ${JSON.stringify({
				id: openaiResp.id,
				object: "chat.completion.chunk",
				created: openaiResp.created,
				model,
				choices: [{ index: 0, delta, finish_reason: finish ?? null }],
			})}\n\n`;
		res.write(frame({ role: "assistant", content: "" }));
		if (msg.content) res.write(frame({ content: msg.content }));
		if (msg.tool_calls)
			for (let i = 0; i < msg.tool_calls.length; i++) {
				const tc = msg.tool_calls[i];
				res.write(frame({ tool_calls: [{ index: i, id: tc.id, type: "function", function: tc.function }] }));
			}
		res.write(frame({}, openaiResp.choices[0].finish_reason));
		res.write("data: [DONE]\n\n");
		res.end();
	} catch (err) {
		res.writeHead(502, { "content-type": "application/json" });
		res.end(JSON.stringify({ error: { message: String(err.message ?? err) } }));
	}
});

server.listen(PORT, () => console.log(`[shim] OpenAI->Anthropic 适配层已就绪 http://localhost:${PORT}/v1/chat/completions`));
