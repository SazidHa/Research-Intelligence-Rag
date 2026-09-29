from pathlib import Path

import pymupdf


def load_pdf(pdf_path: str) -> list[dict]:
    path = Path(pdf_path)

    if not path.is_file():
        raise FileNotFoundError(f"PDF not found: {path}")

    pages = []
    with pymupdf.open(path) as document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text").strip()
            if text:
                pages.append({
                    "text": text,
                    "source": path.name,
                    "page": page_number,
                })

    return pages


if __name__ == "__main__":
    import sys

    pages = load_pdf(sys.argv[1])
    print(f"Extracted text from {len(pages)} pages")
    if pages:
        print(pages[0]["source"], "— page", pages[0]["page"])
        print(pages[0]["text"][:500])