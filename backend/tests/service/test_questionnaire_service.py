from datetime import datetime
from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import HTTPException

from app.models.common import QuestionType, ResultStatus, StatusEnum
from app.models.schemas import (
    Answer,
    Item,
    ItemContent,
    ItemQuestion,
    ItemShort,
    NextItemResponse,
    QuestionnaireModel,
    QuestionnaireStatus,
    Result,
    Session,
    SessionModel,
)
from app.service.protocol.data_adapter_protocol import DataAdapterProtocol
from app.service.questionnaire_service import QuestionnaireService


@pytest.fixture()
def make_mock_adapter():
    def make(
        sessions: list[SessionModel] = [],
        questionnaires: list[QuestionnaireModel] = [],
        session: Session | None = None,
        items: list[Item] = [],
        answers: list[Answer] = [],
        result: Result = Result(status=ResultStatus.SUCCESS, message="Nice !"),
    ):
        mock_adapter = Mock(DataAdapterProtocol)
        mock_adapter.get_sessions = AsyncMock(return_value=sessions)
        mock_adapter.get_questionnaires = AsyncMock(return_value=questionnaires)
        mock_adapter.get_session_questionnaire = AsyncMock(return_value=session)
        mock_adapter.get_items = AsyncMock(return_value=items)
        mock_adapter.get_answers = AsyncMock(return_value=answers)
        mock_adapter.save_answer = AsyncMock(return_value=result)

        return mock_adapter

    return make


@pytest.mark.asyncio
async def test_get_questionnaires_no_session(make_mock_adapter):
    mock_sessions = []
    mock_questionnaires = [
        QuestionnaireModel(id="1", name="SuperName-1", description="SuperDesc-1", order=1),
        QuestionnaireModel(id="2", name="SuperName-2", description="SuperDesc-2", order=2),
    ]
    mock_adapter = make_mock_adapter(mock_sessions, mock_questionnaires)

    service = QuestionnaireService(mock_adapter)

    results = await service.get_questionnaires(api_key="foo")

    assert len(results) == 2
    assert isinstance(results[0], QuestionnaireStatus)
    assert results[0].status is None
    assert results[0].is_next
    assert results[1].status is None
    assert not results[1].is_next


