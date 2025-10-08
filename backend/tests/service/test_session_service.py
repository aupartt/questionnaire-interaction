from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException, status
from pytest_mock import MockerFixture

from app.adapter import AnswerRepository, ItemRepository, QuestionnaireRepository, SessionRepository
from app.schema import Answer, Item, ItemContent, ItemQuestion, ItemShort, QuestionnaireModel, Session, SessionModel
from app.schema.common import QuestionType, StatusEnum
from app.service.session_service import SessionService


@pytest.mark.asyncio
async def test_get_session_no_questionnaire(mocker: MockerFixture):
    questionnaire_repo = AsyncMock(spec=QuestionnaireRepository)
    questionnaire_repo.get_questionnaire_by_id = AsyncMock(return_value=None)

    session_repo = AsyncMock(spec=SessionRepository)
    session_repo.get_session_questionnaire = AsyncMock(return_value=None)

    item_repo = AsyncMock(spec=ItemRepository)
    item_repo.get_items = AsyncMock(return_value=None)

    answer_repo = AsyncMock(spec=AnswerRepository)
    answer_repo.get_answers = AsyncMock(return_value=None)

    service = SessionService(
        session_repo=session_repo, questionnaire_repo=questionnaire_repo, item_repo=item_repo, answer_repo=answer_repo
    )

    with pytest.raises(HTTPException) as exec:
        result = await service.get_session(user_id=1, questionnaire_id=1)

        assert result is None
        assert exec.value.status_code == status.HTTP_404_NOT_FOUND
        assert exec.value.detail == "Aucun Questionnaire ne correspond à l'identifiant 1"


@pytest.mark.asyncio
async def test_get_session_no_session(mocker: MockerFixture):
    mock_questionnaire = QuestionnaireModel(id=1, name="Foo", description="foo", order=1)
    questionnaire_repo = AsyncMock(spec=QuestionnaireRepository)
    questionnaire_repo.get_questionnaire_by_id = AsyncMock(return_value=mock_questionnaire)

    session_repo = AsyncMock(spec=SessionRepository)
    session_repo.get_session_questionnaire = AsyncMock(return_value=None)

    item_repo = AsyncMock(spec=ItemRepository)
    item_repo.get_items = AsyncMock(return_value=None)

    answer_repo = AsyncMock(spec=AnswerRepository)
    answer_repo.get_answers = AsyncMock(return_value=None)

    service = SessionService(
        session_repo=session_repo, questionnaire_repo=questionnaire_repo, item_repo=item_repo, answer_repo=answer_repo
    )

    with pytest.raises(HTTPException) as exec:
        result = await service.get_session(user_id=1, questionnaire_id=1)

        assert result is None
        assert exec.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert exec.value.detail == "Impossible de récupérer une Session."


@pytest.mark.asyncio
async def test_get_session_ok(mocker: MockerFixture):
    mock_questionnaire = QuestionnaireModel(id=1, name="Foo", description="foo", order=1)
    questionnaire_repo = AsyncMock(spec=QuestionnaireRepository)
    questionnaire_repo.get_questionnaire_by_id = AsyncMock(return_value=mock_questionnaire)

    mock_session = SessionModel(id=12, questionnaire_id=1, user_id=1, status=StatusEnum.COMPLETED)
    session_repo = AsyncMock(spec=SessionRepository)
    session_repo.get_session_questionnaire = AsyncMock(return_value=mock_session)

    mock_item = Item(
        id=1,
        name="Item1",
        question=ItemQuestion(type=QuestionType.TEXT, value="value"),
        content=ItemContent(type="text", value="foo"),
    )
    item_repo = AsyncMock(spec=ItemRepository)
    item_repo.get_items = AsyncMock(return_value=[mock_item])

    answer_repo = AsyncMock(spec=AnswerRepository)
    answer_repo.get_answers = AsyncMock(return_value=[Answer(item_id=1, value="baz", status=StatusEnum.COMPLETED)])

    service = SessionService(
        session_repo=session_repo, questionnaire_repo=questionnaire_repo, item_repo=item_repo, answer_repo=answer_repo
    )

    result = await service.get_session(user_id=1, questionnaire_id=1337)

    assert isinstance(result, Session)
    assert result.id == 12
    assert result.questionnaire_id == 1337
    assert len(result.items) == 1
    assert isinstance(result.items[0], ItemShort)
    assert len(result.answers) == 1
    assert isinstance(result.answers[0], Answer)
    assert result.current_item == mock_item
