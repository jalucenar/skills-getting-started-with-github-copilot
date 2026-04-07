import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app

ORIGINAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(ORIGINAL_ACTIVITIES)
    activities.clear()
    activities.update(original)
    yield
    activities.clear()
    activities.update(original)


@pytest.fixture
def client():
    return TestClient(app)
