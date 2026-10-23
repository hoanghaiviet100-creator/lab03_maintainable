from assistant_core.models import Intent

GREETINGS = frozenset({"hi", "hello", "hey", "xin chao", "chao", "chào", "xin chào"})


def route(text: str, office_names: set[str]) -> Intent:
    t = text.lower().strip().rstrip("?!.")

    # 1. Chào hỏi
    if t in GREETINGS:
        return Intent.GREETING

    # 2. Học phí / Lệ phí (Bổ sung thêm "học phí" và "hoc phi")
    if "fee" in t or "tuition" in t or "học phí" in t or "hoc phi" in t:
        return Intent.FEE

    # 3. Phòng ban
    if any(name in t for name in office_names):
        return Intent.OFFICE

    # 4. Quy định / Sổ tay
    return Intent.RULE
