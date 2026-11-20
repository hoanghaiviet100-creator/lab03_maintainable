# Lab 6 — Báo cáo so sánh ba luồng xử lý và đánh giá RAG

## 1. Mốc 1: Đánh giá chuẩn Part F (20 câu hỏi gốc)

Chạy lệnh: `python eval/compare_paths.py` (với 20 câu gốc ban đầu).

```text
path                correct  abstain ok  p50 ms  max ms
deterministic          7/20       5/5     0.0     0.4   fails: E01 E02 E05 E06 E07 E08 E09 E10 E11 E12 E13 E14 E15
retrieval             16/20       4/5     0.0     0.1   fails: E13 E14 E15 E19
llm (stub)            16/20       4/5     0.1     0.3   fails: E13 E14 E15 E19
```

### Bảng phân tích chi tiết

| Path | Correct /20 | Abstain correct /5 | p50 latency | Controllability (1–5) | Main failure mode |
|---|:---:|:---:|:---:|:---:|---|
| **deterministic** | 7/20 | 5/5 | 0.0 ms | 5/5 | Không xử lý được ngôn ngữ tự nhiên; chỉ trả lời được học phí và tra cứu phòng ban theo từ khóa cứng (thất bại 13 câu quy chế). |
| **retrieval (BM25)** | 16/20 | 4/5 | 0.0 ms | 4/5 | Lệch từ khóa/hình thái từ (E13 từ đồng nghĩa "due" vs "paid by", E14 số nhiều "credits" vs "credit"); trích dẫn nguyên văn thô. |
| **llm (stub)** | 16/20 | 4/5 | 0.1 ms | 4/5 | Phụ thuộc hoàn toàn vào kết quả tìm kiếm; câu hỏi mơ hồ (E19) bị trích đoạn quy chế thi nhầm chủ đề thay vì từ chối. |

### Nhận xét 3 câu (Part F Reflection)
1. **Lựa chọn luồng:** Đối với các câu hỏi về sổ tay sinh viên và quy chế học vụ, em sẽ chọn triển khai **luồng kết hợp RAG (Retrieval + LLM có Grounding Check)** vì luồng này vừa tận dụng được khả năng diễn đạt tự nhiên, thân thiện của AI, vừa đảm bảo tính kỷ luật và chính xác tuyệt đối nhờ lớp kiểm duyệt nguồn trích dẫn từ code.
2. **Lý do lựa chọn:** Mặc dù luồng `retrieval` thuần túy đạt độ chính xác tương đương (16/20) với độ trễ cực thấp, nhưng việc chỉ trích nguyên văn các đoạn văn bản Markdown thô khiến trải nghiệm sinh viên bị cứng nhắc và khó hiểu khi gặp các điều khoản phức tạp.
3. **Lỗi ưu tiên sửa trước:** Trong 4 ca lỗi điển hình (`E13`, `E14`, `E15`, `E19`), em sẽ ưu tiên khắc phục lỗi **`E14` ("credits" vs "credit")** trước bằng kỹ thuật cắt tỉa từ (*stemming*) vì đây là lỗi biến đổi hình thái số nhiều rất phổ biến trong tiếng Anh, có thể sửa triệt để và an toàn bằng thuật toán chuẩn hóa từ mà không gây rủi ro ảo giác.

---

## 2. Mốc 2: Đánh giá sau khi bổ sung bài tập về nhà H1 (25 câu hỏi)

Sau khi merge PR của TV6 (`eval/cases.jsonl` có thêm 5 câu: E21, E22, E23, E24, E25).

```text
path                correct  abstain ok  p50 ms  max ms
deterministic          9/25       7/7     0.0     0.5   fails: E01 E02 E05 E06 E07 E08 E09 E10 E11 E12 E13 E14 E15 E21 E22 E23
retrieval             19/25       6/7     0.0     0.1   fails: E13 E14 E15 E19 E21 E23
llm (stub)            19/25       6/7     0.1     0.4   fails: E13 E14 E15 E19 E21 E23
```

### Nhận xét bổ sung cho H1:
- **Câu đúng mới:** Câu E22 (hỏi hạn mức tín chỉ tối đa - `H26#6.1`) và 2 câu từ chối E24 (hỏi thời tiết), E25 (hỏi điểm sinh viên khác vi phạm quyền riêng tư) đều được hệ thống nhận diện chính xác và từ chối an toàn (đạt 6/7 câu abstain).
- **Giải thích ca thất bại mới (E21, E23):** 
  - `E21` (*"how much is the regular tuition fee per credit"*): Câu hỏi chứa từ "tuition fee" và "credit" nên bị chia điểm giữa chunk học phí `F26#1` và các điều khoản tín chỉ khác, đồng thời router chưa bắt chính xác intent học phí dạng mô tả.
  - `E23` (*"how many books can I borrow from the library at once"*): Từ khóa "library" khiến router nhầm sang việc tra cứu vị trí phòng ban thư viện thay vì tìm quy định mượn sách.

---

## 3. Mốc 3: Đánh giá sau khi tích hợp Bonus H3 (Stemming chữ "s" cuối từ)

Sau khi merge PR của TV5 (`src/assistant_core/rag/index.py` cắt đuôi "s" cho từ > 4 ký tự):

