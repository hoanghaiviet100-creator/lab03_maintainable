import pytest
from pathlib import Path
from assistant_core.config import Settings
from assistant_core.knowledge import OfficeDirectory, Handbook, Office, Rule
from assistant_core.responder import StubLLMResponder
from assistant_core.service import AssistantService

@pytest.fixture
def mock_settings():
    return Settings(
        data_dir=Path("data"),
        credit_rate_vnd=450000,
        retake_multiplier=1.5,
        max_credits=30,
    )

@pytest.fixture
def mock_offices():
    return OfficeDirectory({
        "library": Office("library", "room B.201", "Mon-Sat 07:00-20:00"),
        "academic affairs": Office("academic affairs", "room A.101", "Mon-Fri 08:00-17:00"),
    })

@pytest.fixture
def mock_handbook():
    return Handbook([
        Rule(id="H26-5.3", title="Thesis registration", text="Students need at least 110 credits to register for thesis."),
    ])

@pytest.fixture
def service(mock_settings, mock_offices, mock_handbook):
    return AssistantService(
        settings=mock_settings,
        offices=mock_offices,
        handbook=mock_handbook,
        responder=StubLLMResponder(fail=False),
    )
