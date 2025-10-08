import { IAnswerRepository } from "@/core/ports/IAnswerRepository";
import { Answer, AnswerResponse } from "@/core/entities/Answer";
import { ApiNotReachableError } from "./errors";

export class AnswerApiRepository implements IAnswerRepository {
    private apiUrl = `${process.env.NEXT_PUBLIC_API_URL}`;

    async getNext(
        apiKey: string,
        sessionId: string,
        questionnaireId: string,
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
                    "X-API-Key": apiKey,
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
