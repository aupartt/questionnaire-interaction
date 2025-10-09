from fastapi import Depends

from app.adapter import QuestionnaireRepository, SessionRepository
from app.schema import QuestionnaireStatus
from app.schema.common import StatusEnum


class QuestionnaireService:
    def __init__(
        self,
        questionnaire_repo: QuestionnaireRepository = Depends(QuestionnaireRepository),
        session_repo: SessionRepository = Depends(SessionRepository),
    ):
        self.questionnaire_repo = questionnaire_repo
        self.session_repo = session_repo

    async def get_questionnaires(self, user_id: int) -> list[QuestionnaireStatus]:
        """Retourne la listes des questionnaires avec l'état des sessions

        Args
            - api_key (str): La clé API de l'utilisateur

        Returns
            list[QuestionnaireStatus]: La liste des questionnaires avec leur status
        """
        user_sessions = await self.session_repo.get_sessions(user_id)
        _questionnaires = await self.questionnaire_repo.get_questionnaires()

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
