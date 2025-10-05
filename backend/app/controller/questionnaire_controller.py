from fastapi import APIRouter, Depends, Request

from app.adapter.in_memory_data import InMemoryAdapter
from app.models.schemas import QuestionnaireStatus
from app.service.protocol.data_adapter_protocol import DataAdapterProtocol
from app.service.questionnaire_service import QuestionnaireService

router = APIRouter()


def get_questionnaire_service(
    data_adapter: DataAdapterProtocol = Depends(InMemoryAdapter),
) -> QuestionnaireService:
    return QuestionnaireService(data_adapter)


@router.get("/questionnaires", response_model=list[QuestionnaireStatus])
async def get_questionnaires(
    request: Request, service: QuestionnaireService = Depends(get_questionnaire_service)
):
    api_key = request.state.api_key
    return await service.get_questionnaires(api_key)
