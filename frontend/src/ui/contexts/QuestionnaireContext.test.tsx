import { waitFor, act, render, screen, cleanup } from "@testing-library/react";
import "@testing-library/jest-dom";
import {
    QuestionnaireProvider,
    useQuestionnaireContext,
} from "./QuestionnaireContext";
import { Questionnaire } from "@/core/entities/Questionnaire";

// Fonction utilitaire pour créer des questionnaires mock
const createMockQuestionnaire = (
    id: number,
    isNext: boolean = false,
): Questionnaire => ({
    id: id,
    name: "nameFoo",
    description: "DescFoo",
    sessionId: 1,
    status: "active",
    isNext: isNext,
});

// Composant de test qui consomme le contexte
const TestConsumer = () => {
    const { questionnaires, nextQuestionnaire } = useQuestionnaireContext();
    const nextId = nextQuestionnaire ? nextQuestionnaire.id : "none";

    return (
        <>
            <div data-testid="questionnaires-count">
                {questionnaires?.length}
            </div>
            <div data-testid="next-id">{nextId}</div>
        </>
    );
};

const fetchSpy = jest.spyOn(global, "fetch");
const CreateFetchMock = (status = true, jsonMock?: any) => {
    return fetchSpy.mockImplementation(() =>
        Promise.resolve({
            ok: status,
            json: () => Promise.resolve(jsonMock),
        } as Response),
    );
};

describe("QuestionnaireContext", () => {
    afterEach(() => {
        cleanup();
        jest.restoreAllMocks();
    });

    // Test 1: Vérifie que le hook lève une erreur si utilisé hors du Provider
    it("should throw an error when used outside of Provider", () => {
        CreateFetchMock();
        expect(() => {
            render(<TestConsumer />);
        }).toThrow(
            Error(
                "useQuestionnaireContext must be used within a QuestionnaireProvider",
            ),
        );
    });

    // Test 2: Vérifie que le Provider expose les questionnaires et le 'nextQuestionnaire' correct
    it("should expose the correct questionnaires list and identify the next questionnaire", async () => {
        const mockQ = [
            createMockQuestionnaire(1, false),
            createMockQuestionnaire(2, true), // Celui-ci est 'isNext'
            createMockQuestionnaire(3, false),
        ];
        const fetchMock = CreateFetchMock(true, mockQ);

        render(
            <QuestionnaireProvider apiKey={"foo"}>
                <TestConsumer />
            </QuestionnaireProvider>,
        );

        await waitFor(
            () => {
                expect(
                    screen.getByTestId("questionnaires-count"),
                ).toHaveTextContent("3");
                expect(screen.getByTestId("next-id")).toHaveTextContent("2");
                expect(fetchMock).toHaveBeenCalledWith(
                    expect.stringContaining(`/questionnaires`),
                );
            },
            { timeout: 3000 },
        );
    });

    // Test 3: Vérifie que 'nextQuestionnaire' est null si aucun n'a 'isNext'
    it("should set nextQuestionnaire to null if none is marked as isNext", async () => {
        const mockQ = [
            createMockQuestionnaire(1, false),
            createMockQuestionnaire(2, false),
        ];
        CreateFetchMock(true, mockQ);

        render(
            <QuestionnaireProvider apiKey={"foo"}>
                <TestConsumer />
            </QuestionnaireProvider>,
        );

        await waitFor(
            () => {
                expect(screen.getByTestId("next-id")).toHaveTextContent("none");
            },
            { timeout: 3000 },
        );
    });

    // Test 4: Vérifie que 'nextQuestionnaire' est null si la liste est vide
    it("should set nextQuestionnaire to null if the list is empty", async () => {
        render(
            <QuestionnaireProvider apiKey={"foo"}>
                <TestConsumer />
            </QuestionnaireProvider>,
        );
        CreateFetchMock(true, []);

        await waitFor(
            () => {
                expect(screen.getByTestId("next-id")).toHaveTextContent("none");
                expect(
                    screen.getByTestId("questionnaires-count"),
                ).toHaveTextContent("0");
            },
            { timeout: 3000 },
        );
    });

    // Test 5: Vérifie le comportement de mise à jour (l'effet de bord)
    it("should update nextQuestionnaire when the questionnaires prop changes", async () => {
        const initialQ = [
            createMockQuestionnaire(1, true),
            createMockQuestionnaire(2, false),
        ];
        CreateFetchMock(true, initialQ);
        const { rerender } = render(
            <QuestionnaireProvider apiKey={"foo"}>
                <TestConsumer />
            </QuestionnaireProvider>,
        );

        await waitFor(
            () => {
                expect(
                    screen.getByTestId("questionnaires-count"),
                ).toHaveTextContent("2");
                expect(screen.getByTestId("next-id")).toHaveTextContent("1");
            },
            { timeout: 3000 },
        );

        // On passe au prochain questionnaire
        const updatedQ = [
            createMockQuestionnaire(1, false),
            createMockQuestionnaire(2, true),
        ];
        CreateFetchMock(true, updatedQ);

        // Rerender le Provider avec la nouvelle prop
        rerender(
            <QuestionnaireProvider apiKey={"bar"}>
                <TestConsumer />
            </QuestionnaireProvider>,
        );

        await waitFor(
            () => {
                expect(
                    screen.getByTestId("questionnaires-count"),
                ).toHaveTextContent("2");
                expect(screen.getByTestId("next-id")).toHaveTextContent("2");
            },
            { timeout: 3000 },
        );
    });
});
