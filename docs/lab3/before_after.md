# Before and After Maintainability Worksheet

| Question / Metric | Monolith (`assistant_monolith.py`) | Refactored (`assistant_core`) |
| :--- | :--- | :--- |
| **Places to change credit rate** | 1 constant in code (`RATE = 450000`) | 1 variable in `.env` (`CREDIT_RATE_VND`) |
| **Tests run offline and deterministically?** | No (random failures in `llm()`) | Yes (`StubLLMResponder` is deterministic) |
| **Missing `handbook.json`** | Prints message and continues silently | Raises `DataError` at startup |
| **Secret printed or logged?** | Yes (`API_KEY` printed in debug log) | No (`repr=False` on `llm_api_key`) |
| **Module-level globals** | 9 globals (3 mutable: `history`, `offices`, `handbook`) | 0 globals |
| **Bare `except:` count** | 3 instances | 0 instances (specific custom exceptions used) |
| **Longest function (lines)** | ~65 lines (`handle()`) | ~15 lines (`_rule()`, `_fee()`) |
| **Swap LLM without touching service?** | No (hardcoded in `handle()`) | Yes (Dependency Injection via `Responder`) |
