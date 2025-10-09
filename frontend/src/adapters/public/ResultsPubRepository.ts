import type { Results } from "@/core/entities/Results";
import type { IResultsRepository } from "@/core/ports/IResultsRepository";


export class ResultsPubRepository implements IResultsRepository {
    async get(
        apiKey: string,
        questionnaireId: number,
        sessionId: number,
    ): Promise<Results> {
        const response = await fetch(
            `/api/session/results?apiKey=${apiKey}&questionnaireId=${questionnaireId}&sessionId=${sessionId}`
        );

        if (!response.ok) {
            throw new Error("Erreur lors de la récupération de la Session.");
        }

        return await response.json();
    }
}
