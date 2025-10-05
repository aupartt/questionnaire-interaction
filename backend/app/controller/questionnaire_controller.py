from fastapi import APIRouter, Depends, Request

from app.adapter.in_memory_data import InMemoryAdapter
from app.models.schemas import Answer, QuestionnaireStatus, Session
from app.service.protocol.data_adapter_protocol import DataAdapterProtocol
from app.service.questionnaire_service import QuestionnaireService

router = APIRouter()


def get_questionnaire_service(
    data_adapter: DataAdapterProtocol = Depends(InMemoryAdapter),
) -> QuestionnaireService:
    return QuestionnaireService(data_adapter)


@router.get("/questionnaires", response_model=list[QuestionnaireStatus])
async def get_questionnaires(request: Request, service: QuestionnaireService = Depends(get_questionnaire_service)):
    api_key = request.state.api_key
    return await service.get_questionnaires(api_key=api_key)


@router.post("/questionnaire/{questionnaire_id}/session", response_model=Session)
async def get_session(
    questionnaire_id: str,
    request: Request,
    service: QuestionnaireService = Depends(get_questionnaire_service),
):
    api_key = request.state.api_key
    return await service.get_session(api_key=api_key, questionnaire_id=questionnaire_id)


@router.post("/questionnaire/{questionnaire_id}/session/{session_id}/answer")
async def add_answer(
    questionnaire_id: str,
    session_id: str,
    answer: Answer,
    service: QuestionnaireService = Depends(get_questionnaire_service),
):
    return await service.add_answer(questionnaire_id=questionnaire_id, session_id=session_id, answer=answer)
