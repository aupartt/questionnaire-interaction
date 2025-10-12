from fastapi import Depends, HTTPException, status

from app.adapter import AnswerRepository, ItemRepository
from app.schema import Answer, NextItemResponse
from app.schema.common import StatusEnum


class AnswerService:
    def __init__(
        self,
        answer_repo: AnswerRepository = Depends(AnswerRepository),
        item_repo: ItemRepository = Depends(ItemRepository),
    ):
        self.answer_repo = answer_repo
        self.item_repo = item_repo

    async def add_answer(self, questionnaire_id: int, session_id: int, answer: Answer) -> NextItemResponse:
        """Sauvegarde la réponse et retourne le prochain item du questionnaire s'il y en a un
        Sinon retourne"""

        items = await self.item_repo.get_items(questionnaire_id=questionnaire_id)

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
        db_answer = await self.answer_repo.get_answer_by_id(session_id=session_id, item_id=answer.item_id)
        if db_answer is not None and db_answer.id:
            success = await self.answer_repo.update_answer(answer_id=db_answer.id, answer=answer)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Impossible de mettre à jour la réponse {db_answer.id}",
                )
        else:
            res = await self.answer_repo.save_answer(
                session_id=session_id, answer=answer, session_status=session_status
            )
            if res.status == "error":
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res.message)

        return NextItemResponse(next_item=next_item, session_status=session_status, result_url=result_url)
