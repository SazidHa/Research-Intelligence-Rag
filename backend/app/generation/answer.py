from dotenv import load_dotenv
from google import genai
from google.genai import types

from backend.app.core.qdrant import COLLECTION_NAME
from backend.app.retrieval.context import build_context
from backend.app.ingestion.ingest_sections import EXPERIMENT_COLLECTION
from backend.app.retrieval.section_router import route_section_type

def answer_question(
    question: str,
    source: str,
    retrieval_query: str | None = None,
    collection_name: str = COLLECTION_NAME,
    section_type: str | None = None,
) -> str:
    selected_section = section_type
    if selected_section is None and collection_name == EXPERIMENT_COLLECTION:
        selected_section = route_section_type(question)
    context = build_context(
        retrieval_query or question,
        source=source,
        limit=5,
        collection_name=collection_name,
        section_type=selected_section,
    )

    if context == "No relevant passages found.":
        return context

    load_dotenv()
    client = genai.Client()

    prompt = f"""Question:
{question}

Passages from the research paper:
{context}

Answer using only these passages. Describe this study's own procedure,
not protocols mentioned from other studies. Cite each factual claim with
its filename and page number, for example [sample.pdf, p. 2].
If the passages lack an answer, say what cannot be determined.
Do not invent details."""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.1),
    )

    return response.text or "The model returned no text."


if __name__ == "__main__":
    question = "How was modified photodynamic therapy performed in the study?"
    print(answer_question(
        question,
        source="sample.pdf",
        collection_name="research_papers_section_v1",
        section_type="methods",
    ))