from fastapi import Depends, HTTPException, status

from app.adapter import AnswerRepository, ItemRepository, QuestionnaireRepository, SessionRepository
from app.schema import ItemShort, Session


class SessionService:
    def __init__(
        self,
        answer_repo: AnswerRepository = Depends(AnswerRepository),
        item_repo: ItemRepository = Depends(ItemRepository),
        questionnaire_repo: QuestionnaireRepository = Depends(QuestionnaireRepository),
        session_repo: SessionRepository = Depends(SessionRepository),
    ):
        self.answer_repo = answer_repo
        self.item_repo = item_repo
        self.questionnaire_repo = questionnaire_repo
        self.session_repo = session_repo

    async def get_session(self, user_id: int, questionnaire_id: int) -> Session:
        """Vérifie si une session existe déjà pour le questionnaire, sinon crée une nouvelle session.

        Args
            - api_key (str): La clé API de l'utilisateur
            - questionnaire_id: L'id du questionnaire à récupérer

        Returns:
            Session: La session pour le questionnaire
        """

        questionnaire = await self.questionnaire_repo.get_questionnaire_by_id(questionnaire_id=questionnaire_id)

        if questionnaire is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Aucun Questionnaire ne correspond à l'identifiant {questionnaire_id}.",
            )

        session_model = await self.session_repo.get_session_questionnaire(
            user_id=user_id, questionnaire_id=questionnaire_id
        )

        if session_model is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Impossible de récupérer une Session."
            )

        items = await self.item_repo.get_items(questionnaire_id=questionnaire_id)
        answers = await self.answer_repo.get_answers(session_id=session_model.id)

        # Item dédié à l'affichage front
        items_short = [ItemShort(id=item.id, name=item.name) for item in items]

        # TODO: Définir le prochain item (si c'est une reprise de session afin de ne pas juste renvoyer l'item 1)

        return Session(
            id=session_model.id,
            questionnaire_id=questionnaire_id,
            items=items_short,
            answers=answers,
            current_item=items[0],
        )
