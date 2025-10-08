import logging
import random
from datetime import datetime

from app.adapter.data.questionnaires import ITEMS, QUESTIONNAIRES
from app.models.common import ResultStatus, StatusEnum
from app.models.schemas import Answer, AnswerModel, Item, QuestionnaireModel, Result, SessionModel
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

    async def get_questionnaire_by_id(self, questionnaire_id: int) -> QuestionnaireModel | None:
        """Cherche un questionnaire par son id, retourne None si aucun ne correspond."""
        questionnaire = next(filter(lambda q: q["id"] == questionnaire_id, self.questionnaires), None)

        if questionnaire is not None:
            return QuestionnaireModel(**questionnaire)

        return None

    async def get_session_questionnaire(self, api_key: str, questionnaire_id: int) -> SessionModel:
        """Retourne la session pour le questionnaire si elle existe
        Sinon crée une nouvelle session et la retourne"""
        session = next(
            filter(
                lambda x: x["api_key"] == api_key and x["questionnaire_id"] == questionnaire_id,
                self.sessions,
            ),
            None,
        )

        if session is None:
            new_session = SessionModel(
                id=random.randint(0, 9999),
                api_key=api_key,
                questionnaire_id=questionnaire_id,
                status=StatusEnum.ACTIVE,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            self.sessions.append(new_session.model_dump())
            logger.info(f"Création d'une nouvelle session avec l'ID {new_session.id}.")
            return new_session

        return SessionModel(**session)

    async def get_items(self, questionnaire_id: int) -> list[Item]:
        """Retourne la liste d'item pour un questionnaire dans l'ordre"""
        item_list = list(filter(lambda x: x["questionnaire_id"] == questionnaire_id, self.items))

        return [Item(**item) for item in sorted(item_list, key=lambda x: x["order"])]

    async def get_answers(self, session_id: int) -> list[Answer]:
        """Retourne toutes les réponse d'une session"""
        answer_list = list(filter(lambda x: x["session_id"] == session_id, self.answers))

        return [Answer(**answer) for answer in answer_list]

    async def save_answer(self, session_id: int, answer: Answer, session_status: StatusEnum | None) -> Result:
        """Sauvegarde la réponse et update le status de la session"""
        # Vérifie que la session existe
        session_idx = next((i for i, session in enumerate(self.sessions) if session["id"] == session_id), None)
        if session_idx is None:
            logger.warning(f"La session {session_id} n'existe pas: {self.sessions}")
            return Result(status=ResultStatus.ERROR, message="ID de session introuvable")

        # Sauvegarde la réponse
        new_answer = AnswerModel(
            id=random.randint(0, 9999),
            session_id=session_id,
            item_id=answer.item_id,
            value=answer.value,
            status=answer.status,
        )
        self.answers.append(new_answer.model_dump())

        # Update le status de la session si nécessaire
        if session_status is not None:
            self.sessions[session_idx]["status"] = session_status
            self.sessions[session_idx]["updated_at"] = datetime.now().isoformat()

        return Result(status=ResultStatus.SUCCESS, message="Réponse sauvegardé")
