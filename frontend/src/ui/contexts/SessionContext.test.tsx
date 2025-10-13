import {
    act,
    cleanup,
    render,
    renderHook,
    screen,
    waitFor,
} from "@testing-library/react";
import "@testing-library/jest-dom";
import { type ReactNode, useEffect } from "react";
import { SessionProvider, useSessionContext } from "./SessionContext";

const createMockSession = () => ({
    id: 1,
    questionnaireId: 1,
    items: [],
    answers: [],
    currentItem: {
        id: 1,
        name: "Foo",
        question: {
            type: "text",
            value: "Who?",
        },
        content: {
            type: "text",
        },
    },
    status: "active",
});

describe("SessionContext", () => {
    let spyFetch: jest.SpyInstance;

    const TestComponent = ({
        children,
        onRender,
    }: {
        children?: ReactNode;
        onRender: (context: any) => void;
    }) => {
        const context = useSessionContext();
        useEffect(() => {
            onRender(context);
        }, [context, onRender]);
        return <div>{children && children}</div>;
    };

    beforeEach(() => {
        spyFetch = jest.spyOn(global, "fetch");
    });

    afterEach(() => {
        cleanup();
        jest.restoreAllMocks();
    });

    it("devrait envoyer une erreur", async () => {
        spyFetch.mockImplementationOnce(() =>
            Promise.resolve({
                ok: true,
                json: () => Promise.resolve(createMockSession()),
            } as Response),
        );
        await waitFor(() => {
            expect(() => {
                render(<TestComponent onRender={() => null} />);
            }).toThrow(
                Error("useSessionContext must be used within a SessionContext"),
            );
        });
    });

    it("devrait avoir appelé l'api pour récupérer la session", async () => {
        spyFetch.mockImplementationOnce(() =>
            Promise.resolve({
                ok: true,
                json: () => Promise.resolve(createMockSession()),
            } as Response),
        );

        let capturedContext: any;
        const onRender = (context: any) => {
            capturedContext = context;
        };

        render(
            <SessionProvider apiKey="foo" questionnaireId={1}>
                <TestComponent onRender={onRender} />
            </SessionProvider>,
        );

        await waitFor(() => {
            expect(capturedContext.loading).toBe(false);
        });

        expect(spyFetch).toHaveBeenCalledWith(
            expect.stringContaining(`/session?apiKey=foo&questionnaireId=1`),
        );
        expect(capturedContext.session.id).toBe(1);
        expect(capturedContext.session.questionnaireId).toBe(1);
        expect(capturedContext.session.items).toHaveLength(0);
        expect(capturedContext.session.currentItem.name).toBe("Foo");
    });

    it("devrait réinitialiser la session si le questionnaireId change", async () => {
        spyFetch.mockImplementation((url: string) => {
            const params = new URLSearchParams(
                new URL(url, "http://localhost").search,
            );
            const questionnaireId = params.get("questionnaireId");
            if (questionnaireId) {
                const mockSession = createMockSession();
                mockSession.questionnaireId = parseInt(questionnaireId);
                mockSession.currentItem.name =
                    questionnaireId === "1" ? "Foo" : "Bar";
                return Promise.resolve({
                    ok: true,
                    json: () => Promise.resolve(mockSession),
                } as Response);
            }
            return Promise.reject(new Error("Unexpected questionnaireId"));
        });

        let capturedContext: any;
        const onRender = (context: any) => {
            capturedContext = context;
        };

        const { rerender } = render(
            <SessionProvider apiKey="foo" questionnaireId={1}>
                <TestComponent onRender={onRender} />
            </SessionProvider>,
        );

        expect(capturedContext.loading).toBe(true);
        expect(capturedContext.session).toBe(null);

        await waitFor(() => {
            expect(capturedContext.loading).toBe(false);
        });

        expect(spyFetch).toHaveBeenCalledTimes(1);
        expect(capturedContext.session?.id).toBe(1);
        expect(capturedContext.session?.questionnaireId).toBe(1);
        expect(capturedContext.session?.currentItem.name).toBe("Foo");

        rerender(
            <SessionProvider apiKey="foo" questionnaireId={2}>
                <TestComponent onRender={onRender} />
            </SessionProvider>,
        );

        await waitFor(() => {
            expect(capturedContext.loading).toBe(false);
        });

        expect(spyFetch).toHaveBeenCalledTimes(2);
        expect(capturedContext.session?.id).toBe(1);
        expect(capturedContext.session?.questionnaireId).toBe(2); // Received: 1
        expect(capturedContext.session?.currentItem.name).toBe("Bar");
    });

    it("devrait correctement ajouter une réponse", async () => {
        spyFetch.mockImplementationOnce(() =>
            // Initialisation
            Promise.resolve({
                ok: true,
                json: () => Promise.resolve(createMockSession()),
            } as Response),
        );
        const mockNextItem = createMockSession().currentItem;
        mockNextItem.id = 2;
        mockNextItem.name = "Bar";
        spyFetch.mockImplementationOnce(() =>
            // addAnswer
            Promise.resolve({
                ok: true,
                json: () =>
                    Promise.resolve({
                        nextItem: mockNextItem,
                        sessionStatus: "active",
                    }),
            } as Response),
        );

        let capturedContext: any;
        const onRender = (context: any) => {
            capturedContext = context;
        };

        render(
            <SessionProvider apiKey="foo" questionnaireId={1}>
                <TestComponent onRender={onRender} />
            </SessionProvider>,
        );

        await waitFor(() => {
            expect(capturedContext.loading).toBe(false);
            expect(spyFetch).toHaveBeenCalledTimes(1);
        });

        const mockAnswer = {
            itemId: 1,
            value: "Gneugneu",
            status: "completed",
        };

        act(() => {
            capturedContext.addAnswer(mockAnswer);
        });

        await waitFor(() => {
            expect(capturedContext.loading).toBe(false);
        });

        expect(spyFetch).toHaveBeenCalledTimes(2);
        const [url, options] = spyFetch.mock.calls[1];
        expect(url).toBe(
            "/api/session/answer?apiKey=foo&questionnaireId=1&sessionId=1",
        );
        expect(options.method).toBe("POST");
        expect(options.body).toBe(JSON.stringify({ answer: mockAnswer }));

        expect(capturedContext.session.id).toBe(1);
        expect(capturedContext.session.questionnaireId).toBe(1);
        expect(capturedContext.session.answers).toHaveLength(1);
        expect(capturedContext.session.answers[0].value).toBe("Gneugneu");
        expect(capturedContext.session.currentItem.name).toBe("Bar");
    });

    it("devrait correctement supprimer la session", async () => {
        spyFetch.mockImplementationOnce(() =>
            // Initialisation
            Promise.resolve({
                ok: true,
                json: () => Promise.resolve(createMockSession()),
            } as Response),
        );

        let capturedContext: any;
        const onRender = (context: any) => {
            capturedContext = context;
        };

        render(
            <SessionProvider apiKey="foo" questionnaireId={1}>
                <TestComponent onRender={onRender} />
            </SessionProvider>,
        );

        await waitFor(() => {
            expect(capturedContext.loading).toBe(false);
            expect(spyFetch).toHaveBeenCalledTimes(1);
        });

        expect(capturedContext.session).toBeTruthy();

        act(() => {
            capturedContext.clearSession();
        });

        await waitFor(() => {
            expect(capturedContext.session).toBe(null);
        });
    });
});
