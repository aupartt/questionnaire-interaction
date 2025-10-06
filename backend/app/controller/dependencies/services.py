from fastapi import Depends

from app.adapter.in_memory_data import InMemoryAdapter
from app.service.protocol.data_adapter_protocol import DataAdapterProtocol
from app.service.questionnaire_service import QuestionnaireService


def questionnaire_service(
    data_adapter: DataAdapterProtocol = Depends(InMemoryAdapter),
) -> QuestionnaireService:
    return QuestionnaireService(data_adapter)
