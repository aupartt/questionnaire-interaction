import type { Answer, AnswerResponse } from "../entities/Answer";
import type { IAnswerRepository } from "../ports/IAnswerRepository";

export class SubmitAnswer {
    constructor(private repo: IAnswerRepository) {}

    async execute(
        apiKey: string,
        sessionId: string,
        questionnaireId: string,
        answerData: Answer,
    ): Promise<AnswerResponse> {
        const nextItem = await this.repo.getNext(
            apiKey,
            sessionId,
            questionnaireId,
            answerData,
        );
        return nextItem;
    }
}
