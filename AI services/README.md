# AI services

LOOP-MIND's Applied AI layer — LangChain agents, RAG, and function-calling
tools. See `spec.md` §"FINAL BUILD TECHNOLOGY & AI SPECIFICATION" and
`phase.md` §"EXACT AI AGENT BUILD TIMING".

**Exactly 12 agents, built only when their phase arrives — never earlier:**

| Phase | Agents |
| --- | --- |
| 06 | Company Intelligence, Student Skill Analysis, Placement Readiness, Skill-Gap Analysis, Preparation Plan, What-If Analysis |
| 13 | Resume Parser, Embedding, Matching, Shortlisting |
| 15 | Interview, Email |

| Directory | Purpose |
| --- | --- |
| `agents/` | The 12 individual agent implementations |
| `multi_agent/` | The 2 multi-agent systems (Student Intelligence, AI Recruitment) that compose the agents above |
| `rag/` | Retrieval pipeline over Qdrant (company knowledge, job requirements, evidence, outcomes, etc.) |
| `tools/` | Function-calling tools agents are allowed to invoke |
| `function_calling/` | Function/tool-calling schema + dispatch glue |
| `embeddings/` | Sentence-Transformers embedding helpers used before writing to Qdrant |
| `resume_parser/`, `matching/`, `shortlisting/`, `interview/`, `email/` | Supporting logic for their respective recruitment-side agents |

Dependencies: see `requirements.txt` (LangChain, Qdrant client,
Sentence-Transformers). Do not add MCP, additional agent frameworks, or a
second vector database — see `phase.md` §37 "Non-Negotiable Implementation
Principles".
