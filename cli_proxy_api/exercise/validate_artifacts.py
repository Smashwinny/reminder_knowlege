"""Validate the public learning artifacts without third-party packages."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

PROJECT = Path(__file__).resolve().parent.parent
HTML = PROJECT / "cli_proxy_api-guide.html"
PDF = PROJECT / "cli_proxy_api-小白指南.pdf"
RESULTS = PROJECT / "exercise" / "experiment_results.json"
CAPTURES = PROJECT / "exercise" / "runtime" / "upstream_requests.jsonl"
OUTPUT = PROJECT / "exercise" / "artifact_validation.json"

html = HTML.read_text(encoding="utf-8")
pdf = PDF.read_bytes()
results = json.loads(RESULTS.read_text(encoding="utf-8"))
captures = [json.loads(line) for line in CAPTURES.read_text(encoding="utf-8").splitlines() if line.strip()]
questions = {}
for number in range(1, 11):
    marker = f'id="q{number}"'
    start = html.index(marker)
    next_match = re.search(r'<section class="question"', html[start + len(marker):])
    end = start + len(marker) + next_match.start() if next_match else len(html)
    block = html[start:end]
    questions[f"Q{number}"] = {"svg_count": block.count("<svg"), "has_answer": 'class="answer"' in block}

page_objects = len(re.findall(rb"/Type\s*/Page\b", pdf))
report = {
    "success": True,
    "html": {"path": HTML.name, "sha256": hashlib.sha256(HTML.read_bytes()).hexdigest(), "questions": questions},
    "pdf": {"path": PDF.name, "bytes": len(pdf), "sha256": hashlib.sha256(pdf).hexdigest(),
            "header": pdf[:8].decode("ascii"), "page_objects": page_objects,
            "has_eof": pdf.rstrip().endswith(b"%%EOF")},
    "experiment": {"success": results.get("success"), "upstream_captures": len(captures),
                   "external_model_calls": results.get("real_external_model_calls"),
                   "assertions": results.get("assertions")},
    "visual_check": {
        "html_cover_rendered_by_edge": True,
        "screenshot": "exercise/runtime/pdf-preview/html-cover.png",
        "pdf_pixel_review": "not_available_pdftoppm_missing_and_pymupdf_install_denied",
        "pdf_structure_checked": True,
    },
}
assert all(item["svg_count"] >= 1 and item["has_answer"] for item in questions.values())
assert pdf.startswith(b"%PDF-") and report["pdf"]["has_eof"] and page_objects >= 10
assert results["success"] is True and len(captures) == 6
assert results["real_external_model_calls"] == 0
OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, indent=2))
