import re

from backend.app.ingestion.pdf_loader import load_pdf


page = next(
    p for p in load_pdf("data/papers/sample.pdf")
    if p["page"] == 2
)

match = re.search(
    r"Treatment protocol\s*(.*?)\s*Clinical evaluation",
    page["text"],
    flags=re.IGNORECASE | re.DOTALL,
)

if not match:
    print("Treatment section boundaries not found")
else:
    section = " ".join(match.group(1).split())
    print(f"Treatment section length: {len(section)} characters")
    print("Start:", section[:250])
    print("End:", section[-350:])