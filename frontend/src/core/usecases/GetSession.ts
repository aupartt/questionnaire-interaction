import { Session } from "../entities/Session";
import { ISessionRepository } from "../ports/ISessionRepository";

export class GetSession {
    constructor(private readonly repo: ISessionRepository) {}

    async execute(
        apiKey: string,
        questionnaireId: string,
    ): Promise<Session | null> {
        const session = await this.repo.get(apiKey, questionnaireId);
        return session;
    }
}
