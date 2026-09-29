import re


METHOD_TERMS = re.compile(
    r"\b(methods?|protocols?|procedures?|performed|administered)\b",
    flags=re.IGNORECASE,
)


def route_section_type(question: str) -> str | None:
    if METHOD_TERMS.search(question):
        return "methods"
    return None


if __name__ == "__main__":
    questions = [
        "How was modified photodynamic therapy performed in the study?",
        "How did the modified and conventional treatment protocols differ?",
        "What was the lesion clearance rate?",
    ]
    for question in questions:
        print(f"{question} -> {route_section_type(question)}")