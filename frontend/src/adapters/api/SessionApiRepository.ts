import { Session } from "@/core/entities/Session";
import type { ISessionRepository } from "@/core/ports/ISessionRepository";
import { ApiNotReachableError } from "./errors";

export class SessionApiRepository implements ISessionRepository {
    private apiUrl = `${process.env.NEXT_PUBLIC_API_URL}`;

    async get(apiKey: string, questionnaireId: number): Promise<Session> {
        const response = await fetch(
            `${this.apiUrl}/questionnaire/${questionnaireId}/session`,
            {
                method: "POST",
                headers: {
                    "X-API-Key": apiKey,
                },
            },
        );

        if (!response.ok) {
            throw new ApiNotReachableError();
        }

        const data = await response.json();

        return new Session(
            data.id,
            data.questionnaire_id,
            data.items,
            data.answers,
            data.current_item,
        );
    }
}
