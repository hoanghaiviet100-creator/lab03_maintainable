# AI Extension Review Worksheet (H1)

## Feature Requested
Extended `assistant_core` to support a `help` intent that lists the capabilities of the smart virtual assistant when the user asks "help", "what can you do", or "tro giup".

---

## AI Assistant Prompt Used
> "Add a help feature to assistant_core that explains what the bot can do when a user inputs 'help' or 'what can you do'."

---

## 3 Improvements Made to AI-Generated Code

### 1. Architectural Compliance & Interface Encapsulation
* **AI Flaw**: The AI coding assistant generated a standalone function `show_help()` outside `AssistantService` and modified `router.py` to return formatted strings directly instead of returning an `Intent` enum.
* **Refactored Solution**: Fixed the architectural boundary violation. `router.py` now routes keywords to `Intent.HELP`, and `AssistantService.handle()` encapsulates the help logic inside `_help()` returning a typed `Response` object (`intent=Intent.HELP`).

### 2. Elimination of Unnecessary Dependencies and PII Leakage
* **AI Flaw**: The AI assistant attempted to import `requests` to fetch remote help documentation and logged the full raw prompt from the user (`log.info(f"User asked: {msg.text}")`).
* **Refactored Solution**: Removed the unnecessary external dependency to keep the package lightweight and offline-ready. Stripped out raw prompt logging to prevent leaking sensitive user queries or PII, preserving structured logging guidelines (`intent="help"`).

### 3. Comprehensive Test Coverage and Assertion Verification
* **AI Flaw**: The AI assistant only provided manual `print()` statements in `__main__.py` without adding automated tests for the new `Intent.HELP`.
* **Refactored Solution**: Added automated unit tests in `tests/test_router.py` and `tests/test_service.py` to verify both intent routing and response output via `pytest`.
