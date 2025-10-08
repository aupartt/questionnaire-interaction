import { IAnswerRepository } from "@/core/ports/IAnswerRepository";
import { AnswerResponse } from "@/core/entities/Answer";

export class MockAnswerRepository implements IAnswerRepository {
    private answerResponse = {
        nextItem: {
            id: "1",
            name: "foo",
            question: {
                type: "text",
                value: "Yahoo",
            },
            content: {
                type: "text",
                likertValue: null,
            },
        },
        resultUrl: null,
        sessionStatus: "active",
    };

    async getNext(): Promise<AnswerResponse> {
        return Promise.resolve(this.answerResponse);
    }
}
