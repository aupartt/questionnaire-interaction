import type { Questionnaire } from "@/core/entities/Questionnaire";
import type { IQuestionnaireRepository } from "@/core/ports/IQuestionnaireRepository";

export class MockQuestionnaireRepository implements IQuestionnaireRepository {
    private questionnaires: Questionnaire[] = [
        {
            id: 1,
            name: "Information utilisateur",
            description: "Vos informations.",
            sessionId: 123,
            status: "completed",
            isNext: false,
        },
        {
            id: 2,
            name: "Préférences",
            description: "Vos attentes professionnelles.",
            sessionId: 23,
            status: "active",
            isNext: true,
        },
    ];

    async getAll(): Promise<Questionnaire[]> {
        return Promise.resolve(this.questionnaires);
    }
}