```text
path                correct  abstain ok  p50 ms  max ms
deterministic          9/25       7/7     0.0     0.3   fails: E01 E02 E05 E06 E07 E08 E09 E10 E11 E12 E13 E14 E15 E21 E22 E23
retrieval             18/25       5/7     0.0     0.1   fails: E13 E14 E15 E19 E20 E21 E23
llm (stub)            18/25       5/7     0.1     0.4   fails: E13 E14 E15 E19 E20 E21 E23
```

### Phân tích hiện tượng thú vị của H3 (Does E14 pass? Did anything else change?):
1. **Đối với câu `E14` ("can I take 32 credits"):**
   - Trước khi sửa: Chunk `H26#6.1` hoàn toàn không xuất hiện trong kết quả tìm kiếm do từ `credits` không khớp với `credit`.
   - Sau khi sửa: Từ `credits` được chuyển thành `credit`, giúp chunk `H26#6.1` xuất hiện trở lại trong danh sách kết quả (`hits = [H26#7.2, H26#6.1, ...]`). Tuy nhiên, do câu hỏi có từ `"take"` (chỉ xuất hiện duy nhất 1 lần trong toàn bộ kho dữ liệu tại điều khoản vắng thi `H26#7.2`), công thức BM25 gán trọng số nghịch đảo tần suất (IDF) của từ `"take"` rất cao, khiến `H26#7.2` xếp hạng điểm cao hơn `H26#6.1`.
2. **Ảnh hưởng lan tỏa (Side-effect) lên câu khác:**
   - Việc cắt đuôi "s" khiến từ `"exams"` trong câu `E20` ("tell me about exams") bị rút gọn thành `"exam"`. Điều này khiến `E20` bất ngờ vượt qua ngưỡng điểm `min_score = 2.0` và khớp nhầm vào điều khoản vắng thi `H26#7.2`, làm tỷ lệ từ chối giảm từ 6/7 xuống 5/7.
   - **Bài học kinh nghiệm:** Cắt đuôi từ theo luật cứng (rule-based stemming) có thể cải thiện độ bao phủ từ vựng nhưng cũng làm tăng độ nhiễu cho các câu hỏi ngắn hoặc mơ hồ.

---

## 4. Bài tập về nhà H2: Reflection — Giải thích RAG (Đúng 5 dòng)

1. RAG (Retrieval-Augmented Generation) hoạt động tương tự như một kỳ thi mở tài liệu (open-book exam): mô hình AI không phải "học vẹt" và cố nhớ hàng nghìn trang quy chế từ trước, mà mỗi khi có câu hỏi, hệ thống sẽ mở đúng trang tài liệu quy chế nhà trường ra cho AI đọc trước rồi mới trả lời.
2. Ngược lại, việc dùng mô hình LLM thuần túy giống như đi thi đóng tài liệu (closed-book exam), hoàn toàn dựa vào trí nhớ huấn luyện cũ nên rất dễ nhớ nhầm hoặc tự "bịa chuyện" (hallucination) khi gặp các câu hỏi chi tiết về quy định học vụ.
3. Điểm an toàn quan trọng mà mã nguồn của chúng ta kiểm soát nhưng bản thân mô hình AI không tự làm được là bước kiểm tra căn cứ (grounding check): code chủ động chặn câu trả lời nếu nguồn trích dẫn không khớp với tài liệu truy xuất, hoặc dừng ngay lập tức khi không tìm thấy thông tin đủ tin cậy.
4. Điều này giúp ngăn chặn hoàn toàn việc AI tự bịa ra điều khoản giả mạo hay đưa ra nguồn tham chiếu không có thật cho sinh viên.
5. Nhờ lớp bảo vệ độc lập này của code, hệ thống trợ lý học tập vừa tận dụng được khả năng diễn đạt thông minh của AI, vừa đảm bảo tính kỷ luật và chính xác tuyệt đối của văn bản pháp lý trường học.

---

## 5. Bonus: Thử nghiệm Local LLM với Ollama (Trích xuất từ `docs/lab6/ollama_notes.md`)

- **Mô hình thử nghiệm:** `qwen2.5-coder:14b` / `llama3.2` chạy qua Ollama cục bộ.
- **Quan sát chính:**
  - **Câu luận văn ("can I register my thesis with 118 credits"):** Mô hình cục bộ có khả năng suy luận logic xuất sắc, hiểu rằng 118 < 120 nên trả lời thẳng thắn *"No, you cannot register your thesis with 118 credits. You need at least 120 accumulated credits"* kèm trích dẫn chính xác `H26#5.3`. Trong khi đó `StubLLM` chỉ trích dẫn lại nguyên văn câu đầu tiên.
  - **Câu mơ hồ E19 ("is the final exam open-book"):** Mô hình thật nhận biết tài liệu không nhắc đến hình thức thi mở sách nên chủ động trả về `abstain: true` ("I don't know"), khắc phục triệt để điểm yếu trích dẫn lạc đề của `StubLLM`.
  - **Độ trễ:** `StubLLM` chạy trong 0.1 ms; Ollama mất từ 5.0 đến 15.8 giây (do phải nạp mô hình vào VRAM và tính toán trọng số cục bộ).
