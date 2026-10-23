from assistant_core.models import Intent

# Tập hợp các từ chào hỏi phổ biến (dùng frozenset để tối ưu tốc độ tra cứu)
GREETINGS = frozenset({"hi", "hello", "hey", "xin chao", "chao", "chào", "xin chào"})


def route(text: str, office_names: set[str]) -> Intent:
    """Phân loại ý định (Intent) của người dùng dựa trên câu văn nhập vào.

    Args:
        text (str): Câu thoại/câu hỏi từ người dùng.
        office_names (set[str]): Tập hợp tên các phòng ban đã chuẩn hóa (chữ thường).

    Returns:
        Intent: Ý định tương ứng (GREETING, FEE, OFFICE, hoặc RULE).
    """
    # Chuẩn hóa chuỗi: chuyển thành chữ thường, xóa khoảng trắng thừa và ký tự đặc biệt ở cuối
    t = text.lower().strip().rstrip("?!.")

    # 1. Kiểm tra chào hỏi
    if t in GREETINGS:
        return Intent.GREETING

    # 2. Kiểm tra từ khóa hỏi về học phí / lệ phí
    if "fee" in t or "tuition" in t or "học phí" in t or "hoc phi" in t:
        return Intent.FEE

    # 3. Kiểm tra xem có chứa tên phòng ban nào không
    if any(name in t for name in office_names):
        return Intent.OFFICE

    # 4. Trường hợp mặc định: Tra cứu quy định/sổ tay (Rule)
    return Intent.RULE