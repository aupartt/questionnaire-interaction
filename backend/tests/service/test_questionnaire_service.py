from unittest.mock import AsyncMock

import pytest

from app.adapter import AnswerRepository, ItemRepository
from app.schema import (
    QuestionnaireModel,
    QuestionnaireStatus,
    SessionModel,
)
from app.schema.common import StatusEnum
from app.service.questionnaire_service import QuestionnaireService


@pytest.mark.asyncio
async def test_get_questionnaires_no_session():
    mock_sessions = []
    mock_questionnaires = [
        QuestionnaireModel(id=1, name="SuperName-1", description="SuperDesc-1", order=1),
        QuestionnaireModel(id=2, name="SuperName-2", description="SuperDesc-2", order=2),
    ]

    session_repo = AsyncMock(spec=ItemRepository)
    session_repo.get_sessions = AsyncMock(return_value=mock_sessions)

    questionnaire_repo = AsyncMock(spec=AnswerRepository)
    questionnaire_repo.get_questionnaires = AsyncMock(return_value=mock_questionnaires)

    service = QuestionnaireService(session_repo=session_repo, questionnaire_repo=questionnaire_repo)

    results = await service.get_questionnaires(user_id=4)

    assert len(results) == 2
    assert isinstance(results[0], QuestionnaireStatus)
    assert results[0].status is None
    assert results[0].is_next
    assert results[1].status is None
    assert not results[1].is_next


@pytest.mark.asyncio
async def test_get_questionnaires_with_active_session():
    mock_sessions = [
        SessionModel(id=1, questionnaire_id=1, user_id=42, status=StatusEnum.ACTIVE),
    ]
    mock_questionnaires = [
        QuestionnaireModel(id=1, name="SuperName-1", description="SuperDesc-1", order=1),
        QuestionnaireModel(id=2, name="SuperName-2", description="SuperDesc-2", order=2),
    ]

    session_repo = AsyncMock(spec=ItemRepository)
    session_repo.get_sessions = AsyncMock(return_value=mock_sessions)

    questionnaire_repo = AsyncMock(spec=AnswerRepository)
    questionnaire_repo.get_questionnaires = AsyncMock(return_value=mock_questionnaires)

    service = QuestionnaireService(session_repo=session_repo, questionnaire_repo=questionnaire_repo)

    results = await service.get_questionnaires(user_id=2)

    assert len(results) == 2
    assert isinstance(results[0], QuestionnaireStatus)
    assert results[0].status == StatusEnum.ACTIVE
    assert results[0].is_next
    assert results[1].status is None
    assert not results[1].is_next


@pytest.mark.asyncio
async def test_get_questionnaires_with_completed_session():
    mock_sessions = [
        SessionModel(id=1, questionnaire_id=1, user_id=2, status=StatusEnum.COMPLETED),
    ]
    mock_questionnaires = [
        QuestionnaireModel(id=1, name="SuperName-1", description="SuperDesc-1", order=1),
        QuestionnaireModel(id=2, name="SuperName-2", description="SuperDesc-2", order=2),
    ]

    session_repo = AsyncMock(spec=ItemRepository)
    session_repo.get_sessions = AsyncMock(return_value=mock_sessions)

    questionnaire_repo = AsyncMock(spec=AnswerRepository)
    questionnaire_repo.get_questionnaires = AsyncMock(return_value=mock_questionnaires)

    service = QuestionnaireService(session_repo=session_repo, questionnaire_repo=questionnaire_repo)

    results = await service.get_questionnaires(user_id=42)

    assert len(results) == 2
    assert isinstance(results[0], QuestionnaireStatus)
    assert results[0].status == StatusEnum.COMPLETED
    assert not results[0].is_next
    assert results[1].status is None
    assert results[1].is_next
