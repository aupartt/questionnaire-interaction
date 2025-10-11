import pytest
from pytest_mock import MockerFixture

from app.adapter.user_repository import UserRepository
from app.models.users import UserDB
from app.schema import User


@pytest.mark.asyncio
async def test_get_user_id_found(mocker: MockerFixture, make_mock_get_db):
    mock_result = UserDB(id=1, name="Mathieu", email="mathieu@foo.bar", api_key="foo")
    mock_get_db, _ = make_mock_get_db(scalar_one_or_none=mock_result)

    mocker.patch("app.adapter.user_repository.get_db", side_effect=mock_get_db)

    repo = UserRepository()

    result = await repo.get_user_by_key("foo")

    assert isinstance(result, User)


@pytest.mark.asyncio
async def test_get_user_id_not_found(mocker: MockerFixture, make_mock_get_db):
    mock_result = None
    mock_get_db, _ = make_mock_get_db(scalar_one_or_none=mock_result)

    mocker.patch("app.adapter.user_repository.get_db", side_effect=mock_get_db)

    repo = UserRepository()

    result = await repo.get_user_by_key("foo")

    assert result == None
