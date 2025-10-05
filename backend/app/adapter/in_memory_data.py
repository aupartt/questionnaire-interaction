import logging
import uuid
from datetime import datetime

from app.adapter.data.questionnaires import ITEMS, QUESTIONNAIRES
from app.models.common import StatusEnum
from app.models.schemas import Answer, AnswerModel, Item, QuestionnaireModel, SessionModel
from app.service.protocol.data_adapter_protocol import DataAdapterProtocol

logger = logging.getLogger(__name__)


class InMemoryAdapter(DataAdapterProtocol):
    """
    Adapter temporaire pour gérer les données
    """

    def __init__(self) -> None:
        super().__init__()
        self.sessions = []
        self.answers = []
        self.questionnaires = QUESTIONNAIRES
        self.items = ITEMS

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

    async def get_session_questionnaire(self, api_key: str, questionnaire_id: str) -> SessionModel:
        """Retourne la session pour le questionnaire si elle existe
        Sinon crée une nouvelle session et la retourne"""
        session_list = list(
            filter(
                lambda x: x["api_key"] == api_key and x["questionnaire_id"] == questionnaire_id,
                self.sessions,
            )
        )

        if len(session_list) == 0:
            new_session = SessionModel(
                id=str(uuid.uuid4()),
                api_key=api_key,
                questionnaire_id=questionnaire_id,
                status=StatusEnum.ACTIVE,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            self.sessions.append(new_session.model_dump())
            return new_session

        return SessionModel(**session_list[0])

    async def get_items(self, questionnaire_id: str) -> list[Item]:
        """Retourne la liste d'item pour un questionnaire dans l'ordre"""
        item_list = list(filter(lambda x: x["questionnaire_id"] == questionnaire_id, self.items))

        return [Item(**item) for item in sorted(item_list, key=lambda x: x["order"])]

    async def get_answers(self, session_id: str) -> list[Answer]:
        """Retourne toutes les réponse d'une session"""
        answer_list = list(filter(lambda x: x["session_id"] == session_id, self.answers))

        return [Answer(**answer) for answer in answer_list]

    async def save_answer(self, session_id: str, answer: Answer) -> bool:
        """Sauvegarde la réponse"""
        new_answer = AnswerModel(
            id=str(uuid.uuid4()),
            session_id=session_id,
            item_id=answer.item_id,
            value=answer.value,
            status=answer.status,
        )
        self.answers.append(new_answer.model_dump())
        return True
