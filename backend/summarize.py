"""
Your part: take the text your friend's code extracted from the PDF,
send it to a free AI model (Google Gemini), and get back a clean summary.
"""
import json
import os
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-flash-latest"  # free-tier model, large context window

SUMMARY_PROMPT = """You are given the full text of a research paper.

Read it and return a summary as STRICT JSON only, no other text, no markdown fences:
{
  "overview": "1-2 sentences on what the paper is about",
  "methods": "2-3 sentences on how the study was done",
  "results": "2-3 sentences on what they found",
  "limitations": "1-2 sentences on caveats or weaknesses"
}
"""


def summarize_text(extracted_text: str):
    response = client.models.generate_content(
        model=MODEL,
        contents=f"{SUMMARY_PROMPT}\n\nPAPER TEXT:\n{extracted_text}",
    )

    raw = response.text.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"overview": raw, "methods": "", "results": "", "limitations": ""}


if __name__ == "__main__":
    sample_text = """
    [PAGE 1] We introduce a new architecture based entirely on attention
    mechanisms, removing recurrence and convolutions...
    [PAGE 7] Our model achieves state-of-the-art BLEU scores on translation
    benchmarks while training significantly faster...
    """
    result = summarize_text(sample_text)
    print(json.dumps(result, indent=2))