from unittest.mock import AsyncMock, MagicMock

import pytest
from app.config import settings
from app.controller.questionnaire_controller import router
from app.models.schemas import QuestionnaireStatus
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture()
def make_mock_client():
    def make(mock_service=AsyncMock()):
        app = FastAPI()
        app.include_router(router)

        @app.middleware("http")
        async def add_api_key(request, call_next):
            """Simule le middleware pour ajouter la clé api dans les state"""
            request.state.api_key = request.headers.get(settings.API_KEY_NAME)
            return await call_next(request)

        from app.controller.questionnaire_controller import get_questionnaire_service

        app.dependency_overrides[get_questionnaire_service] = lambda: mock_service

        return TestClient(app)

    return make


@pytest.mark.asyncio
async def test_get_questionnaires(make_mock_client):
    """Test simple du endpoint /questionnaires avec mock d'adapter"""

    mock_service = MagicMock()
    mock_service.get_questionnaires = AsyncMock(
        return_value=[
            QuestionnaireStatus(
                id="1",
                name="SuperName",
                description="SuperDesc",
                session_id=None,
                status=None,
                is_next=True,
            )
        ]
    )

    client = make_mock_client(mock_service=mock_service)
    response = client.get(
        "/questionnaires", headers={settings.API_KEY_NAME: "foo-api-key"}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == "1"
    mock_service.get_questionnaires.assert_awaited_once_with("foo-api-key")
