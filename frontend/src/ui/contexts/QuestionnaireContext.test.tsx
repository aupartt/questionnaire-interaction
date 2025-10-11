
import { renderHook, act, render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QuestionnaireProvider, useQuestionnaireContext } from './QuestionnaireContext';
import { Questionnaire } from '@/core/entities/Questionnaire';


// Fonction utilitaire pour créer des questionnaires mock
const createMockQuestionnaire = (id: number, isNext: boolean = false): Questionnaire => ({
    id: id,
    name: "nameFoo",
    description: "DescFoo",
    sessionId: 1,
    status: "active",
    isNext: isNext
});

// Composant de test qui consomme le contexte
const TestConsumer = () => {
    const { questionnaires, nextQuestionnaire } = useQuestionnaireContext();
    const nextId = nextQuestionnaire ? nextQuestionnaire.id : 'none';

    return (
        <>
            <div data-testid="questionnaires-count">{questionnaires.length}</div>
            <div data-testid="next-id">{nextId}</div>
        </>
    );
};

describe('QuestionnaireContext', () => {

    // Test 1: Vérifie que le hook lève une erreur si utilisé hors du Provider
    it('should throw an error when used outside of Provider', () => {
        expect(() => {
            render(<TestConsumer />)
        }).toThrow(Error('useQuestionnaireContext must be used within a QuestionnaireProvider'))
    });

    // Test 2: Vérifie que le Provider expose les questionnaires et le 'nextQuestionnaire' correct
    it('should expose the correct questionnaires list and identify the next questionnaire', () => {
        const mockQ = [
            createMockQuestionnaire(1, false),
            createMockQuestionnaire(2, true), // Celui-ci est 'isNext'
            createMockQuestionnaire(3, false),
        ];

        render(
            <QuestionnaireProvider questionnaires={mockQ}>
                <TestConsumer />
            </QuestionnaireProvider>
        );

        // Vérification de la liste
        expect(screen.getByTestId('questionnaires-count')).toHaveTextContent('3');

        // Vérification du 'nextQuestionnaire' (basé sur le premier `q.isNext` trouvé)
        expect(screen.getByTestId('next-id')).toHaveTextContent('2');
    });

    // Test 3: Vérifie que 'nextQuestionnaire' est null si aucun n'a 'isNext'
    it('should set nextQuestionnaire to null if none is marked as isNext', () => {
        const mockQ = [
            createMockQuestionnaire(1, false),
            createMockQuestionnaire(2, false),
        ];

        render(
            <QuestionnaireProvider questionnaires={mockQ}>
                <TestConsumer />
            </QuestionnaireProvider>
        );

        expect(screen.getByTestId('next-id')).toHaveTextContent('none');
    });

    // Test 4: Vérifie que 'nextQuestionnaire' est null si la liste est vide
    it('should set nextQuestionnaire to null if the list is empty', () => {
        render(
            <QuestionnaireProvider questionnaires={[]}>
                <TestConsumer />
            </QuestionnaireProvider>
        );

        expect(screen.getByTestId('next-id')).toHaveTextContent('none');
        expect(screen.getByTestId('questionnaires-count')).toHaveTextContent('0');
    });

    // Test 5: Vérifie le comportement de mise à jour (l'effet de bord)
    it('should update nextQuestionnaire when the questionnaires prop changes', () => {
        const initialQ = [
            createMockQuestionnaire(1, true),
            createMockQuestionnaire(2, false)

        ];
        const { rerender } = render(
            <QuestionnaireProvider questionnaires={initialQ}>
                <TestConsumer />
            </QuestionnaireProvider>
        );

        // Initialement, il est 'none' (car `isNext` est false par défaut)
        expect(screen.getByTestId('questionnaires-count')).toHaveTextContent('2');
        expect(screen.getByTestId('next-id')).toHaveTextContent('1');

        // On passe au prochain questionnaire
        const updatedQ = [
            createMockQuestionnaire(1, false),
            createMockQuestionnaire(2, true)
        ];

        // Rerender le Provider avec la nouvelle prop
        rerender(
            <QuestionnaireProvider questionnaires={updatedQ}>
                <TestConsumer />
            </QuestionnaireProvider>
        );

        // Vérifie que l'effet a été déclenché et que l'état interne a été mis à jour
        expect(screen.getByTestId('questionnaires-count')).toHaveTextContent('2');
        expect(screen.getByTestId('next-id')).toHaveTextContent('2');
    });
});
