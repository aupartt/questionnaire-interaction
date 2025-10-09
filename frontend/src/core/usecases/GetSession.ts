import type { Session } from "../entities/Session";
import type { ISessionRepository } from "../ports/ISessionRepository";

export class GetSession {
    constructor(private readonly repo: ISessionRepository) {}

    async execute(
        apiKey: string,
        questionnaireId: number,
    ): Promise<Session | null> {
        const session = await this.repo.get(apiKey, questionnaireId);
        return session;
    }
}
