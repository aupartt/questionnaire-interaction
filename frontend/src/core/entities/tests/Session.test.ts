import type { Answer } from "../Answer";
import { Session } from "../Session";

describe("Session Entity", () => {
    it("devrait créer une session valide", () => {
        const item = {
            id: "1",
            name: "Foo",
            question: {
                type: "text",
                value: "Foo",
            },
            content: {
                type: "text",
                likertValue: null,
            },
        };
        const session: Session = new Session("1", "1", [item], [], item);

        expect(session.id).toBe("1");
        expect(session.currentItem.name).toBe("Foo");
        expect(session.items).toHaveLength(1);
        expect(session.answers).toHaveLength(0);
    });

    it("devrait correctement ajouter une réponse", () => {
        const item = {
            id: "1",
            name: "Foo",
            question: {
                type: "text",
                value: "Foo",
            },
            content: {
                type: "text",
                likertValue: null,
            },
        };
        const session: Session = new Session("1", "1", [item], [], item);

        expect(session.answers).toHaveLength(0);

        const newAnswer = {
            itemId: "1",
            value: "Bar",
            status: "completed",
        } as Answer;

        session.addAnswer(newAnswer);

        expect(session.answers).toHaveLength(1);
        expect(session.answers[0].itemId).toBe("1");
    });

    it("devrait correctement mettre à jours une réponse", () => {
        const item = {
            id: "1",
            name: "Foo",
            question: {
                type: "text",
                value: "Foo",
            },
            content: {
                type: "text",
                likertValue: null,
            },
        };
        const session: Session = new Session(
            "1",
            "1",
            [item],
            [
                {
                    itemId: "1",
                    value: "Bar",
                    status: "skipped",
                },
            ],
            item,
        );

        expect(session.answers).toHaveLength(1);
        expect(session.answers[0]).toStrictEqual({
            itemId: "1",
            value: "Bar",
            status: "skipped",
        });

        const newAnswer = {
            itemId: "1",
            value: "Baz",
            status: "completed",
        } as Answer;

        session.addAnswer(newAnswer);

        expect(session.answers).toHaveLength(1);
        expect(session.answers[0]).toStrictEqual({
            itemId: "1",
            value: "Baz",
            status: "completed",
        });
    });

    it("devrait retourner le status de l'Item", () => {
        const item1 = {
            id: "1",
            name: "Foo",
            question: {
                type: "text",
                value: "Foo",
            },
            content: {
                type: "text",
                likertValue: null,
            },
        };
        const item2 = item1;
        item2.id = "2";

        const session: Session = new Session(
            "1",
            "1",
            [item1, item2],
            [
                {
                    itemId: "1",
                    value: "Bar",
                    status: "skipped",
                },
            ],
            item1,
        );

        const itemStatus1 = session.getItemStatus("1");
        const itemStatus2 = session.getItemStatus("2");

        expect(itemStatus1).toBe("skipped");
        expect(itemStatus2).toBe(null);
    });
});
