from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
from pytest_mock import MockerFixture

from app.adapter.session_repository import SessionRepository
from app.models import SessionDB
from app.schema import SessionModel
from app.schema.common import StatusEnum


@pytest.fixture
def mock_db_models():
    return [
        SessionDB(
            id=1,
            status=StatusEnum.COMPLETED,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            user_id=1,
            questionnaire_id=1,
        ),
        SessionDB(
            id=2,
            status=StatusEnum.SKIPPED,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            user_id=1,
            questionnaire_id=2,
        ),
        SessionDB(
            id=3,
            status=StatusEnum.ACTIVE,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            user_id=1,
            questionnaire_id=3,
        ),
        SessionDB(
            id=4,
            status=StatusEnum.ACTIVE,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            user_id=2,
            questionnaire_id=1,
        ),
    ]


@pytest.mark.asyncio
async def test_get_session_by_id_found(mocker: MockerFixture, make_mock_get_db, mock_db_models):
    mock_get_db, _ = make_mock_get_db(scalar_one_or_none=mock_db_models[0])

    mocker.patch("app.adapter.session_repository.get_db", side_effect=mock_get_db)

    repo = SessionRepository()

    result = await repo.get_session_by_id(session_id=1)

    assert isinstance(result, SessionModel)


@pytest.mark.asyncio
async def test_get_session_by_id_not_found(mocker: MockerFixture, make_mock_get_db, mock_db_models):
    mock_get_db, _ = make_mock_get_db(scalar_one_or_none=None)

    mocker.patch("app.adapter.session_repository.get_db", side_effect=mock_get_db)

    repo = SessionRepository()

    result = await repo.get_session_by_id(session_id=1)

    assert result is None


@pytest.mark.asyncio
async def test_get_sessions_found(mocker: MockerFixture, make_mock_get_db, mock_db_models):
    mock_get_db, _ = make_mock_get_db(scalars_all=mock_db_models[:-1])

    mocker.patch("app.adapter.session_repository.get_db", side_effect=mock_get_db)

    repo = SessionRepository()

    results = await repo.get_sessions(user_id=1)

    assert len(results) == 3
    assert isinstance(results[0], SessionModel)


@pytest.mark.asyncio
async def test_get_sessions_not_found(mocker: MockerFixture, make_mock_get_db, mock_db_models):
    mock_get_db, _ = make_mock_get_db(scalars_all=[])

    mocker.patch("app.adapter.session_repository.get_db", side_effect=mock_get_db)

    repo = SessionRepository()

    results = await repo.get_sessions(user_id=1)

    assert len(results) == 0


@pytest.mark.asyncio
async def test_get_session_questionnaire_found(mocker: MockerFixture, make_mock_get_db, mock_db_models):
    mock_get_db, _ = make_mock_get_db(scalar_one_or_none=mock_db_models[0])

    mocker.patch("app.adapter.session_repository.get_db", side_effect=mock_get_db)

    repo = SessionRepository()

    result = await repo.get_session_questionnaire(user_id=1, questionnaire_id=1)

    assert isinstance(result, SessionModel)
    assert result.id == mock_db_models[0].id


@pytest.mark.asyncio
async def test_get_session_questionnaire_not_found(mocker: MockerFixture, make_mock_get_db, mock_db_models):
    mock_get_db, mock_session = make_mock_get_db(scalar_one_or_none=None)

    async def mock_refresh(obj):
        obj.id = 42

    mock_session.refresh = AsyncMock(side_effect=mock_refresh)

    mocker.patch("app.adapter.session_repository.get_db", side_effect=mock_get_db)

    repo = SessionRepository()

    result = await repo.get_session_questionnaire(user_id=1, questionnaire_id=4)

    assert isinstance(result, SessionModel)
    assert result.id == 42
    assert result.questionnaire_id == 4


@pytest.mark.asyncio
async def test_get_session_questionnaire_error(mocker: MockerFixture, make_mock_get_db, mock_db_models):
    mocker.patch("app.adapter.session_repository.get_db", side_effect=Exception("FOO!"))
    mock_log = mocker.patch("app.adapter.session_repository.logger.error")

    repo = SessionRepository()

    with pytest.raises(Exception):
        result = await repo.get_session_questionnaire(user_id=1, questionnaire_id=4)

        assert result is None
        assert mock_log.assert_called_once()


@pytest.mark.asyncio
async def test_update_status_found(mocker: MockerFixture, make_mock_get_db, mock_db_models):
    mock_get_db, mock_session = make_mock_get_db(scalar_one_or_none=mock_db_models[0])

    mocker.patch("app.adapter.session_repository.get_db", side_effect=mock_get_db)
    mock_log = mocker.patch("app.adapter.session_repository.logger.error")

    repo = SessionRepository()

    result = await repo.update_status(session_id=1, status=StatusEnum.ACTIVE)

    assert result is None
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_log.assert_not_called()


@pytest.mark.asyncio
async def test_update_status_not_found(mocker: MockerFixture, make_mock_get_db, mock_db_models):
    mock_get_db, mock_session = make_mock_get_db(scalar_one_or_none=None)

    mocker.patch("app.adapter.session_repository.get_db", side_effect=mock_get_db)
    mock_log = mocker.patch("app.adapter.session_repository.logger.error")

    repo = SessionRepository()

    result = await repo.update_status(session_id=1, status=StatusEnum.ACTIVE)

    assert result is None
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_awaited()
    mock_log.assert_not_called()


@pytest.mark.asyncio
async def test_update_status_error(mocker: MockerFixture, make_mock_get_db, mock_db_models):
    mock_get_db, mock_session = make_mock_get_db(scalar_one_or_none=None)

    mocker.patch("app.adapter.session_repository.get_db", side_effect=Exception("FOO!"))
    mock_log = mocker.patch("app.adapter.session_repository.logger.error")

    repo = SessionRepository()

    with pytest.raises(Exception):
        result = await repo.update_status(session_id=1, status=StatusEnum.ACTIVE)

        assert result is None
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_awaited()
        mock_log.assert_called_once()
