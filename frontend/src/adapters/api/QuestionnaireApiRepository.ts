import { IQuestionnaireRepository } from "@/core/ports/IQuestionnaireRepository";
import { Questionnaire } from "@/core/entities/Questionnaire";
import { ApiNotReachableError } from "./errors";

export class QuestionnaireApiRepository implements IQuestionnaireRepository {
    private apiUrl = `${process.env.NEXT_PUBLIC_API_URL}`;

    async getAll(apiKey: string): Promise<Questionnaire[]> {
        const response = await fetch(`${this.apiUrl}/questionnaires`, {
            headers: {
                "X-API-Key": apiKey,
            },
        });

        if (!response.ok) {
            throw new ApiNotReachableError();
        }

        const data = await response.json();

        // Transformation snake_case → camelCase
        return data.map((item: any) => ({
            id: item.id,
            name: item.name,
            description: item.description,
            sessionId: item.session_id,
            status: item.status,
            isNext: item.is_next,
        }));
    }
}
