import json
from pathlib import Path

import httpx
from streamlit.testing.v1 import AppTest

from ui.api_client import AssistantClient, ChatResult
from ui.logic import format_sources, status_note, validate_input

APP_PATH = Path(__file__).resolve().parents[1] / "ui" / "app.py"

OK = {
    "answer": "Room B.201",
    "intent": "office",
    "sources": [{"id": "S26#1", "title": "1 Library borrowing"}],
    "degraded": False,
    "escalate": False,
    "path": "deterministic",
    "request_id": "abc123",
}


def client_with(handler) -> AssistantClient:
    return AssistantClient("http://api.test", transport=httpx.MockTransport(handler))


def test_ask_ok():
    captured = {}

    def handler(req: httpx.Request) -> httpx.Response:
        captured["path"] = req.url.path
        captured["body"] = json.loads(req.content)
        return httpx.Response(200, json=OK)

    r = client_with(handler).ask("where is the library", "s1")
    assert captured == {"path": "/v1/chat", "body": {"message": "where is the library", "session_id": "s1"}}
    assert r.ok and r.answer == "Room B.201" and r.intent == "office"
    assert r.sources == OK["sources"] and r.path == "deterministic" and r.request_id == "abc123"


def test_ask_flags_escalate_and_degraded():
    payload = {**OK, "escalate": True, "degraded": True, "path": "abstain"}
    r = client_with(lambda req: httpx.Response(200, json=payload)).ask("unknown", "s1")
    assert r.ok and r.escalate is True and r.degraded is True and r.path == "abstain"


def test_ask_backend_down():
    def boom(req: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("refused", request=req)

    r = client_with(boom).ask("hi", "s1")
    assert not r.ok and "backend" in r.error


def test_ask_timeout():
    def slow(req: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("timed out", request=req)

    r = client_with(slow).ask("hi", "s1")
    assert not r.ok and "taking too long" in r.error


def test_ask_validation_rate_limit_and_server_errors():
    assert "type a question" in client_with(lambda req: httpx.Response(422)).ask("", "s").error
    assert "wait a minute" in client_with(lambda req: httpx.Response(429)).ask("hi", "s").error
    assert "error 500" in client_with(lambda req: httpx.Response(500)).ask("x", "s").error
    assert "invalid response" in client_with(lambda req: httpx.Response(200, text="not-json")).ask("x", "s").error


def test_feedback():
    assert client_with(lambda req: httpx.Response(201, json={})).send_feedback("abc123", 1)
    assert not client_with(lambda req: httpx.Response(404, json={})).send_feedback("missing", -1)

    def boom(req: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("refused", request=req)

    assert not client_with(boom).send_feedback("abc123", 1)


def test_healthy():
    assert client_with(lambda req: httpx.Response(200, json={"status": "ok"})).healthy() is True
    assert client_with(lambda req: httpx.Response(503)).healthy() is False

    def boom(req: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("refused", request=req)

    assert client_with(boom).healthy() is False


def test_validate_input():
    assert validate_input("   ") == "Please type a question."
    assert validate_input("x" * 2001).startswith("Your question is too long")
    assert "English" in validate_input("tôi có thể đăng ký khóa luận không?")
    assert validate_input("hello") is None


def test_app_shows_error_when_backend_down(monkeypatch):
    monkeypatch.setattr(AssistantClient, "healthy", lambda self: False)
    at = AppTest.from_file(APP_PATH).run()
    assert at.title[0].value == "🎓 FIT Study Assistant"
    assert len(at.error) == 1
    assert "not reachable" in at.error[0].value


def test_app_healthy_and_session_id_persists(monkeypatch):
    monkeypatch.setattr(AssistantClient, "healthy", lambda self: True)
    at = AppTest.from_file(APP_PATH).run()
    assert len(at.error) == 0
    sid = at.session_state["session_id"]
    assert isinstance(sid, str) and len(sid) == 12
    at.run()
    assert at.session_state["session_id"] == sid


def test_format_sources():
    assert format_sources([]) == ""
    assert format_sources(OK["sources"]) == "Sources: S26#1 — 1 Library borrowing"


def test_status_note():
    assert "Training Office" in status_note(ChatResult(ok=True, escalate=True))
    assert status_note(ChatResult(ok=True)) is None