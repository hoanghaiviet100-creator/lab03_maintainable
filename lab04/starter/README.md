# Study Assistant — backend (Lab 4 reference)

## Setup
```
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt && pip install -e .
cp .env.example .env
```
## Run the API
```
uvicorn assistant_api.main:create_app --factory --reload
```
Open http://127.0.0.1:8000/docs for the interactive OpenAPI documentation.

## API contract (v1)
| Method | Path | Body | Success | Errors |
|---|---|---|---|---|
| GET | `/health` | — | 200 `{"status":"ok","version":...}` | — |
| POST | `/v1/chat` | `{"message": str 1–2000, "session_id": str}` | 200 `{answer, intent, sources[], degraded, request_id}` | 422 invalid, 429 rate limit |
| POST | `/v1/feedback` | `{"request_id": str, "rating": -1/0/1, "comment"?: str ≤500}` | 201 feedback with `id`, `created_at` | 422 |
| GET | `/v1/feedback` | header `X-API-Key` | 200 list | 401 |
| GET | `/v1/weather` | — | 200 `{temperature_c, wind_kmh, description, observed_at, stale}` | 503 upstream down |
| GET | `/v1/offices` | — | 200 `[{name, room, hours}, ...]`, sorted by name | — |

All errors use one shape: `{"error": {"code": "...", "message": "..."}}`.

## Tests
```
pytest -q                          # unit + API tests (external API mocked)
python -m ruff check .
bash api-tests/curl_tests.sh       # manual tests against a running server
```
Postman / Bruno: import `api-tests/study-assistant.postman_collection.json`.

Run these commands from `lab04/starter`. Set `API_ADMIN_KEY` in the server environment
and the curl environment to the same value for the authenticated feedback check.
`POST /v1/chat` allows `RATE_LIMIT_PER_MIN` requests per client in a rolling minute
(default: 30); further requests return 429 with `error.code = "too_many_requests"`.

From the repository root, also run the warm-up and the unchanged Week 3 tests:
```
python -m pytest -q -o pythonpath=lab04/practice lab04/practice
python -m pytest -q -c lab04/starter/pyproject.toml Refactor_onclass_exercise/tests
```
The second command runs the team's Week 3 tests against the Lab 4 core, including
the existing HELP behavior. Week 3 source and test files are preserved.

## H2 — Reflection

Ở Lab 3, `service.handle()` được gọi trực tiếp từ chương trình Python và trả về một đối tượng Python.<br>
Ở Lab 4, client gửi JSON đến `POST /v1/chat` qua HTTP rồi nhận JSON cùng mã trạng thái.<br>
FastAPI kiểm tra dữ liệu đầu vào trước khi chuyển yêu cầu đến cùng phần xử lý `service.handle()`.<br>
HTTP giúp giao diện web, ứng dụng điện thoại hoặc chương trình viết bằng ngôn ngữ khác cùng dùng dịch vụ.<br>
Nhóm có thể phát triển giao diện và backend riêng, miễn là thống nhất cấu trúc request, response và cách báo lỗi.
