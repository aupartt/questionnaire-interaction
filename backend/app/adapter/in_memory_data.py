import logging

from app.models.schemas import Answer, Item, QuestionnaireModel, SessionModel
from app.service.protocol.data_adapter_protocol import DataAdapterProtocol

logger = logging.getLogger(__name__)


class InMemoryAdapter(DataAdapterProtocol):
    """
    Adapter temporaire pour gérer les données
    """

    def __init__(self) -> None:
        super().__init__()
        self.sessions = []
        self.reponses = []
        self.questionnaires = QUESTIONNAIRES

    async def get_sessions(self, api_key: str) -> list[SessionModel]:
        """Retourne la liste de sessions liées à la clé api"""
        user_sessions = list(filter(lambda x: x["api_key"] == api_key, self.sessions))
        return [SessionModel(**s) for s in user_sessions]

    async def get_questionnaires(self) -> list[QuestionnaireModel]:
        """Retourne la liste de questionnaires dans l'ordre de passage."""
        return sorted(
            [QuestionnaireModel(**q) for q in self.questionnaires],
            key=lambda x: x.order,
        )
