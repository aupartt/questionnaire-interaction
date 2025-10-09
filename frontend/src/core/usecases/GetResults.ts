import type { Results } from "../entities/Results";
import type { IResultsRepository } from "../ports/IResultsRepository";

export class GetResults {
    constructor(private readonly repo: IResultsRepository) {}

    async execute(
        apiKey: string,
        questionnaireId: number,
        sessionId: number,
    ): Promise<Results> {
        const results = await this.repo.get(apiKey, questionnaireId, sessionId);
        return results;
    }
}
