from datetime import datetime

import pytest
from app.adapter.in_memory_data import InMemoryAdapter
from app.models.common import StatusEnum
from app.models.schemas import Answer, Item, QuestionnaireModel, SessionModel
from pytest_mock import MockerFixture


@pytest.mark.asyncio
async def test_get_session_no_results(mocker: MockerFixture):
    adapter = InMemoryAdapter()

    sessions = await adapter.get_sessions("foo")
    assert len(sessions) == 0


@pytest.mark.asyncio
async def test_get_session_with_results(mocker: MockerFixture):
    adapter = InMemoryAdapter()
    adapter.sessions = [
        {
            "id": "1",
            "questionnaire_id": "1",
            "api_key": "foo",
            "status": StatusEnum.COMPLETED,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        },
        {
            "id": "2",
            "questionnaire_id": "2",
            "api_key": "foo",
            "status": StatusEnum.COMPLETED,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        },
        {
            "id": "3",
            "questionnaire_id": "1",
            "api_key": "bar",
            "status": StatusEnum.COMPLETED,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        },
    ]

    results = await adapter.get_sessions("foo")
    assert len(results) == 2
    assert isinstance(results[0], SessionModel)


@pytest.mark.asyncio
async def test_get_questionnaires(mocker: MockerFixture):
    adapter = InMemoryAdapter()
    adapter.questionnaires = [
        {
            "id": "2",
            "name": "Bar",
            "description": "BarDesc",
            "order": 2,
        },
        {
            "id": "1",
            "name": "Foo",
            "description": "FooDesc",
            "order": 1,
        },
    ]

    results = await adapter.get_questionnaires()
    assert len(results) == 2
    assert isinstance(results[0], QuestionnaireModel)
    assert results[0].order == 1


@pytest.mark.asyncio
async def test_get_session_questionnaire_no_session(mocker: MockerFixture):
    adapter = InMemoryAdapter()
    adapter.sessions = []
    adapter.questionnaires = [
        {
            "id": "2",
            "name": "Bar",
            "description": "BarDesc",
            "order": 2,
        },
        {
            "id": "1",
            "name": "Foo",
            "description": "FooDesc",
            "order": 1,
        },
    ]

    result = await adapter.get_session_questionnaire(
        api_key="foo", questionnaire_id="2"
    )

    assert isinstance(result, SessionModel)
    assert result.api_key == "foo"
    assert result.questionnaire_id == "2"
    assert result.status == StatusEnum.ACTIVE


@pytest.mark.asyncio
async def test_get_session_questionnaire_session_found(mocker: MockerFixture):
    adapter = InMemoryAdapter()
    adapter.sessions = [
        {
            "id": "1",
            "questionnaire_id": "2",
            "api_key": "foo",
            "status": "completed",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
    ]
    adapter.questionnaires = [
        {
            "id": "2",
            "name": "Bar",
            "description": "BarDesc",
            "order": 2,
        },
        {
            "id": "1",
            "name": "Foo",
            "description": "FooDesc",
            "order": 1,
        },
    ]

    result = await adapter.get_session_questionnaire(
        api_key="foo", questionnaire_id="2"
    )

    assert isinstance(result, SessionModel)
    assert result.api_key == "foo"
    assert result.questionnaire_id == "2"
    assert result.status == StatusEnum.COMPLETED


@pytest.mark.asyncio
async def test_get_items_not_found(mocker: MockerFixture):
    adapter = InMemoryAdapter()
    adapter.items = []

    results = await adapter.get_items(questionnaire_id="1")

    assert isinstance(results, list)
    assert len(results) == 0


@pytest.mark.asyncio
async def test_get_items_found(mocker: MockerFixture):
    adapter = InMemoryAdapter()
    adapter.items = [
        {
            "id": "1",
            "questionnaire_id": "1",
            "name": "How?",
            "question": {"type": "text", "value": "How?"},
            "content": {"type": "text"},
            "order": 2,
        },
        {
            "id": "2",
            "questionnaire_id": "1",
            "name": "Who?",
            "question": {"type": "text", "value": "Who?"},
            "content": {"type": "text"},
            "order": 1,
        },
        {
            "id": "3",
            "questionnaire_id": "2",
            "name": "When?",
            "question": {"type": "text", "value": "When?"},
            "content": {"type": "text"},
            "order": 1,
        },
    ]

    results = await adapter.get_items(questionnaire_id="1")

    assert len(results) == 2
    assert isinstance(results[0], Item)
    assert results[0].id == "2"
    assert results[1].id == "1"


@pytest.mark.asyncio
async def test_get_answers_not_found(mocker: MockerFixture):
    adapter = InMemoryAdapter()
    adapter.answers = []

    results = await adapter.get_answers(session_id="1")

    assert isinstance(results, list)
    assert len(results) == 0


@pytest.mark.asyncio
async def test_get_answers_found(mocker: MockerFixture):
    adapter = InMemoryAdapter()
    adapter.answers = [
        {
            "id": "1",
            "session_id": "1",
            "item_id": "1",
            "value": "foo",
            "status": StatusEnum.COMPLETED,
        },
        {
            "id": "2",
            "session_id": "1",
            "item_id": "1",
            "value": None,
            "status": StatusEnum.SKIPPED,
        },
        {
            "id": "3",
            "session_id": "2",
            "item_id": "1",
            "value": None,
            "status": StatusEnum.SKIPPED,
        },
    ]

    results = await adapter.get_answers(session_id="1")

    assert isinstance(results[0], Answer)
    assert len(results) == 2
