import pytest
from assistant_core.errors import ProviderError
from assistant_core.knowledge import Rule
from assistant_core.responder import StubLLMResponder, TemplateResponder


@pytest.fixture
def sample_rule():
    return Rule(
        id="H26-5.3",
        title="Thesis Credits",
        text="Requires 120 credits.",
        keywords=["thesis"],
    )


def test_template_responder(sample_rule):
    responder = TemplateResponder()
    ans = responder.explain("how many credits?", sample_rule)
    assert ans == "Thesis Credits: Requires 120 credits."


def test_stub_llm_responder_success(sample_rule):
    responder = StubLLMResponder(fail=False)
    ans = responder.explain("how many credits?", sample_rule)
    assert ans == "Based on 'Thesis Credits': Requires 120 credits."


def test_stub_llm_responder_failure(sample_rule):
    responder = StubLLMResponder(fail=True)
    with pytest.raises(ProviderError):
        responder.explain("how many credits?", sample_rule)