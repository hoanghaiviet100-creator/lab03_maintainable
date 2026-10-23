from assistant_core.models import Intent

GREETINGS = frozenset({"hi", "hello", "hey", "xin chao"})
HELP_KEYWORDS = frozenset({"help", "what can you do", "tro giup", "huong dan", "support"})

def route(text: str, office_names: set[str]) -> Intent:
    t = text.lower().strip().rstrip("?!.")
    if t in GREETINGS:
        return Intent.GREETING
    if any(k in t for k in HELP_KEYWORDS):
        return Intent.HELP
    if "fee" in t or "tuition" in t:
        return Intent.FEE
    if any(name in t for name in office_names):
        return Intent.OFFICE
    return Intent.RULE
