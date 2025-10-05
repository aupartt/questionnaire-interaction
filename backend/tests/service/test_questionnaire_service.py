from datetime import datetime
from unittest.mock import AsyncMock, Mock

import pytest
from app.models.common import StatusEnum
from app.models.schemas import Questionnaire, QuestionnaireStatus, Session
from app.service.protocol.data_adapter_protocol import DataAdapterProtocol
from app.service.questionnaire_service import QuestionnaireService


@pytest.fixture()
def make_mock_adapter():
    def make(sessions: list[Session] = [], questionnaires: list[Questionnaire] = []):
        mock_adapter = Mock(DataAdapterProtocol)
        mock_adapter.get_sessions = AsyncMock(return_value=sessions)
        mock_adapter.get_questionnaires = AsyncMock(return_value=questionnaires)
        return mock_adapter

    return make


@pytest.mark.asyncio
async def test_get_questionnaires_no_session(make_mock_adapter):
    mock_sessions = []
    mock_questionnaires = [
        Questionnaire(id="1", name="SuperName-1", description="SuperDesc-1", order=1),
        Questionnaire(id="2", name="SuperName-2", description="SuperDesc-2", order=2),
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
        Session(
            id="1",
            questionnaire_id="1",
            api_key="foo",
            status=StatusEnum.ACTIVE,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ]
    mock_questionnaires = [
        Questionnaire(id="1", name="SuperName-1", description="SuperDesc-1", order=1),
        Questionnaire(id="2", name="SuperName-2", description="SuperDesc-2", order=2),
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
        Session(
            id="1",
            questionnaire_id="1",
            api_key="foo",
            status=StatusEnum.COMPLETED,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ]
    mock_questionnaires = [
        Questionnaire(id="1", name="SuperName-1", description="SuperDesc-1", order=1),
        Questionnaire(id="2", name="SuperName-2", description="SuperDesc-2", order=2),
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
