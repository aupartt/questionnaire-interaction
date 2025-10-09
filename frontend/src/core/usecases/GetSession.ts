import { Session } from "../entities/Session";
import type { ISessionRepository } from "../ports/ISessionRepository";

export class GetSession {
    constructor(private readonly repo: ISessionRepository) {}

    async execute(
        apiKey: string,
        questionnaireId: number,
    ): Promise<Session | null> {
        const session = await this.repo.get(apiKey, questionnaireId);

        return new Session(
            session.id,
            session.questionnaireId,
            session.items,
            session.answers,
            session.currentItem,
        );
    }
}
