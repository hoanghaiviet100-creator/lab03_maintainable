from assistant_core.router import route
from assistant_core.models import Intent

def test_route_greeting():
    assert route("hi", {"library"}) == Intent.GREETING

def test_route_fee():
    assert route("tuition for 18 credits", {"library"}) == Intent.FEE

def test_route_office():
    assert route("where is library", {"library"}) == Intent.OFFICE

def test_route_rule():
    assert route("thesis registration credits", {"library"}) == Intent.RULE
