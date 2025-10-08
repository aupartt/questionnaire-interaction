import type { Questionnaire } from "../entities/Questionnaire";

export interface IQuestionnaireRepository {
    getAll(apiKey: string): Promise<Questionnaire[]>;
}
