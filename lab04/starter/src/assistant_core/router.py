"""Decide which capability handles a message. Rules first — no AI needed."""

from __future__ import annotations

import re

from assistant_core.models import Intent

GREETINGS = frozenset({"hi", "hello", "hey", "xin chao"})
HELP_KEYWORDS = frozenset({"help", "what can you do", "tro giup", "huong dan", "support"})
FEE_WORDS = ("fee", "tuition")


def route(text: str, office_names: set[str]) -> Intent:
    t = text.lower().strip().rstrip("?!.")
    if t in GREETINGS:
        return Intent.GREETING
    if any(re.search(rf"\b{re.escape(keyword)}\b", t) for keyword in HELP_KEYWORDS):
        return Intent.HELP
    if any(w in t for w in FEE_WORDS):
        return Intent.FEE
    if any(name in t for name in office_names):
        return Intent.OFFICE
    return Intent.RULE
