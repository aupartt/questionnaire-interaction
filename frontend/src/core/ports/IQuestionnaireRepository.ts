import { Questionnaire } from '../entities/Questionnaire';
import { Session } from '../entities/Session';

export interface IQuestionnaireRepository {
    getAll(apiKey: string): Promise<Questionnaire[]>;
    getSession(apiKey: string, questionnaireId: string): Promise<Session>;
}