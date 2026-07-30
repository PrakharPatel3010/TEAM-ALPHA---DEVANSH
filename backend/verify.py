"""
Step 4: Verify every extracted item against the actual source text on its
claimed page. This is the trust layer that makes the agent "verified with
citations" rather than just an LLM summary.
"""
import sys
import json
from anthropic import Anthropic
from pdf_parser import parse_pdf
from extract import extract_structured_info

client = Anthropic()

VERIFICATION_SYSTEM_PROMPT = """You are a fact-checking engine for research paper summaries.

You will be given:
1. A single extracted point (a claim, method, result, or limitation).
2. The actual source text from the page it claims to come from.

Decide whether the source text genuinely supports the extracted point.

Return STRICT JSON only, no other text:
{
  "supported": true or false,
  "confidence": <float between 0 and 1>,
  "supporting_span": "the exact minimal sentence or phrase from the source
    text that best supports this point, or empty string if not supported",
  "reason": "one short sentence explaining your judgment"
}

Be strict: if the source text only loosely relates but doesn't actually
state the point, mark supported as false and confidence low.
"""


def verify_item(item_text: str, page_number: int, page_text: str):
    user_content = (
        f"EXTRACTED POINT:\n{item_text}\n\n"
        f"SOURCE TEXT (page {page_number}):\n{page_text}"
    )

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system=VERIFICATION_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}]
    )

    raw = response.content[0].text.strip().replace("```json", "").replace("```", "")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"supported": False, "confidence": 0.0, "supporting_span": "", "reason": "parse_error"}


def verify_all(pdf_path: str, confidence_threshold: float = 0.6):
    chunks = parse_pdf(pdf_path)
    page_text_map = {}
    for c in chunks:
        page_text_map.setdefault(c["page_number"], []).append(c["text"])
    page_text_map = {p: " ".join(texts) for p, texts in page_text_map.items()}

    extraction = extract_structured_info(pdf_path)
    verified = {}

    for category in ["claims", "methods", "results", "limitations"]:
        verified[category] = []
        for item in extraction.get(category, []):
            page_text = page_text_map.get(item["page_number"], "")
            check = verify_item(item["text"], item["page_number"], page_text)
            verified[category].append({
                **item,
                "verified": check["supported"] and check["confidence"] >= confidence_threshold,
                "confidence": check["confidence"],
                "supporting_span": check["supporting_span"],
            })

    return verified


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python verify.py <path_to_pdf>")
        sys.exit(1)

    result = verify_all(sys.argv[1])
    print(json.dumps(result, indent=2))