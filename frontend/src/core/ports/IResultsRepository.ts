import type { Results } from "../entities/Results";

export interface IResultsRepository {
    get(apiKey: string, questionnaireId: number, sessionId: number): Promise<Results>;
}
