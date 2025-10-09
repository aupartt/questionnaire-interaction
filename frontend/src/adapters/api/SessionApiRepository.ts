import { Session } from "@/core/entities/Session";
import type { ISessionRepository } from "@/core/ports/ISessionRepository";
import { ApiNotReachableError } from "./errors";

export class SessionApiRepository implements ISessionRepository {
    private apiUrl = `${process.env.API_URL}`;
    private apiKeyName = `${process.env.API_KEY_NAME}`;

    async get(apiKey: string, questionnaireId: number): Promise<Session> {
        const response = await fetch(
            `${this.apiUrl}/questionnaire/${questionnaireId}/session`,
            {
                method: "POST",
                headers: {
                    [this.apiKeyName]: apiKey,
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
