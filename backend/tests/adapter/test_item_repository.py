import pytest
from pytest_mock import MockerFixture

from app.adapter.item_repository import ItemRepository
from app.models import ItemDB
from app.schema import Item


@pytest.fixture
def mock_db_models():
    content = {"type": "text", "value": "foo"}
    question = {"type": "text", "value": "bar"}
    return [
        ItemDB(id=1, name="bar", question=question, content=content, order=1),
        ItemDB(id=2, name="foo", question=question, content=content, order=2),
    ]


@pytest.mark.asyncio
async def test_get_items_found(mocker: MockerFixture, make_mock_get_db, mock_db_models):
    mock_get_db, _ = make_mock_get_db(scalars_all=mock_db_models)

    mocker.patch("app.adapter.item_repository.get_db", side_effect=mock_get_db)

    repo = ItemRepository()

    results = await repo.get_items(questionnaire_id=1)

    assert len(results) == 2
    assert isinstance(results[0], Item)


@pytest.mark.asyncio
async def test_get_items_not_found(mocker: MockerFixture, make_mock_get_db, mock_db_models):
    mock_get_db, _ = make_mock_get_db(scalars_all=[])

    mocker.patch("app.adapter.item_repository.get_db", side_effect=mock_get_db)

    repo = ItemRepository()

    results = await repo.get_items(questionnaire_id=1)

    assert len(results) == 0
