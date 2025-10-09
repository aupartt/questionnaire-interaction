import type { Session } from "@/core/entities/Session";
import type { ISessionRepository } from "@/core/ports/ISessionRepository";

export class SessionPubRepository implements ISessionRepository {
    async get(apiKey: string, questionnaireId: number): Promise<Session> {
        const response = await fetch(
            `/api/session?apiKey=${apiKey}&questionnaireId=${questionnaireId}`,
        );

        if (!response.ok) {
            throw new Error("Erreur lors de la récupération de la Session.");
        }

        return await response.json();
    }
}
