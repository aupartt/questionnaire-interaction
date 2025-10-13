import "@testing-library/jest-dom";
import { GetSession } from "./GetSession";
import type { ISessionRepository } from "../ports/ISessionRepository";

describe("GetSession", () => {
    it("devrait correctement renvoyer une entity Session", async () => {
        const mockResult = {
            id: 1,
            questionnaireId: 1,
            session: [],
            answers: [],
            currentItem: {
                id: 1,
                name: "foo",
                question: {
                    type: "text",
                    value: "foo",
                },
                content: {
                    type: "text",
                    value: "foo",
                },
            },
        };

        const mockRepo: ISessionRepository = {
            get: jest.fn().mockResolvedValue(mockResult),
        };

        const usecase = new GetSession(mockRepo);

        const res = await usecase.execute("foo", 12);
        expect(res).toHaveProperty("getItemStatus");
    });
});
