import re

from backend.app.ingestion.pdf_loader import load_pdf


HEADING_PATTERN = re.compile(
    r"(?im)^[ \t]*(materials and methods|patients and methods|"
    r"methods|methodology|research design|subjects|"
    r"treatment protocol|clinical evaluation|results|discussion|"
    r"conclusions?|references)[ \t]*$"
)


def split_sections(
    page_text: str,
    initial_section: str = "Unlabelled",
) -> list[tuple[str, str]]:
    headings = list(HEADING_PATTERN.finditer(page_text))

    if not headings:
        return [(initial_section, page_text)]

    sections = []

    if page_text[:headings[0].start()].strip():
        sections.append(
            (initial_section, page_text[:headings[0].start()])
        )

    for index, heading in enumerate(headings):
        end = (
            headings[index + 1].start()
            if index + 1 < len(headings)
            else len(page_text)
        )
        sections.append(
            (heading.group(1), page_text[heading.end():end])
        )

    return sections


def chunk_pages_by_section(
    pages: list[dict],
    chunk_size: int = 1800,
    overlap: int = 200,
) -> list[dict]:
    if chunk_size <= 0 or not 0 <= overlap < chunk_size:
        raise ValueError("Overlap must be smaller than chunk size")

    chunks = []
    current_section = "Unlabelled"
    current_source = None

    for page in pages:
        # Start fresh when processing a different document.
        if page["source"] != current_source:
            current_section = "Unlabelled"
            current_source = page["source"]

        chunk_number = 1

        for heading, section_text in split_sections(
            page["text"],
            initial_section=current_section,
        ):
            # Remember the heading even if its text is empty.
            current_section = heading
            text = " ".join(section_text.split())
            if not text:
                continue

            start = 0
            while start < len(text):
                end = min(start + chunk_size, len(text))

                chunks.append({
                    "text": f"{heading}\n{text[start:end]}",
                    "source": page["source"],
                    "page": page["page"],
                    "section": heading,
                    "chunk_number": chunk_number,
                })

                chunk_number += 1
                if end == len(text):
                    break
                start = end - overlap

    return chunks


if __name__ == "__main__":
    chunks = chunk_pages_by_section(load_pdf("data/papers/sample.pdf"))

    for chunk in chunks:
        if chunk["page"] == 2 and chunk["section"].lower() == "treatment protocol":
            print("Section:", chunk["section"])
            print("Length:", len(chunk["text"]))
            print("Contains C-PDT timing:", "3 h" in chunk["text"])
            print("Contains M-PDT timing:", "0.5 h" in chunk["text"])
            print(chunk["text"][:250])