import type { Answer, AnswerResponse } from "@/core/entities/Answer";
import type { IAnswerRepository } from "@/core/ports/IAnswerRepository";

export class AnswerPubRepository implements IAnswerRepository {
    async getNext(
        apiKey: string,
        sessionId: number,
        questionnaireId: number,
        answer: Answer,
    ): Promise<AnswerResponse> {
        const jsonAnswer = JSON.stringify({
            itemId: answer.itemId,
            value: answer.value,
            status: answer.status,
        });

        const response = await fetch(
            `/api/session/answer?apiKey=${apiKey}&questionnaireId=${questionnaireId}&sessionId=${sessionId}`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: jsonAnswer,
            },
        );

        return await response.json();
    }
}
