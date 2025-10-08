from fastapi import HTTPException, status

from app.schema import Answer, ItemShort, NextItemResponse, QuestionnaireStatus, Session
from app.schema.common import StatusEnum
from app.service.protocol.data_adapter_protocol import DataAdapterProtocol


class QuestionnaireService:
    def __init__(self, data_adapter: DataAdapterProtocol):
        self.data_adapter = data_adapter

    async def get_questionnaires(self, api_key: str) -> list[QuestionnaireStatus]:
        """Retourne la listes des questionnaires avec l'état des sessions

        Args
            - api_key (str): La clé API de l'utilisateur

        Returns
            list[QuestionnaireStatus]: La liste des questionnaires avec leur status
        """
        user_sessions = await self.data_adapter.get_sessions(api_key)
        _questionnaires = await self.data_adapter.get_questionnaires()

        session_by_qid = {s.questionnaire_id: s for s in user_sessions}

        # On ajoute les sessions existantes aux questionnaires
        last_completed: int | None = None
        active_session: int | None = None
        questionnaires: list[QuestionnaireStatus] = []
        for idx, q in enumerate(_questionnaires):
            session = session_by_qid.get(q.id)
            is_completed = session is not None and session.status != StatusEnum.ACTIVE
            is_active = session is not None and session.status == StatusEnum.ACTIVE

            if is_completed:
                last_completed = idx
            elif is_active:
                active_session = idx

            questionnaires.append(
                QuestionnaireStatus(
                    id=q.id,
                    name=q.name,
                    description=q.description,
                    session_id=session.id if session else None,
                    status=session.status if session else None,
                    is_next=is_active,
                )
            )

        # Ajoute le status 'is_next' au prochain questionnaire
        # si aucun questionnaire n'a été marqué comme actif
        if active_session is None and last_completed is not None:
            next_idx = last_completed + 1
            if next_idx < len(questionnaires):
                questionnaires[next_idx].is_next = True
        elif len(questionnaires) > 0:
            questionnaires[0].is_next = True

        return questionnaires

    async def get_session(self, api_key: str, questionnaire_id: int) -> Session:
        """Vérifie si une session existe déjà pour le questionnaire, sinon crée une nouvelle session.

        Args
            - api_key (str): La clé API de l'utilisateur
            - questionnaire_id: L'id du questionnaire à récupérer

        Returns:
            Session: La session pour le questionnaire
        """

        questionnaire = await self.data_adapter.get_questionnaire_by_id(questionnaire_id=questionnaire_id)

        if questionnaire is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Aucun Questionnaire ne correspond à l'identifiant {questionnaire_id}.",
            )

        session_model = await self.data_adapter.get_session_questionnaire(
            api_key=api_key, questionnaire_id=questionnaire_id
        )

        items = await self.data_adapter.get_items(questionnaire_id=questionnaire_id)
        answers = await self.data_adapter.get_answers(session_id=session_model.id)

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

    async def add_answer(self, questionnaire_id: int, session_id: int, answer: Answer) -> NextItemResponse:
        """Sauvegarde la réponse et retourne le prochain item du questionnaire s'il y en a un
        Sinon retourne"""

        items = await self.data_adapter.get_items(questionnaire_id=questionnaire_id)

        # Récupère l'index de l'item (Answer)
        current_index = next((i for i, item in enumerate(items) if item.id == answer.item_id), None)

        # Cas où l'index de l'Item n'a pas été trouvé
        if current_index is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"L'identifiant d'Item {answer.item_id} spécifié dans le corp de la requête n'existe pas pour le questionnaire {questionnaire_id}.",
            )

        # C'est le dernier item du questionnaire
        next_item = None
        session_status = StatusEnum.COMPLETED
        result_url = f"/questionnaire/{questionnaire_id}/session/{session_id}/results"

        if current_index < len(items) - 1:
            next_item = items[current_index + 1]
            session_status = StatusEnum.ACTIVE
            result_url = None

        # Sauvegarde la réponse et update le status de la session
        res = await self.data_adapter.save_answer(session_id=session_id, answer=answer, session_status=session_status)
        if res.status == "error":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res.message)

        return NextItemResponse(next_item=next_item, session_status=session_status, result_url=result_url)
