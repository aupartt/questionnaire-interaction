from typing import Protocol

from app.models.schemas import Questionnaire, Session


class DataAdapterProtocol(Protocol):
    async def get_sessions(self, api_key: str) -> list[Session]: ...

    async def get_questionnaires(self) -> list[Questionnaire]:
        """Retourne la liste de questionnaires dans l'ordre de passage."""
        ...
