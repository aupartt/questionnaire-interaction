import logging

from app.data.questionnaires import QUESTIONNAIRES, SESSIONS
from app.models.schemas import Questionnaire, Session

logger = logging.getLogger(__name__)


class InMemoryAdapter:
    """
    Adapter temporaire pour gérer les données
    """

    async def get_sessions(self, api_key: str) -> list[Session]:
        """Retourne la liste de sessions liées à la clé api"""
        user_sessions = list(filter(lambda x: x["api_key"] == api_key, SESSIONS))
        return [Session(**s) for s in user_sessions]

    async def get_questionnaires(self) -> list[Questionnaire]:
        """Retourne la liste de questionnaires dans l'ordre de passage."""
        return sorted(
            [Questionnaire(**q) for q in QUESTIONNAIRES], key=lambda x: x.order
        )
