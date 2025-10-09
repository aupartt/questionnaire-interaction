import type { Questionnaire } from "@/core/entities/Questionnaire";
import type { IQuestionnaireRepository } from "@/core/ports/IQuestionnaireRepository";
import { ApiNotReachableError } from "./errors";

type ItemResponse = {
    id: number;
    name: string;
    description: string;
    session_id: number;
    status: string;
    is_next: boolean;
};

export class QuestionnaireApiRepository implements IQuestionnaireRepository {
    private apiUrl = `${process.env.API_URL}`;
    private apiKeyName = `${process.env.API_KEY_NAME}`;

    async getAll(
        apiKey: string
    ): Promise<Questionnaire[]> {
        const response = await fetch(`${this.apiUrl}/questionnaires`, {
            headers: {
                [this.apiKeyName]: apiKey,
            },
        });

        if (!response.ok) {
            throw new ApiNotReachableError();
        }

        const data = await response.json();

        // Transformation snake_case → camelCase
        return data.map((item: ItemResponse) => ({
            id: item.id,
            name: item.name,
            description: item.description,
            sessionId: item.session_id,
            status: item.status,
            isNext: item.is_next,
        }));
    }
}