@pytest.mark.asyncio
async def test_get_questionnaires_with_active_session(make_mock_adapter):
    mock_sessions = [
        SessionModel(
            id="1",
            questionnaire_id="1",
            api_key="foo",
            status=StatusEnum.ACTIVE,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ]
    mock_questionnaires = [
        QuestionnaireModel(id="1", name="SuperName-1", description="SuperDesc-1", order=1),
        QuestionnaireModel(id="2", name="SuperName-2", description="SuperDesc-2", order=2),
    ]
    mock_adapter = make_mock_adapter(mock_sessions, mock_questionnaires)

    service = QuestionnaireService(mock_adapter)

    results = await service.get_questionnaires(api_key="foo")

    assert len(results) == 2
    assert isinstance(results[0], QuestionnaireStatus)
    assert results[0].status == StatusEnum.ACTIVE
    assert results[0].is_next
    assert results[1].status is None
    assert not results[1].is_next


@pytest.mark.asyncio
async def test_get_questionnaires_with_completed_session(make_mock_adapter):
    mock_sessions = [
        SessionModel(
            id="1",
            questionnaire_id="1",
            api_key="foo",
            status=StatusEnum.COMPLETED,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ]
    mock_questionnaires = [
        QuestionnaireModel(id="1", name="SuperName-1", description="SuperDesc-1", order=1),
        QuestionnaireModel(id="2", name="SuperName-2", description="SuperDesc-2", order=2),
    ]
    mock_adapter = make_mock_adapter(mock_sessions, mock_questionnaires)

    service = QuestionnaireService(mock_adapter)

    results = await service.get_questionnaires(api_key="foo")

    assert len(results) == 2
    assert isinstance(results[0], QuestionnaireStatus)
    assert results[0].status == StatusEnum.COMPLETED
    assert not results[0].is_next
    assert results[1].status is None
    assert results[1].is_next


@pytest.mark.asyncio
async def test_get_session_without_answers(make_mock_adapter):
    mock_session = SessionModel(
        id="1",
        questionnaire_id="1",
        api_key="foo",
        status=StatusEnum.COMPLETED,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    mock_items = [
        Item(
            id="1",
            name="SuperName-1",
            question=ItemQuestion(type=QuestionType.TEXT, value="Who?"),
            content=ItemContent(type="text"),
        ),
        Item(
            id="2",
            name="SuperName-2",
            question=ItemQuestion(type=QuestionType.TEXT, value="What?"),
            content=ItemContent(type="text"),
        ),
    ]
    mock_answers = []
    mock_adapter = make_mock_adapter(session=mock_session, items=mock_items, answers=mock_answers)

    service = QuestionnaireService(mock_adapter)

    result = await service.get_session(api_key="foo", questionnaire_id="1")

    assert isinstance(result, Session)
    assert len(result.items) == 2
    assert isinstance(result.items[0], ItemShort)
    assert len(result.answers) == 0
    assert result.current_item == mock_items[0]


@pytest.mark.asyncio
async def test_get_session_with_answers(make_mock_adapter):
    mock_session = SessionModel(
        id="1",
        questionnaire_id="1",
        api_key="foo",
        status=StatusEnum.COMPLETED,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    mock_items = [
        Item(
            id="1",
            name="SuperName-1",
            question=ItemQuestion(type=QuestionType.TEXT, value="Who?"),
            content=ItemContent(type="text"),
        ),
        Item(
            id="2",
            name="SuperName-2",
            question=ItemQuestion(type=QuestionType.TEXT, value="What?"),
            content=ItemContent(type="text"),
        ),
    ]
    mock_answers = [Answer(item_id="1", value="Foo", status=StatusEnum.COMPLETED)]
    mock_adapter = make_mock_adapter(session=mock_session, items=mock_items, answers=mock_answers)

    service = QuestionnaireService(mock_adapter)

    result = await service.get_session(api_key="foo", questionnaire_id="1")

    assert isinstance(result, Session)
    assert len(result.items) == 2
    assert isinstance(result.items[0], ItemShort)
    assert len(result.answers) == 1
    assert isinstance(result.answers[0], Answer)
    assert result.current_item == mock_items[0]


@pytest.mark.asyncio
async def test_add_answer_success_is_next(make_mock_adapter):
    mock_items = [
        Item(
            id="1",
            name="SuperName-1",
            question=ItemQuestion(type=QuestionType.TEXT, value="Who?"),
            content=ItemContent(type="text"),
        ),
        Item(
            id="2",
            name="SuperName-2",
            question=ItemQuestion(type=QuestionType.TEXT, value="What?"),
            content=ItemContent(type="text"),
        ),
    ]
    mock_adapter = make_mock_adapter(items=mock_items)
    mock_answer = Answer(item_id="1", value="Foo", status=StatusEnum.COMPLETED)

    service = QuestionnaireService(mock_adapter)

    result = await service.add_answer(questionnaire_id="1", session_id="1337", answer=mock_answer)

    assert isinstance(result, NextItemResponse)
    assert result.next_item == mock_items[1]
    assert result.session_status == StatusEnum.ACTIVE


@pytest.mark.asyncio
async def test_add_answer_success_is_last(make_mock_adapter):
    mock_items = [
        Item(
            id="1",
            name="SuperName-1",
            question=ItemQuestion(type=QuestionType.TEXT, value="Who?"),
            content=ItemContent(type="text"),
        ),
        Item(
            id="2",
            name="SuperName-2",
            question=ItemQuestion(type=QuestionType.TEXT, value="What?"),
            content=ItemContent(type="text"),
        ),
    ]
    mock_adapter = make_mock_adapter(items=mock_items)
    mock_answer = Answer(item_id="2", value="Foo", status=StatusEnum.COMPLETED)

    service = QuestionnaireService(mock_adapter)

    result = await service.add_answer(questionnaire_id="1", session_id="1337", answer=mock_answer)

    assert isinstance(result, NextItemResponse)
    assert result.result_url == "/questionnaire/1/session/1337/results"
    assert result.session_status == StatusEnum.COMPLETED


@pytest.mark.asyncio
async def test_add_answer_error_item_id(make_mock_adapter):
    mock_items = [
        Item(
            id="1",
            name="SuperName-1",
            question=ItemQuestion(type=QuestionType.TEXT, value="Who?"),
            content=ItemContent(type="text"),
        ),
        Item(
            id="2",
            name="SuperName-2",
            question=ItemQuestion(type=QuestionType.TEXT, value="What?"),
            content=ItemContent(type="text"),
        ),
    ]
    mock_adapter = make_mock_adapter(items=mock_items)
    mock_answer = Answer(item_id="3", value="Foo", status=StatusEnum.COMPLETED)

    service = QuestionnaireService(mock_adapter)

    with pytest.raises(HTTPException) as excinfo:
        await service.add_answer(questionnaire_id="1", session_id="1337", answer=mock_answer)

    assert excinfo.value.status_code == 400


@pytest.mark.asyncio
async def test_add_answer_error_session_id(make_mock_adapter):
    mock_items = [
        Item(
            id="1",
            name="SuperName-1",
            question=ItemQuestion(type=QuestionType.TEXT, value="Who?"),
            content=ItemContent(type="text"),
        ),
        Item(
            id="2",
            name="SuperName-2",
            question=ItemQuestion(type=QuestionType.TEXT, value="What?"),
            content=ItemContent(type="text"),
        ),
    ]
    mock_message = "ID de session introuvable"
    mock_result = Result(status=ResultStatus.ERROR, message=mock_message)
    mock_adapter = make_mock_adapter(items=mock_items, result=mock_result)
    mock_answer = Answer(item_id="2", value="Foo", status=StatusEnum.COMPLETED)

    service = QuestionnaireService(mock_adapter)

    with pytest.raises(HTTPException) as excinfo:
        await service.add_answer(questionnaire_id="1", session_id="1337", answer=mock_answer)

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == mock_message
