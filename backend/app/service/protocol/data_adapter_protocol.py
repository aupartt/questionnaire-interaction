from typing import Protocol

from app.models.common import StatusEnum
from app.models.schemas import Answer, Item, QuestionnaireModel, Result, SessionModel


class DataAdapterProtocol(Protocol):
    async def get_sessions(self, api_key: str) -> list[SessionModel]:
        """Retourne toutes les sessions d'un utilisateur."""
        ...

    async def get_questionnaires(self) -> list[QuestionnaireModel]:
        """Retourne la liste de questionnaires dans l'ordre de passage."""
        ...

    async def get_questionnaire_by_id(self, questionnaire_id: int) -> QuestionnaireModel | None:
        """Cherche un questionnaire par son id, retourne None si aucun ne correspond."""
        ...

    async def get_session_questionnaire(self, api_key: str, questionnaire_id: int) -> SessionModel:
        """Retourne la session pour le questionnaire si elle existe
        Sinon crée une nouvelle session et la retourne"""
        ...

    async def get_items(self, questionnaire_id: int) -> list[Item]:
        """Retourne la liste d'items d'un questionnaire dans l'ordre de passage"""
        ...

    async def get_answers(self, session_id: int) -> list[Answer]:
        """Retourne la liste de réponse pour une session"""
        ...

    async def save_answer(self, session_id: int, answer: Answer, session_status: StatusEnum) -> Result:
        """Sauvegarde la réponse dans la base de données et update la session"""
        ...
