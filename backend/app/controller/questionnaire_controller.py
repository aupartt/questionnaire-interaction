from fastapi import APIRouter, Depends

from app.controller.dependencies.security import verify_api_key
from app.controller.dependencies.services import questionnaire_service
from app.schema import Answer, NextItemResponse, QuestionnaireStatus, Session
from app.schema.common import VerifyResult
from app.service.questionnaire_service import QuestionnaireService

router = APIRouter()


@router.get("/questionnaires", response_model=list[QuestionnaireStatus])
async def get_questionnaires(
    api_key: str = Depends(verify_api_key), service: QuestionnaireService = Depends(questionnaire_service)
):
    return await service.get_questionnaires(api_key=api_key)


@router.get("/verify", response_model=VerifyResult)
async def verify(_: str = Depends(verify_api_key)):
    return VerifyResult(is_valid=True)


@router.post("/questionnaire/{questionnaire_id}/session", response_model=Session)
async def get_session(
    questionnaire_id: int,
    api_key: str = Depends(verify_api_key),
    service: QuestionnaireService = Depends(questionnaire_service),
):
    return await service.get_session(api_key=api_key, questionnaire_id=questionnaire_id)


@router.post("/questionnaire/{questionnaire_id}/session/{session_id}/answer", response_model=NextItemResponse)
async def add_answer(
    questionnaire_id: int,
    session_id: int,
    answer: Answer,
    _: str = Depends(verify_api_key),
    service: QuestionnaireService = Depends(questionnaire_service),
):
    return await service.add_answer(questionnaire_id=questionnaire_id, session_id=session_id, answer=answer)
