"""
Step 5: Generate the four learner-facing outputs from verified points:
summary, flashcards, concept map, and slides.
"""
import sys
import json
from anthropic import Anthropic
from verify import verify_all

client = Anthropic()


def _call(system_prompt, verified_json):
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=system_prompt,
        messages=[{"role": "user", "content": json.dumps(verified_json)}]
    )
    raw = response.content[0].text.strip().replace("```json", "").replace("```", "")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw": raw}


SUMMARY_PROMPT = """You will receive verified claims, methods, results, and
limitations from a research paper as JSON. Only use items where "verified"
is true; ignore unverified ones.

Write a clear plain-language summary a student can read in 2 minutes.
Return STRICT JSON only:
{
  "summary": {
    "overview": "1-2 sentences on what the paper is about",
    "methods": "2-3 sentences on how they did it",
    "results": "2-3 sentences on what they found",
    "limitations": "1-2 sentences on caveats"
  }
}
"""

FLASHCARDS_PROMPT = """You will receive verified claims, methods, results,
and limitations from a research paper as JSON. Only use items where
"verified" is true.

Create 8-12 flashcards for exam-style review. Return STRICT JSON only:
{
  "flashcards": [
    {"question": "...", "answer": "...", "page_number": <int>}
  ]
}
"""

CONCEPT_MAP_PROMPT = """You will receive verified claims, methods, results,
and limitations from a research paper as JSON. Only use items where
"verified" is true.

Build a concept map showing how methods lead to results, and how results
support claims. Return STRICT JSON only:
{
  "nodes": [{"id": "n1", "label": "...", "type": "method|result|claim|limitation"}],
  "edges": [{"source": "n1", "target": "n2", "label": "leads to"}]
}
Keep it to 8-15 nodes maximum so it stays readable.
"""

SLIDES_PROMPT = """You will receive verified claims, methods, results, and
limitations from a research paper as JSON. Only use items where "verified"
is true.

Create a presentation-ready slide outline (5-7 slides). Return STRICT JSON
only:
{
  "slides": [
    {"title": "...", "bullets": ["...", "...", "..."], "page_number": <int>}
  ]
}
"""


def generate_all_outputs(pdf_path: str):
    verified = verify_all(pdf_path)

    return {
        "summary": _call(SUMMARY_PROMPT, verified).get("summary"),
        "flashcards": _call(FLASHCARDS_PROMPT, verified).get("flashcards"),
        "concept_map": _call(CONCEPT_MAP_PROMPT, verified),
        "slides": _call(SLIDES_PROMPT, verified).get("slides"),
        "verified_source": verified,
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate.py <path_to_pdf>")
        sys.exit(1)

    result = generate_all_outputs(sys.argv[1])
    print(json.dumps(result, indent=2))