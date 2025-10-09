import type { Answer, AnswerResponse } from "@/core/entities/Answer";
import type { IAnswerRepository } from "@/core/ports/IAnswerRepository";
import { ApiNotReachableError } from "./errors";

export class AnswerApiRepository implements IAnswerRepository {
    private apiUrl = `${process.env.API_URL}`;
    private apiKeyName = `${process.env.API_KEY_NAME}`;

    async getNext(
        apiKey: string,
        sessionId: number,
        questionnaireId: number,
        answer: Answer,
    ): Promise<AnswerResponse> {
        const jsonAnswer = JSON.stringify({
            item_id: answer.itemId,
            value: answer.value,
            status: answer.status,
        });
        const response = await fetch(
            `${this.apiUrl}/questionnaire/${questionnaireId}/session/${sessionId}/answer`,
            {
                method: "POST",
                headers: {
                    [this.apiKeyName]: apiKey,
                    "Content-Type": "application/json",
                },
                body: jsonAnswer,
            },
        );

        if (!response.ok) {
            const data = await response.json();
            throw new ApiNotReachableError(data.detail);
        }

        const data = await response.json();

        return {
            nextItem: data.next_item,
            resultUrl: data.result_url,
            sessionStatus: data.session_status,
        };
    }
}
