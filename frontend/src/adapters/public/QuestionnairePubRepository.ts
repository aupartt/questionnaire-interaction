import type { Questionnaire } from "@/core/entities/Questionnaire";
import type { IQuestionnaireRepository } from "@/core/ports/IQuestionnaireRepository";

export class QuestionnairePubRepository implements IQuestionnaireRepository {
    async getAll(
        apiKey: string
    ): Promise<Questionnaire[]> {
        const response = await fetch(`/api/questionnaires?apiKey=${apiKey}`);

        if (!response.ok) {
            throw new Error("Erreur lors de la récupération des questionnaires");
        }

        return await response.json()
    }
}
