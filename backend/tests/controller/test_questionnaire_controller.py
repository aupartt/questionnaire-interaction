from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from app.controller.questionnaire_controller import router
from app.schema import (
    Answer,
    Item,
    ItemContent,
    ItemQuestion,
    ItemShort,
    NextItemResponse,
    QuestionnaireStatus,
    Session,
)
from app.schema.common import QuestionType, StatusEnum, WillSmith
from app.service import AnswerService, QuestionnaireService, ResultsService, SessionService


@pytest.fixture()
def make_mock_client():
    def make(service=None, mock_service=AsyncMock(), user_id=0):
        app = FastAPI()
        app.include_router(router)

        from app.controller.dependencies.security import verify_api_key

        if service is not None:
            app.dependency_overrides[service] = lambda: mock_service
        app.dependency_overrides[verify_api_key] = lambda: user_id

        return TestClient(app)

    return make


@pytest.mark.asyncio
async def test_verify_success(make_mock_client):
    client = make_mock_client(user_id=42)

    response = client.get("/verify", headers={"X-API-Key": "foo-api-key"})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["is_valid"]


@pytest.mark.asyncio
async def test_get_questionnaires(make_mock_client):
    mock_service = MagicMock()
    mock_service.get_questionnaires = AsyncMock(
        return_value=[
            QuestionnaireStatus(
                id=1,
                name="SuperName",
                description="SuperDesc",
                session_id=None,
                status=None,
                is_next=True,
            )
        ]
    )
    client = make_mock_client(QuestionnaireService, mock_service=mock_service, user_id=42)
    response = client.get("/questionnaires", headers={"X-API-Key": "foo-api-key"})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == 1
    mock_service.get_questionnaires.assert_awaited_once_with(user_id=42)


@pytest.mark.asyncio
async def test_get_session(make_mock_client):
    mock_service = MagicMock()

    mock_items = [ItemShort(id=1, name="Who?"), ItemShort(id=2, name="Where?")]
    mock_answers = [Answer(item_id=1, value="Me!", status=StatusEnum.COMPLETED)]
    mock_item = Item(
        id=2,
        name="Where?",
        question=ItemQuestion(type=QuestionType.TEXT, value="Where?"),
        content=ItemContent(type="text"),
    )
    mock_service.get_session = AsyncMock(
        return_value=Session(
            id=1,
            questionnaire_id=1,
            items=mock_items,
            answers=mock_answers,
            current_item=mock_item,
        )
    )

    client = make_mock_client(SessionService, mock_service=mock_service, user_id=42)
    response = client.post("/questionnaire/42/session", headers={"X-API-Key": "foo-api-key"})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert Session.model_validate(data)
    mock_service.get_session.assert_awaited_once_with(user_id=42, questionnaire_id=42)


@pytest.mark.asyncio
async def test_add_answer(make_mock_client):
    mock_service = MagicMock()

    mock_service.add_answer = AsyncMock(
        return_value=NextItemResponse(
            result_url="/questionnaire/5/session/3/answer", session_status=StatusEnum.COMPLETED
        )
    )
    mock_answer = Answer(item_id=2, value="Ceci va échouer", status=StatusEnum.COMPLETED)

    client = make_mock_client(AnswerService, mock_service=mock_service, user_id=42)
    response = client.post(
        "/questionnaire/42/session/3/answer",
        headers={"X-API-Key": "foo-api-key"},
        json=mock_answer.model_dump(),
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert NextItemResponse.model_validate(data)
    mock_service.add_answer.assert_awaited_once_with(questionnaire_id=42, session_id=3, answer=mock_answer)


@pytest.mark.asyncio
async def test_get_results(make_mock_client):
    mock_service = MagicMock()

    mock_service.get_results = AsyncMock(return_value=WillSmith(img_url="FOOOO.jpg"))

    client = make_mock_client(ResultsService, mock_service=mock_service, user_id=42)
    response = client.post("/questionnaire/42/session/3/results", headers={"X-API-Key": "foo-api-key"})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert WillSmith.model_validate(data)
    assert data["img_url"] == "FOOOO.jpg"
    mock_service.get_results.assert_awaited_once_with(questionnaire_id=42, session_id=3)
