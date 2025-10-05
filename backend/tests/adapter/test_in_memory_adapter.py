from datetime import datetime

import pytest
from app.adapter.in_memory_data import InMemoryAdapter
from app.models.common import StatusEnum
from app.models.schemas import Questionnaire, Session
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
    assert isinstance(results[0], Session)


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
    assert isinstance(results[0], Questionnaire)
    assert results[0].order == 1
