# Lab 4 homework — design for an external service that goes down

Service chosen: **Open-Meteo Weather API**  Base URL: `https://api.open-meteo.com/v1/forecast`

| Failure | How you simulate it | What your API returns | What the user sees |
|---|---|---|---|
| timeout | `MockTransport` raises `httpx.ConnectTimeout` | 503 `{"error": {"code": "weather_service_unavailable", ...}}` | "Weather data is temporarily unavailable." |
| 500 from upstream | `MockTransport` returns `httpx.Response(500)` | 503 (after retries exhausted and no cache) | "Weather data is temporarily unavailable." |
| malformed JSON | `MockTransport` returns `httpx.Response(200, text="{}")` | 503 (KeyError caught as HTTPError-equivalent; falls through to ExternalServiceError) | "Weather data is temporarily unavailable." |
| rate limited (429) | `MockTransport` returns `httpx.Response(429)` | 503 (raise_for_status triggers HTTPStatusError → retry → ExternalServiceError) | "Weather data is temporarily unavailable." |

**Timeout value:** 3 s — fast enough to feel responsive on a campus LAN; long enough to allow for a slow satellite hop.

**Retries:** 1 — a single retry handles transient blips without noticeably delaying the user (adds at most 0.4 s back-off).

**Cache TTL:** 600 s (10 min) — weather changes slowly; a 10-minute stale reading is still useful and dramatically reduces upstream load.

## Reflection — H2

Calling `service.handle()` directly (Lab 3) works fine for a single CLI session on one machine: everything lives in the same Python process, sharing memory, so there is no network overhead, no serialisation, and no authentication needed. The moment we wrap it in `POST /v1/chat` (Lab 4), every client — a web browser, a mobile app, a teammate's script — can reach the same logic over HTTP without installing any Python code. The contract becomes a JSON schema, not a function signature, which means the frontend team can work in TypeScript, the testing team can use `curl`, and a future microservice can call the same endpoint. HTTP also gives us cross-cutting concerns for free: rate limiting (429), structured error codes, Swagger docs, and authentication headers — all without touching the core business logic in `assistant_core`. That separation between *transport* (FastAPI layer) and *domain* (service layer) is exactly why real-world teams prefer the HTTP API model: it decouples who calls the code from how the code is written.

Tests added (`tests/test_api.py`):
- `test_weather_ok` — verifies 200 and correct description from a mock upstream
- `test_weather_down_returns_503` — verifies 503 + error code when upstream is unreachable
- `test_weather_stale_cache_when_upstream_fails` — verifies stale-cache fallback behaviour
