import { Session } from '../entities/Session';

export interface ISessionRepository {
    get(apiKey: string, questionnaireId: string): Promise<Session>;
}