import json
from pathlib import Path

from backend.app.retrieval.retriever import retrieve_chunks


COLLECTION = "research_papers_section_v1"
TOP_K = 5

CASES = [
    {
        "id": "paper1_procedure",
        "source": "sample.pdf",
        "question": "How did the C-PDT and M-PDT treatment protocols differ?",
        "answerable": True,
        "expected_evidence": [
            "Both used 10% ALA cream",
            "C-PDT: incubation 3 hours; irradiation 144 J/cm² for 60 minutes",
            "M-PDT: incubation 0.5 hours; irradiation 288 J/cm² for 120 minutes",
            "Three treatments spaced two weeks apart",
        ],
        "evidence_pages": [2],
    },
    {
        "id": "paper1_selection",
        "source": "sample.pdf",
        "question": "What were the patient inclusion criteria?",
        "answerable": True,
        "expected_evidence": [
            "Either sex, aged over 18 years",
            "Facial actinic keratosis, Olsen grade I–III",
            "More than six lesions",
        ],
        "evidence_pages": [2],
    },
    {
        "id": "paper1_outcomes",
        "source": "sample.pdf",
        "question": (
            "What were the total lesion clearance rates one month "
            "after three sessions, and did the treatments differ significantly?"
        ),
        "answerable": True,
        "expected_evidence": [
            "C-PDT: 138/155 lesions cleared, 89.0%",
            "M-PDT: 185/202 lesions cleared, 91.6%",
            "Between-treatment p = 0.416; no significant difference",
        ],
        "evidence_pages": [4],
    },
    {
        "id": "paper1_unanswerable",
        "source": "sample.pdf",
        "question": "What were the treatment outcomes at five years?",
        "answerable": False,
        "expected_evidence": [
            "Five-year outcomes cannot be established from provided evidence",
        ],
        "evidence_pages": [],
    },
    {
        "id": "paper2_procedure",
        "source": "paper2.pdf",
        "question": "How was photodynamic therapy performed in the study?",
        "answerable": True,
        "expected_evidence": [
            "Three sessions at 14-day intervals",
            "30% urea nightly for one week before first irradiation",
            "20% ALA with 2% DMSO under occlusion four hours before light",
            "Green: 540 ± 15 nm, 62.5 J/cm²",
            "Red: 630 ± 15 nm, 125 J/cm²",
            "Both: 86 mW/cm²; three minutes irradiation, one-minute pause",
        ],
        "evidence_pages": [2],
    },
    {
        "id": "paper2_selection",
        "source": "paper2.pdf",
        "question": "How were patients selected for the study?",
        "answerable": True,
        "expected_evidence": [
            "Head AK lesions of grade I or II",
            "Histologically verified diagnoses",
            "3 × 3 cm areas with at least two AKs, minimum diameter 0.5 cm",
            "Enrolled sample: 20 patients aged 61–84",
        ],
        "evidence_pages": [2],
    },
    {
        "id": "paper2_outcomes",
        "source": "paper2.pdf",
        "question": "What were the main treatment outcomes at nine months?",
        "answerable": True,
        "expected_evidence": [
            "Red light: 91.67% complete remission",
            "Green light: 86.67% complete remission",
            "Four new AK lesions in green-light areas",
            "No statistically significant difference in treatment outcomes",
        ],
        "evidence_pages": [2, 3],
    },
    {
        "id": "paper2_unanswerable",
        "source": "paper2.pdf",
        "question": "What were the treatment outcomes at five years?",
        "answerable": False,
        "expected_evidence": [
            "Five-year outcomes cannot be established from provided evidence",
        ],
        "evidence_pages": [],
    },
]


def main():
    report = {
        "method": "dense",
        "collection": COLLECTION,
        "top_k": TOP_K,
        "section_filter": None,
        "cases": [],
    }

    for case in CASES:
        results = retrieve_chunks(
            case["question"],
            source=case["source"],
            limit=TOP_K,
            collection_name=COLLECTION,
            section_type=None,
        )

        report["cases"].append({
            **case,
            "retrieved_chunks": results,
            "review": {
                "evidence_coverage": "pending",
                "first_relevant_rank": None,
                "notes": "",
            },
        })

        print(f"\nCASE: {case['id']} | SOURCE: {case['source']}")
        print(f"QUESTION: {case['question']}")

        for evidence in case["expected_evidence"]:
            print(f"EXPECTED: {evidence}")

        if not results:
            print("NO RESULTS: check whether this source is indexed.")

        for rank, result in enumerate(results, start=1):
            print(
                f"\nRank {rank} | Page {result['page']} | "
                f"Section: {result.get('section', 'Unknown')} | "
                f"Score: {result['score']:.3f}"
            )
            print(result["text"])

    project_root = Path(__file__).resolve().parents[2]
    output_path = project_root / "data/evaluation/dense_baseline.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )
    print(f"\nSaved: {output_path}")


if __name__ == "__main__":
    main()