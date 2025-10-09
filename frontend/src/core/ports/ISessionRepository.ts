import type { Session } from "../entities/Session";

export interface ISessionRepository {
    get(apiKey: string, questionnaireId: number): Promise<Session>;
}
