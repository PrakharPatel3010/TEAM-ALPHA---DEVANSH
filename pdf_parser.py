"""
Step 2: Parse a PDF into page-tagged text chunks.

Every chunk keeps its page_number so later steps can cite the exact
page a claim came from. This is the foundation of the "verified with
citations" feature.
"""
import sys
import json
import fitz  # PyMuPDF


def parse_pdf(pdf_path: str, max_chars_per_chunk: int = 1200):
    """
    Returns a list of chunks:
    [{"chunk_id": 0, "page_number": 1, "text": "..."}, ...]
    """
    doc = fitz.open(pdf_path)
    chunks = []
    chunk_id = 0

    for page_index in range(len(doc)):
        page = doc[page_index]
        page_number = page_index + 1
        text = page.get_text("text").strip()

        if not text:
            continue

        for start in range(0, len(text), max_chars_per_chunk):
            piece = text[start:start + max_chars_per_chunk].strip()
            if piece:
                chunks.append({
                    "chunk_id": chunk_id,
                    "page_number": page_number,
                    "text": piece
                })
                chunk_id += 1

    doc.close()
    return chunks


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pdf_parser.py <path_to_pdf>")
        sys.exit(1)

    result = parse_pdf(sys.argv[1])
    print(json.dumps(result, indent=2))
    print(f"\n--- Parsed {len(result)} chunks ---", file=sys.stderr)