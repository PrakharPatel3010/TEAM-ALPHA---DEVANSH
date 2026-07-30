import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL = "gemini-flash-latest"

SUMMARY_PROMPT = """
You are given the full text of a research paper.

Return STRICT JSON only.

{
  "overview": "1-2 sentences on what the paper is about",
  "methods": "2-3 sentences describing methodology",
  "results": "2-3 sentences summarizing findings",
  "limitations": "1-2 sentences describing limitations"
}
"""


def summarize_text(extracted_text: str):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found.")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=MODEL,
        contents=f"{SUMMARY_PROMPT}\n\nPAPER:\n{extracted_text}",
    )

    raw = response.text.strip()

    raw = raw.replace("```json", "")
    raw = raw.replace("```", "")
    raw = raw.strip()

    try:
        return json.loads(raw)

    except json.JSONDecodeError:

        return {
            "overview": raw,
            "methods": "",
            "results": "",
            "limitations": ""
        }