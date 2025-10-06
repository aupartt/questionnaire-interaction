from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.controller.questionnaire_controller import router
from app.models.common import QuestionType, StatusEnum
from app.models.schemas import (
    Answer,
    Item,
    ItemContent,
    ItemQuestion,
    ItemShort,
    NextItemResponse,
    QuestionnaireStatus,
    Session,
)


@pytest.fixture()
def make_mock_client():
    def make(mock_service=AsyncMock()):
        app = FastAPI()
        app.include_router(router)

        @app.middleware("http")
        async def add_api_key(request, call_next):
            """Simule le middleware pour ajouter la clé api dans les state"""
            request.state.api_key = request.headers.get("X-API-Key")
            return await call_next(request)

        from app.controller.questionnaire_controller import get_questionnaire_service

        app.dependency_overrides[get_questionnaire_service] = lambda: mock_service

        return TestClient(app)

    return make


@pytest.mark.asyncio
async def test_get_questionnaires(make_mock_client):
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
    response = client.get("/questionnaires", headers={"X-API-Key": "foo-api-key"})

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == "1"
    mock_service.get_questionnaires.assert_awaited_once_with(api_key="foo-api-key")


@pytest.mark.asyncio
async def test_get_session(make_mock_client):
    mock_service = MagicMock()

    mock_items = [ItemShort(id="1", name="Who?"), ItemShort(id="2", name="Where?")]
    mock_answers = [Answer(item_id="1", value="Me!", status=StatusEnum.COMPLETED)]
    mock_item = Item(
        id="2",
        name="Where?",
        question=ItemQuestion(type=QuestionType.TEXT, value="Where?"),
        content=ItemContent(type="text"),
    )
    mock_service.get_session = AsyncMock(
        return_value=Session(
            id="1",
            questionnaire_id="1",
            items=mock_items,
            answers=mock_answers,
            current_item=mock_item,
        )
    )

    client = make_mock_client(mock_service=mock_service)
    response = client.post("/questionnaire/42/session", headers={"X-API-Key": "foo-api-key"})

    assert response.status_code == 200
    data = response.json()
    assert Session.model_validate(data)
    mock_service.get_session.assert_awaited_once_with(api_key="foo-api-key", questionnaire_id="42")


@pytest.mark.asyncio
async def test_add_answer(make_mock_client):
    mock_service = MagicMock()

    mock_service.add_answer = AsyncMock(
        return_value=NextItemResponse(
            result_url="/questionnaire/5/session/3/answer", session_status=StatusEnum.COMPLETED
        )
    )
    mock_answer = Answer(item_id="2", value="Ceci va échouer", status=StatusEnum.COMPLETED)

    client = make_mock_client(mock_service=mock_service)
    response = client.post(
        "/questionnaire/42/session/3/answer",
        headers={"X-API-Key": "foo-api-key"},
        json=mock_answer.model_dump(),
    )

    assert response.status_code == 200
    data = response.json()
    assert NextItemResponse.model_validate(data)
    mock_service.add_answer.assert_awaited_once_with(questionnaire_id="42", session_id="3", answer=mock_answer)
