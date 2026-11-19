# Study Assistant — Architecture Note (Labs 3–6)

## 1. Module Responsibility Overview

### Core Package (`src/assistant_core/`)
| Module | Responsibility | Depends on |
| :--- | :--- | :--- |
| `config.py` | Read and validate environment settings from `.env` using Pydantic. | `errors` |
| `errors.py` | Custom named exceptions (`AssistantError`, `ConfigError`, `DataError`, `InvalidRequest`, `ProviderError`). | — |
| `models.py` | Public domain contract (`Message`, `Response`, `Intent`, `Source`). | `pydantic` |
| `router.py` | Deterministic rule-first intent classification (`greeting`, `fee`, `office`, `rule`). | `models` |
| `knowledge.py` | Load and query `OfficeDirectory` (CSV) and `Handbook` (JSON). | `errors` |
| `tools.py` | Pure deterministic tuition calculation (`parse_credits`, `tuition`) and validated LLM tool calling (`run_tool_call`). | `errors`, `pydantic` |
| `responder.py` | `Responder` Protocol interface with `TemplateResponder` and `StubLLMResponder` (Lab 3). | `knowledge`, `errors` |
| `guard.py` | Privacy guardrail blocking requests about other students' personal data (Lab 6). | — |
| `llm.py` | `LLM` adapter (`StubLLM`, `OllamaLLM`, `OpenAICompatibleLLM`), prompt builder, structured JSON + grounding validation (Lab 6). | `errors`, `rag.index`, `pydantic`, `httpx` |
| `rag/` | Markdown knowledge-base chunker (`chunker.py`), BM25/TF-IDF/hybrid search index (`index.py`), and safe RAG orchestrator with abstain & fallback (`answerer.py`). | `llm`, `models`, `errors` |
| `service.py` | Central `AssistantService.handle(Message) -> Response` entry point and `build_service()`. | all core modules |
| `logging_setup.py` | Structured JSON logging to `stderr` without leaking secrets or PII. | — |
| `__main__.py` | Command-line interface (CLI) entry point. | `service`, `config` |

### Web API & Persistence Package (`src/assistant_api/`)
| Module | Responsibility | Depends on |
| :--- | :--- | :--- |
| `main.py` | FastAPI app factory (`create_app`), HTTP endpoints (`/health`, `/v1/chat`, `/v1/feedback`, `/v1/stats/intents`, `/v1/weather`, `/v1/offices`), uniform error handlers, admin API-key check. | `assistant_core`, `schemas`, `db`, `weather`, `ratelimit` |
| `schemas.py` | HTTP request/response Pydantic models. | `assistant_core.models`, `pydantic` |
| `db.py` | SQLModel tables (`ChatSession`, `Interaction`, `Feedback`), salted SHA-256 session hashing, and `Repository` pattern (Lab 5). | `sqlmodel`, `sqlalchemy` |
| `weather.py` | External Open-Meteo API client with timeout, retry, and stale-cache fallback (Lab 4). | `httpx` |
| `ratelimit.py` | Per-client sliding-window rate limiter returning HTTP 429 on abuse (Lab 4 Bonus). | — |

## 2. Service Interface
```text
AssistantService.handle(msg: Message) -> Response
```
- **Input:** `Message(text: 1–2000 chars, session_id)`
- **Output:** `Response(answer, intent, sources, degraded, escalate, path, confidence)`
- **Error Boundary:** Invalid input raises `pydantic.ValidationError`; startup misconfiguration raises `ConfigError` / `DataError`; provider failures never propagate to callers (automatic fallback to retrieval/template with `degraded=True`).

## 3. Key Design Decisions
1. **Deterministic Fee Calculation:** Tuition fees are always computed by pure functions in `tools.py`, never by an LLM, ensuring exact calculations and zero hallucination.
2. **Adapter Pattern for AI Providers:** Both `Responder` (Lab 3) and `LLM` (Lab 6) sit behind `Protocol` interfaces. The default offline `stub` requires no API key, keeping unit tests and CI deterministic.
3. **Environment-Driven Configuration (Twelve-Factor III):** All settings live in environment variables documented in `.env.example`; secrets use `Field(repr=False)` and `.env` is excluded from Git.
4. **Privacy by Design in Persistence (Lab 5):** The database stores only interaction metadata, salted SHA-256 hashes of `session_id`, and user feedback — never raw student messages or personal identifiers.
5. **Safe RAG with Grounding & Abstention (Lab 6):** Policy questions pass through privacy guardrails, BM25 retrieval score thresholds (abstain/escalate before calling the LLM), strict JSON schema + citation grounding checks, and automatic retrieval-only fallback on failure.
