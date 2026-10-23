import pytest
from assistant_core.models import Message, Intent
from assistant_core.responder import StubLLMResponder

def test_handle_greeting(service):
    res = service.handle(Message(text="hello"))
    assert res.intent == Intent.GREETING
    assert "help with offices" in res.answer

def test_handle_fee(service):
    res = service.handle(Message(text="tuition for 18 credits and 2 retake"))
    assert res.intent == Intent.FEE
    assert "9,450,000" in res.answer

def test_handle_office(service):
    res = service.handle(Message(text="library"))
    assert res.intent == Intent.OFFICE
    assert "room B.201" in res.answer

def test_handle_rule(service):
    res = service.handle(Message(text="thesis credits"))
    assert res.intent == Intent.RULE
    assert len(res.sources) == 1
    assert res.sources[0].id == "H26-5.3"
    assert res.degraded is False

def test_fallback_when_provider_fails(service):
    service.responder = StubLLMResponder(fail=True)
    res = service.handle(Message(text="thesis registration credits"))
    assert res.intent == Intent.RULE
    assert res.degraded is True
    assert len(res.sources) == 1
