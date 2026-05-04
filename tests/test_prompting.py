from gcp_vertex_rag_blueprint.models import RetrievedChunk
from gcp_vertex_rag_blueprint.prompting import build_grounded_prompt


def _chunks():
    return [
        RetrievedChunk(
            id="1",
            title="Runbook",
            text="Scale pods on CPU > 70%.",
            source_uri="gs://docs/runbook.md",
            score=0.95,
        ),
        RetrievedChunk(
            id="2",
            title="SLO",
            text="p95 latency target is 1200ms.",
            source_uri="gs://docs/slo.md",
            score=0.88,
        ),
    ]


def test_prompt_contains_query_and_context():
    prompt = build_grounded_prompt("What is our p95 target?", _chunks())
    assert "What is our p95 target?" in prompt
    assert "[1] Runbook" in prompt
    assert "[2] SLO" in prompt


def test_prompt_demands_grounding():
    prompt = build_grounded_prompt("Q", _chunks())
    assert "Use ONLY the provided context" in prompt
    assert "do not fabricate" in prompt
