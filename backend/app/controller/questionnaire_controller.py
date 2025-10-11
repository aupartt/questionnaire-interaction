from fastapi import APIRouter, Depends, Header

from app.controller.dependencies.security import verify_api_key
from app.core.config import settings
from app.schema import Answer, NextItemResponse, QuestionnaireStatus, Session
from app.schema.common import VerifyResult, WillSmith
from app.service import AnswerService, QuestionnaireService, ResultsService, SessionService, UserService

router = APIRouter()


@router.get("/questionnaires", response_model=list[QuestionnaireStatus])
async def get_questionnaires(
    user_id: int = Depends(verify_api_key), service: QuestionnaireService = Depends(QuestionnaireService)
):
    return await service.get_questionnaires(user_id=user_id)


@router.get("/verify", response_model=VerifyResult)
async def verify(api_key: str = Header(..., alias=settings.API_KEY_NAME), service: UserService = Depends(UserService)):
    return await service.verify_api_key(api_key)


@router.post("/questionnaire/{questionnaire_id}/session", response_model=Session)
async def get_session(
    questionnaire_id: int,
    user_id: int = Depends(verify_api_key),
    service: SessionService = Depends(SessionService),
):
    return await service.get_session(user_id=user_id, questionnaire_id=questionnaire_id)


@router.post("/questionnaire/{questionnaire_id}/session/{session_id}/answer", response_model=NextItemResponse)
async def add_answer(
    questionnaire_id: int,
    session_id: int,
    answer: Answer,
    _: str = Depends(verify_api_key),
    service: AnswerService = Depends(AnswerService),
):
    return await service.add_answer(questionnaire_id=questionnaire_id, session_id=session_id, answer=answer)


@router.post("/questionnaire/{questionnaire_id}/session/{session_id}/results", response_model=WillSmith)
async def get_results(
    questionnaire_id: int,
    session_id: int,
    _: int = Depends(verify_api_key),
    service: ResultsService = Depends(ResultsService),
):
    return await service.get_results(questionnaire_id=questionnaire_id, session_id=session_id)
