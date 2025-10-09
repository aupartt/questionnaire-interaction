import type { Questionnaire } from "../entities/Questionnaire";
import type { IQuestionnaireRepository } from "../ports/IQuestionnaireRepository";

export class GetAllQuestionnaire {
    constructor(private readonly repo: IQuestionnaireRepository) {}

    async execute(apiKey: string): Promise<Questionnaire[]> {
        const questionnaires = await this.repo.getAll(apiKey);
        return questionnaires;
    }
}
