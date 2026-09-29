from dotenv import load_dotenv
from google import genai
from google.genai import types


def rewrite_query(question: str, paper_title: str = "") -> str:
    load_dotenv()
    client = genai.Client()

    prompt = f"""Turn the question into ONE search query for locating
a passage in a scientific paper.

Rules:
- Preserve the named technique and any comparison groups.
- If the question asks HOW a method was performed, include concrete
  procedure terms relevant to that technique: materials, preparation,
  timing, dose, equipment, exposure, or measurement settings.
- Prefer terms likely to appear under "Materials and Methods" or
  "Treatment protocol".
- Do not add "results" or "outcomes" to a methods question.
- Do not invent numerical values, study findings, or an answer.
- Return only one line of search terms.

Example:
Question: How was ultrasound imaging performed?
Search: ultrasound imaging acquisition protocol transducer settings
frequency scan duration

Paper title: {paper_title}
Question: {question}
Search:"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0),
    )

    rewritten = (response.text or "").strip()
    return rewritten.splitlines()[0].strip() if rewritten else question


if __name__ == "__main__":
    questions = [
        "How was modified photodynamic therapy performed in the study?",
        "How did the modified and conventional treatment protocols differ?",
    ]
    for question in questions:
        print(f"Original:  {question}")
        print(f"Search:    {rewrite_query(question)}\n")