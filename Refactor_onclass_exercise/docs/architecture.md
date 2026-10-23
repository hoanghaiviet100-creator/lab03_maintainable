# Architecture Note - assistant_core

## 1. Module Responsibility Overview
| Module | Responsibility |
| :--- | :--- |
| `config.py` | Read and validate environment settings using Pydantic. |
| `errors.py` | Custom named exceptions for domain error handling. |
| `models.py` | Public domain models (`Message`, `Response`, `Intent`, `Source`). |
| `router.py` | Deterministic intent classification from user text. |
| `knowledge.py` | Data loading and search engines for CSV (offices) and JSON (handbook). |
| `tools.py` | Pure function calculations (tuition fees). |
| `responder.py` | AI/Template response generator abstraction behind a Protocol interface. |
| `service.py` | Central `AssistantService` orchestrator, exposing `handle(Message) -> Response`. |
| `logging_setup.py` | Structured JSON log formatter ensuring no secrets/PII leak. |
| `__main__.py` | CLI entry point. |

## 2. Service Interface
`AssistantService.handle(msg: Message) -> Response`
- **Input**: `Message(text: str, session_id: str)`
- **Output**: `Response(answer: str, intent: Intent, sources: list[Source], degraded: bool)`

## 3. Key Design Decisions
1. **Deterministic Fee Calculation**: Fees are calculated using pure Python functions in `tools.py` rather than LLM prompts, ensuring exact results and zero hallucination.
2. **Adapter Pattern for AI Providers**: LLMs sit behind a `Responder` Protocol interface. The default stub requires no API key, allowing offline testing and CI/CD pipelines.
3. **Environment-driven Configuration**: Follows 12-Factor App principles. Configuration is stored in environment variables, with `.env.example` documenting all parameters and secrets excluded from representations (`repr=False`).
