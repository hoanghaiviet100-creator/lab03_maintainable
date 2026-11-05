# Lab 4 — API contract worksheet

Fill in one row per endpoint **before** you code it.

| Method | Path | Request body / params | Success (code + body) | Errors (code + error.code) | Who calls it |
|---|---|---|---|---|---|
| GET | /health | — | 200 {status, version} | — | ops, UI |
| POST | /v1/chat | JSON message (1–2000 chars), optional session_id (max 64, default anonymous) | 200 {answer, intent, sources[], degraded, request_id} | 422 invalid_request; 429 too_many_requests | UI, tests |
| POST | /v1/feedback | JSON request_id (1–64 chars), rating (-1/0/1), optional comment (max 500) | 201 {request_id, rating, comment, id, created_at} | 422 invalid_request | UI |
| GET | /v1/feedback | header X-API-Key | 200 list of feedback | 401 missing_or_invalid_api_key | staff dashboard |
| GET | /v1/weather | — | 200 {temperature_c, wind_kmh, description, observed_at, stale} | 503 weather_service_unavailable | UI |
| GET | /v1/offices | — | 200 [{name, room, hours}, ...], sorted by name | — | UI, tests |

Questions:
1. Which fields are required, and what are their limits?
2. What does the UI show for each error code?
3. What changes would force a `/v2`?

1. Chat requires `message`. Feedback requires `request_id` and `rating`.
   Field limits are listed above; the other endpoints have no request body.
2. For 422, show the field error so the user can correct the input. For 401,
   ask staff to check their key. For 429, ask the user to wait for the rolling
   minute limit to clear. For 503, show that weather is temporarily unavailable.
   When weather has `stale: true`, label the cached observation as outdated.
3. Removing or renaming public fields, changing their types, or changing the
   meaning of an existing response would require a new API version.

All errors use `{"error": {"code": "...", "message": "..."}}`.
Unknown paths return 404 `not_found`; unsupported methods return 405 `method_not_allowed`.
