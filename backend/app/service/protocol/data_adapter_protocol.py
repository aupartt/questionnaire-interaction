from typing import Protocol

from app.models.schemas import Answer, Item, QuestionnaireModel, SessionModel


class DataAdapterProtocol(Protocol):
    async def get_sessions(self, api_key: str) -> list[SessionModel]:
        """Retourne toutes les sessions d'un utilisateur."""
        ...

    async def get_questionnaires(self) -> list[QuestionnaireModel]:
        """Retourne la liste de questionnaires dans l'ordre de passage."""
        ...
