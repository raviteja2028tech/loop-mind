"""Multi-Agent System 2 — AI Recruitment.

phase.md Phase 13:

    Resume Parser Agent
              |
    Embedding Agent
              |
    Matching Agent
              |
    Shortlisting Agent
              |
    Human Approval        (Phase 14 — recruiter action, not part of this pipeline)
              |
    Interview Agent       (Phase 15)
              |
    Email Agent           (Phase 15)

Composed as a genuine LangChain `RunnableSequence` over a shared state
dict, matching Multi-Agent System 1's pattern (student_placement_
intelligence.py). Only Agents 7-10 run automatically; Human Approval,
Interview and Email are later phases' recruiter-triggered stages,
represented on the workflow visualization as their defined "pending"
state until those phases exist.
"""

from agents.embedding_agent import EmbeddingAgent
from agents.matching_agent import MatchingAgent
from agents.resume_parser_agent import ResumeParserAgent
from agents.shortlisting_agent import ShortlistingAgent
from langchain_core.runnables import RunnableLambda
from qdrant_client import QdrantClient


def _build_pipeline(qdrant: QdrantClient):
    resume_agent = ResumeParserAgent()
    embedding_agent = EmbeddingAgent()
    matching_agent = MatchingAgent()
    shortlisting_agent = ShortlistingAgent()

    step_resume = RunnableLambda(
        lambda state: {**state, "parsed_resume": resume_agent.run(state["candidate"])}
    )
    step_embedding = RunnableLambda(
        lambda state: {
            **state,
            "embedding": embedding_agent.run(
                qdrant, state["application_id"], state["parsed_resume"]
            ),
        }
    )
    step_matching = RunnableLambda(
        lambda state: {
            **state,
            "matching": matching_agent.run(
                qdrant,
                state["job_id"],
                state["job"],
                state["parsed_resume"],
                state["embedding"]["vector"],
            ),
        }
    )
    step_shortlisting = RunnableLambda(
        lambda state: {**state, "shortlisting": shortlisting_agent.run(state["matching"])}
    )

    return step_resume | step_embedding | step_matching | step_shortlisting


def run_recruitment_pipeline(
    qdrant: QdrantClient,
    *,
    application_id: int,
    candidate: dict,
    job_id: int,
    job: dict,
) -> dict:
    """Runs Agents 7-10 in sequence. Returns the accumulated state dict
    containing `parsed_resume`, `embedding`, `matching`, and
    `shortlisting`."""
    pipeline = _build_pipeline(qdrant)
    return pipeline.invoke(
        {
            "application_id": application_id,
            "candidate": candidate,
            "job_id": job_id,
            "job": job,
        }
    )
