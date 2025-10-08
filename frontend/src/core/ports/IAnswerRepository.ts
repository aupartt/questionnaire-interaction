import type { Answer, AnswerResponse } from "../entities/Answer";

export interface IAnswerRepository {
    getNext(
        apiKey: string,
        sessionId: string,
        questionnaireId: string,
        answerData: Answer,
    ): Promise<AnswerResponse>;
}
