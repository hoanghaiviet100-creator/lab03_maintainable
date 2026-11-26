# Lab 6 — Bonus Ollama & Part H2 Reflection Notes

## 1. Bonus Ollama: Thử nghiệm thực tế với mô hình cục bộ (Local LLM)

Môi trường kiểm thử thực tế:
- **Hệ thống:** MacBook (Apple M3, Metal GPU acceleration)
- **Local LLM Engine:** Ollama (localhost:11434)
- **Model sử dụng:** `qwen2.5-coder:14b` (được cấu hình qua `LLM_PROVIDER="ollama"` và `LLM_MODEL="qwen2.5-coder:14b"`)

---

### A. Thực thi câu hỏi luận văn: *"can I register my thesis with 118 credits"*

#### 1. Chạy với `Ollama` (`qwen2.5-coder:14b`):
- **Lệnh thực thi:**
  ```bash
  PYTHONPATH=src LLM_PROVIDER="ollama" LLM_MODEL="qwen2.5-coder:14b" LLM_TIMEOUT_S="60" .venv/bin/python -m assistant_core "can I register my thesis with 118 credits"
  ```
- **Kết quả trả về:**
  > *"No, you cannot register your thesis with 118 credits. You need at least 120 accumulated credits."*
  > `source: H26#5.3 — 5.3 Thesis registration`
- **Độ trễ (Latency):** `15,861.6 ms` (~15.8 giây cho lượt chạy đầu load model vào VRAM).
- **Độ chính xác (Accuracy):** Rất cao và thông minh. Mô hình hiểu ngữ cảnh câu hỏi (hỏi về 118 tín chỉ so với quy chế yêu cầu 120 tín chỉ), đưa ra câu trả lời trực diện ("No, you cannot..."), giải thích lý do cụ thể và trích dẫn chính xác nguồn quy chế `H26#5.3`.

#### 2. So sánh với `StubLLM`:
- **Kết quả trả về:**
  > *"According to 5.3 Thesis registration: Students may register a thesis when they have at least 120 accumulated credits and a cumulative GPA of at least 2.0."*
- **Độ trễ:** `0.4 ms`.
- **Nhận xét so sánh:**
  - `StubLLM` phản hồi gần như tức thì (< 1ms) nhưng thực chất chỉ cắt câu đầu tiên từ văn bản tìm được một cách máy móc, không suy luận được câu trả lời dạng Yes/No cho con số "118 credits".
  - `Ollama (qwen2.5-coder:14b)` chậm hơn đáng kể do phải tính toán suy luận mô hình 14B tham số trên thiết bị cục bộ, nhưng câu trả lời tự nhiên, có tư duy logic và giải quyết đúng trọng tâm câu hỏi của sinh viên.

---

### B. Thực thi câu E19: *"is the final exam open-book"*

#### 1. Chạy với `Ollama` (`qwen2.5-coder:14b`):
- **Lệnh thực thi:**
  ```bash
  PYTHONPATH=src LLM_PROVIDER="ollama" LLM_MODEL="qwen2.5-coder:14b" LLM_TIMEOUT_S="60" .venv/bin/python -m assistant_core "is the final exam open-book"
  ```
- **Kết quả trả về:**
  > *"I'm not confident I can answer that from the official documents. Please contact the Training Office (room I.101) or ask your academic advisor."*
  > `intent: unknown, degraded: false`
- **Độ trễ (Latency):** `4,994.3 ms` (~5.0 giây, nhanh hơn do model đã nằm sẵn trên RAM/VRAM).
- **Hành vi từ chối (Abstain):** **Có, mô hình biết nói "I don't know" (từ chối trả lời).** Vì trong toàn bộ tài liệu Sổ tay sinh viên (`handbook_2026.md`) không có thông tin về việc thi cuối kỳ được dùng tài liệu hay không, mô hình không tự ý bịa đặt (không hallucinate) mà chủ động trả về cờ `abstain: true`.

#### 2. So sánh với `StubLLM`:
- **Kết quả trả về của Stub:**
  > *"According to 7.2 Exam absence: Students absent from a final exam for medical reasons must submit a medical certificate to the Training Office within 3 working days."*
- **Nhược điểm nghiêm trọng của Stub:** BM25 tìm thấy chunk có từ khóa `"exam"` liên quan đến việc vắng thi vì lý do y tế (`7.2 Exam absence`). `StubLLM` ngô nghê trích dẫn đoạn này ra trả lời, dẫn đến việc trả lời hoàn toàn lạc đề so với câu hỏi thi mở sách hay đóng sách.
- **Kết luận:** Mô hình thật vượt trội hơn hẳn ở khả năng nhận biết giới hạn tri thức trong ngữ cảnh được cấp và biết từ chối trả lời (`abstain`) khi không có dữ liệu đối sánh.

---

## 2. Phần H2: Reflection — Giải thích RAG (Đúng 5 dòng)

1. RAG (Retrieval-Augmented Generation) hoạt động tương tự như một kỳ thi mở tài liệu (open-book exam): mô hình AI không phải "học vẹt" và cố nhớ hàng nghìn trang quy chế từ trước, mà mỗi khi có câu hỏi, hệ thống sẽ mở đúng trang tài liệu quy chế nhà trường ra cho AI đọc trước rồi mới trả lời.
2. Ngược lại, việc dùng mô hình LLM thuần túy giống như đi thi đóng tài liệu (closed-book exam), hoàn toàn dựa vào trí nhớ huấn luyện cũ nên rất dễ nhớ nhầm hoặc tự "bịa chuyện" (hallucination) khi gặp các câu hỏi chi tiết về quy định học vụ.
3. Điểm an toàn quan trọng mà mã nguồn của chúng ta kiểm soát nhưng bản thân mô hình AI không tự làm được là bước kiểm tra căn cứ (grounding check): code chủ động chặn câu trả lời nếu nguồn trích dẫn không khớp với tài liệu truy xuất, hoặc dừng ngay lập tức khi không tìm thấy thông tin đủ tin cậy.
4. Điều này giúp ngăn chặn hoàn toàn việc AI tự bịa ra điều khoản giả mạo hay đưa ra nguồn tham chiếu không có thật cho sinh viên.
5. Nhờ lớp bảo vệ độc lập này của code, hệ thống trợ lý học tập vừa tận dụng được khả năng diễn đạt thông minh của AI, vừa đảm bảo tính kỷ luật và chính xác tuyệt đối của văn bản pháp lý trường học.

