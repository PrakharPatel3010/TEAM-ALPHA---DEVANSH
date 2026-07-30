"""
Step 3: Extract claims, methods, results, and limitations from the paper
as structured JSON, each item tagged with the page it came from.
"""
import sys
import json
from anthropic import Anthropic
from pdf_parser import parse_pdf

client = Anthropic()

EXTRACTION_SYSTEM_PROMPT = """You are a research paper analysis engine.
You will be given the full text of a research paper, with each page's text
labeled by its page number.

Extract the following into STRICT JSON and nothing else — no preamble, no
markdown fences, no commentary:

{
  "claims": [
    {"text": "...", "page_number": <int>}
  ],
  "methods": [
    {"text": "...", "page_number": <int>}
  ],
  "results": [
    {"text": "...", "page_number": <int>}
  ],
  "limitations": [
    {"text": "...", "page_number": <int>}
  ]
}

Rules:
- "claims" = the paper's core arguments or contributions (usually from the
  abstract/introduction/conclusion).
- "methods" = how the study was conducted (data, model, experimental setup).
- "results" = quantitative or qualitative findings.
- "limitations" = anything the authors themselves acknowledge as a limitation,
  or a clear methodological weakness (e.g. small sample size, narrow dataset).
- Every item MUST have the page_number where it was stated.
- Keep each "text" field to one or two sentences, in your own words (not a
  verbatim copy of the source), so it reads as a clean summary point.
- Extract 5-10 items per category. If a category genuinely doesn't apply,
  return an empty list for it.
- Return ONLY the JSON object, nothing else.
"""


def build_labeled_text(chunks):
    parts = []
    for c in chunks:
        parts.append(f"[PAGE {c['page_number']}]\n{c['text']}")
    return "\n\n".join(parts)


def extract_structured_info(pdf_path: str):
    chunks = parse_pdf(pdf_path)
    labeled_text = build_labeled_text(chunks)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        system=EXTRACTION_SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": labeled_text}
        ]
    )

    raw_text = response.content[0].text.strip()
    raw_text = raw_text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        print("Warning: model did not return clean JSON, returning raw text.", file=sys.stderr)
        return {"raw": raw_text}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract.py <path_to_pdf>")
        sys.exit(1)

    result = extract_structured_info(sys.argv[1])
    print(json.dumps(result, indent=2))