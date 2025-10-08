from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
from pytest_mock import MockerFixture

from app.adapter.answer_repository import AnswerRepository
from app.adapter.session_repository import SessionRepository
from app.models import AnswerDB
from app.models.sessions import SessionDB
from app.schema import Answer
from app.schema.common import Result, ResultStatus, StatusEnum


@pytest.fixture
def mock_db_models():
    return [
        AnswerDB(
            id=1, value="bar", status="skipped", item_id=1, created_at=datetime.now(UTC), updated_at=datetime.now(UTC)
        ),
        AnswerDB(
            id=2, value="foo", status="completed", item_id=2, created_at=datetime.now(UTC), updated_at=datetime.now(UTC)
        ),
    ]


@pytest.mark.asyncio
async def test_get_answers_found(mocker: MockerFixture, make_mock_get_db, mock_db_models):
    mock_get_db, _ = make_mock_get_db(scalars_all=mock_db_models)

    mocker.patch("app.adapter.answer_repository.get_db", side_effect=mock_get_db)

    repo = AnswerRepository()

    results = await repo.get_answers(session_id=1)

    assert len(results) == 2
    assert isinstance(results[0], Answer)


@pytest.mark.asyncio
async def test_get_answers_not_found(mocker: MockerFixture, make_mock_get_db, mock_db_models):
    mock_get_db, _ = make_mock_get_db(scalars_all=[])

    mocker.patch("app.adapter.answer_repository.get_db", side_effect=mock_get_db)

    repo = AnswerRepository()

    results = await repo.get_answers(session_id=1)

    assert len(results) == 0


@pytest.fixture
def make_session_repo():
    def make(
        value=SessionDB(
            id=1,
            status=StatusEnum.COMPLETED,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            user_id=1,
            questionnaire_id=1,
        ),
    ):
        mock_session_repo = AsyncMock(spec=SessionRepository)
        mock_session_repo.get_session_by_id = AsyncMock(return_value=value)
        return mock_session_repo

    return make


@pytest.mark.asyncio
async def test_save_answer_found_no_status(mocker: MockerFixture, make_mock_get_db, mock_db_models, make_session_repo):
    mock_get_db, mock_session = make_mock_get_db()
    mock_session_repo = make_session_repo()
    mock_answer = Answer(item_id=1, value="Foo", status=StatusEnum.COMPLETED)

    mocker.patch("app.adapter.answer_repository.get_db", side_effect=mock_get_db)

    repo = AnswerRepository(repo=mock_session_repo)

    result = await repo.save_answer(session_id=1, answer=mock_answer, session_status=None)

    assert isinstance(result, Result)
    assert result.status == ResultStatus.SUCCESS
    assert result.message == "Réponse sauvegardé"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_save_answer_found_has_status(mocker: MockerFixture, make_mock_get_db, mock_db_models, make_session_repo):
    mock_get_db, mock_session = make_mock_get_db()
    mock_session_repo = make_session_repo()
    mock_answer = Answer(item_id=1, value="Foo", status=StatusEnum.COMPLETED)

    mocker.patch("app.adapter.answer_repository.get_db", side_effect=mock_get_db)

    repo = AnswerRepository(repo=mock_session_repo)

    result = await repo.save_answer(session_id=1, answer=mock_answer, session_status=StatusEnum.COMPLETED)

    assert isinstance(result, Result)
    assert result.status == ResultStatus.SUCCESS
    assert result.message == "Réponse sauvegardé"
    mock_session_repo.update_status.assert_awaited_once_with(1, StatusEnum.COMPLETED)
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_save_answer_not_found(mocker: MockerFixture, make_mock_get_db, mock_db_models, make_session_repo):
    mock_get_db, mock_session = make_mock_get_db()
    mock_session_repo = make_session_repo(None)
    mock_answer = Answer(item_id=1, value="Foo", status=StatusEnum.COMPLETED)

    mocker.patch("app.adapter.answer_repository.get_db", side_effect=mock_get_db)

    repo = AnswerRepository(repo=mock_session_repo)

    result = await repo.save_answer(session_id=1, answer=mock_answer, session_status=StatusEnum.COMPLETED)

    assert isinstance(result, Result)
    assert result.status == ResultStatus.ERROR
    assert result.message == "ID de session introuvable"
    mock_session_repo.update_status.assert_not_awaited()
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_awaited()
    mock_session.refresh.assert_not_awaited()
