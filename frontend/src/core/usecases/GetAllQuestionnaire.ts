import { Questionnaire } from '../entities/Questionnaire';
import { IQuestionnaireRepository } from '../ports/IQuestionnaireRepository';


export class GetSession {
    constructor(
        private readonly repo: IQuestionnaireRepository
    ) { }

    async execute(apiKey: string): Promise<Questionnaire[]> {
        const questionnaires = await this.repo.getAll(apiKey)
        return questionnaires
    }
}