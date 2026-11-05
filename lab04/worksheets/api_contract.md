# Lab 4 — API contract worksheet

Fill in one row per endpoint **before** you code it.

| Method | Path | Request body / params | Success (code + body) | Errors (code + error.code) | Who calls it |
|---|---|---|---|---|---|
| GET | /health | — | 200 `{status, version}` | — | ops, UI |
| POST | /v1/chat | `{message: str, session_id?: str}` | 200 `{answer, intent, sources, degraded, request_id}` | 422 `invalid_request`, 429 `rate_limit_exceeded` | UI, tests |
| POST | /v1/feedback | `{request_id: str, rating: int[-1..1], comment?: str}` | 201 `{id, request_id, rating, comment, created_at}` | 422 `invalid_request` | UI |
| GET | /v1/feedback | header `X-API-Key` | 200 `[{...FeedbackOut}]` | 401 `missing_or_invalid_api_key` | staff dashboard |
| GET | /v1/weather | — | 200 `{temperature_c, wind_kmh, description, observed_at, stale}` | 503 `weather_service_unavailable` | UI |
| GET | /v1/offices | — | 200 `[{name, room, hours}]` sorted by name | — | UI, tests |

Questions:
1. Which fields are required, and what are their limits?
   - `POST /v1/chat`: `message` required, 1–2000 chars. `session_id` optional, max 64 chars.
   - `POST /v1/feedback`: `request_id` required (1–64 chars), `rating` required (−1, 0, 1), `comment` optional (max 500 chars).
   - `GET /v1/feedback`: `X-API-Key` header required.
2. What does the UI show for each error code?
   - `invalid_request` (422): Form validation error — highlight the offending field.
   - `rate_limit_exceeded` (429): "Too many requests, please wait a moment."
   - `missing_or_invalid_api_key` (401): "Unauthorized — admin access only."
   - `weather_service_unavailable` (503): "Weather data is temporarily unavailable."
3. What changes would force a `/v2`?
   - Renaming or removing existing response fields (e.g., changing `answer` → `reply`).
   - Changing `rating` from int to string enum.
   - Making previously optional fields required in a request body.
