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

All errors use one shape: `{"error": {"code": "...", "message": "..."}}`.

## Tests
```
pytest -q                          # unit + API tests (external API mocked)
bash api-tests/curl_tests.sh       # manual tests against a running server
```
Postman / Bruno: import `api-tests/study-assistant.postman_collection.json`.

## D–T4 — Weather API (Bảo Hưng)

`GET /v1/weather` calls the provided `WeatherClient.current()`. The existing client
handles timeout, retries and cached fallback; if it raises `ExternalServiceError`,
the endpoint returns HTTP 503 with `error.code = "weather_service_unavailable"`.

Run the existing weather tests from `lab04/starter`:
```
python -m pytest -q tests/test_api.py -k weather
python -m ruff check .
```
The other API tasks and their tests are assigned to the other team members.
The full test suite and Ruff still report unfinished starter tasks outside T4
until those changes are integrated.

## H2 — Reflection

Ở Lab 3, `service.handle()` được gọi trực tiếp từ chương trình Python và trả về một đối tượng Python.<br>
Ở Lab 4, client gửi JSON đến `POST /v1/chat` qua HTTP rồi nhận JSON cùng mã trạng thái.<br>
FastAPI kiểm tra dữ liệu đầu vào trước khi chuyển yêu cầu đến cùng phần xử lý `service.handle()`.<br>
HTTP giúp giao diện web, ứng dụng điện thoại hoặc chương trình viết bằng ngôn ngữ khác cùng dùng dịch vụ.<br>
Nhóm có thể phát triển giao diện và backend riêng, miễn là thống nhất cấu trúc request, response và cách báo lỗi.
