import logging

from app.data.questionnaires import QUESTIONNAIRES
from app.models.schemas import Questionnaire, Session
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

    async def get_sessions(self, api_key: str) -> list[Session]:
        """Retourne la liste de sessions liées à la clé api"""
        user_sessions = list(filter(lambda x: x["api_key"] == api_key, self.sessions))
        return [Session(**s) for s in user_sessions]

    async def get_questionnaires(self) -> list[Questionnaire]:
        """Retourne la liste de questionnaires dans l'ordre de passage."""
        return sorted(
            [Questionnaire(**q) for q in self.questionnaires], key=lambda x: x.order
        )
