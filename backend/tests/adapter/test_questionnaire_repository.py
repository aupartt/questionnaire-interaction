import pytest
from pytest_mock import MockerFixture

from app.adapter.questionnaire_repository import QuestionnaireRepository
from app.models.questionnaires import QuestionnaireDB
from app.schema.questionnaires import QuestionnaireModel


@pytest.fixture
def mock_db_models():
    return [
        QuestionnaireDB(id=1, name="bar", description="rab", order=2),
        QuestionnaireDB(id=2, name="foo", description="oof", order=1),
    ]


@pytest.mark.asyncio
async def test_get_questionnaires_found(mocker: MockerFixture, make_mock_get_db, mock_db_models):
    mock_get_db = make_mock_get_db(scalars_all=mock_db_models)

    mocker.patch("app.adapter.questionnaire_repository.get_db", side_effect=mock_get_db)

    repo = QuestionnaireRepository()

    results = await repo.get_questionnaires()

    assert len(results) == 2
    assert isinstance(results[0], QuestionnaireModel)


@pytest.mark.asyncio
async def test_get_questionnaires_not_found(mocker: MockerFixture, make_mock_get_db):
    mock_result = []
    mock_get_db = make_mock_get_db(scalars_all=mock_result)

    mocker.patch("app.adapter.questionnaire_repository.get_db", side_effect=mock_get_db)

    repo = QuestionnaireRepository()

    results = await repo.get_questionnaires()

    assert len(results) == 0


@pytest.mark.asyncio
async def test_get_questionnaire_by_id_found(mocker: MockerFixture, make_mock_get_db, mock_db_models):
    mock_result = mock_db_models[0]
    mock_get_db = make_mock_get_db(scalar_one_or_none=mock_result)

    mocker.patch("app.adapter.questionnaire_repository.get_db", side_effect=mock_get_db)

    repo = QuestionnaireRepository()

    result = await repo.get_questionnaire_by_id(1)

    assert isinstance(result, QuestionnaireModel)


@pytest.mark.asyncio
async def test_get_questionnaire_by_id_not_found(mocker: MockerFixture, make_mock_get_db, mock_db_models):
    mock_result = None
    mock_get_db = make_mock_get_db(scalar_one_or_none=mock_result)

    mocker.patch("app.adapter.questionnaire_repository.get_db", side_effect=mock_get_db)

    repo = QuestionnaireRepository()

    result = await repo.get_questionnaire_by_id(1)

    assert result == None
