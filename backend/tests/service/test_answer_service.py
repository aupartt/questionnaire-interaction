from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException, status
from pytest_mock import MockerFixture

from app.adapter import AnswerRepository, ItemRepository
from app.schema import Answer, Item, ItemContent, ItemQuestion, NextItemResponse
from app.schema.common import QuestionType, Result, ResultStatus, StatusEnum
from app.service.answer_service import AnswerService


@pytest.mark.asyncio
async def test_add_answer_no_item(mocker: MockerFixture):
    mock_item = Item(
        id=1,
        name="foo",
        question=ItemQuestion(type=QuestionType.TEXT, value="baz"),
        content=ItemContent(type="text", value="foo"),
    )
    item_repo = AsyncMock(spec=ItemRepository)
    item_repo.get_items = AsyncMock(return_value=[mock_item])

    answer_repo = AsyncMock(spec=AnswerRepository)
    answer_repo.get_answers = AsyncMock(return_value=Result)

    mock_answer = Answer(item_id=2, value="gneu", status=StatusEnum.COMPLETED)

    service = AnswerService(item_repo=item_repo, answer_repo=answer_repo)

    with pytest.raises(HTTPException) as exec:
        result = await service.add_answer(questionnaire_id=1, session_id=1, answer=mock_answer)

        assert result is None
        assert exec.value.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            exec.value.detail
            == "L'identifiant d'Item 2 spécifié dans le corp de la requête n'existe pas pour le questionnaire 1."
        )


@pytest.mark.asyncio
async def test_add_answer_no_save(mocker: MockerFixture):
    mock_item_1 = Item(
        id=1,
        name="foo",
        question=ItemQuestion(type=QuestionType.TEXT, value="baz"),
        content=ItemContent(type="text", value="foo"),
    )

    mock_item_2 = Item(
        id=2,
        name="foo2",
        question=ItemQuestion(type=QuestionType.TEXT, value="baz2"),
        content=ItemContent(type="text", value="foo2"),
    )

    item_repo = AsyncMock(spec=ItemRepository)
    item_repo.get_items = AsyncMock(return_value=[mock_item_1, mock_item_2])

    answer_repo = AsyncMock(spec=AnswerRepository)
    answer_repo.save_answer = AsyncMock(return_value=Result(status=ResultStatus.ERROR, message="YOUPI"))

    mock_answer = Answer(item_id=1, value="gneu", status=StatusEnum.COMPLETED)

    service = AnswerService(item_repo=item_repo, answer_repo=answer_repo)

    with pytest.raises(HTTPException) as exec:
        result = await service.add_answer(questionnaire_id=1, session_id=1, answer=mock_answer)

        assert result is None
        assert exec.value.status_code == status.HTTP_400_BAD_REQUEST
        assert exec.value.detail == "YOUPI"


@pytest.mark.asyncio
async def test_add_answer_get_next(mocker: MockerFixture):
    mock_item_1 = Item(
        id=1,
        name="foo",
        question=ItemQuestion(type=QuestionType.TEXT, value="baz"),
        content=ItemContent(type="text", value="foo"),
    )

    mock_item_2 = Item(
        id=2,
        name="foo2",
        question=ItemQuestion(type=QuestionType.TEXT, value="baz2"),
        content=ItemContent(type="text", value="foo2"),
    )

    item_repo = AsyncMock(spec=ItemRepository)
    item_repo.get_items = AsyncMock(return_value=[mock_item_1, mock_item_2])

    answer_repo = AsyncMock(spec=AnswerRepository)
    answer_repo.save_answer = AsyncMock(return_value=Result(status=ResultStatus.SUCCESS, message="YOUPI"))

    mock_answer = Answer(item_id=1, value="gneu", status=StatusEnum.COMPLETED)

    service = AnswerService(item_repo=item_repo, answer_repo=answer_repo)

    result = await service.add_answer(questionnaire_id=1, session_id=1, answer=mock_answer)

    assert isinstance(result, NextItemResponse)
    assert result.next_item == mock_item_2
    assert result.session_status == StatusEnum.ACTIVE
    assert result.result_url is None


@pytest.mark.asyncio
async def test_add_answer_is_last(mocker: MockerFixture):
    mock_item_1 = Item(
        id=1,
        name="foo",
        question=ItemQuestion(type=QuestionType.TEXT, value="baz"),
        content=ItemContent(type="text", value="foo"),
    )

    mock_item_2 = Item(
        id=2,
        name="foo2",
        question=ItemQuestion(type=QuestionType.TEXT, value="baz2"),
        content=ItemContent(type="text", value="foo2"),
    )

    item_repo = AsyncMock(spec=ItemRepository)
    item_repo.get_items = AsyncMock(return_value=[mock_item_1, mock_item_2])

    answer_repo = AsyncMock(spec=AnswerRepository)
    answer_repo.save_answer = AsyncMock(return_value=Result(status=ResultStatus.SUCCESS, message="YOUPI"))

    mock_answer = Answer(item_id=2, value="gneu", status=StatusEnum.COMPLETED)

    service = AnswerService(item_repo=item_repo, answer_repo=answer_repo)

    result = await service.add_answer(questionnaire_id=4, session_id=8, answer=mock_answer)

    assert isinstance(result, NextItemResponse)
    assert result.next_item is None
    assert result.session_status == StatusEnum.COMPLETED
    assert result.result_url == "/questionnaire/4/session/8/results"
