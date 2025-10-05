from app.models.common import StatusEnum
from app.models.schemas import QuestionnaireStatus
from app.service.protocol.data_adapter_protocol import DataAdapterProtocol


class QuestionnaireService:
    def __init__(self, data_adapter: DataAdapterProtocol):
        self.data_adapter = data_adapter

    async def get_questionnaires(self, api_key: str) -> list[QuestionnaireStatus]:
        """Retourne la listes des questionnaires avec l'état des sessions"""
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
