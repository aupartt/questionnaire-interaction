import type { Answer, AnswerResponse } from "../entities/Answer";

export interface IAnswerRepository {
    getNext(
        apiKey: string,
        sessionId: number,
        questionnaireId: number,
        answerData: Answer,
    ): Promise<AnswerResponse>;
}
