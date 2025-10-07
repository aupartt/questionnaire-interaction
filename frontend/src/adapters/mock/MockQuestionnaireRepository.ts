import { IQuestionnaireRepository } from '@/core/ports/IQuestionnaireRepository';
import { Questionnaire } from '@/core/entities/Questionnaire';

export class MockQuestionnaireRepository implements IQuestionnaireRepository {
    private questionnaires: Questionnaire[] = [
        {
            id: '1',
            name: 'Information utilisateur',
            description: 'Vos informations.',
            sessionId: 'session-123',
            status: 'completed',
            isNext: false,
        },
        {
            id: '2',
            name: 'Préférences',
            description: 'Vos attentes professionnelles.',
            sessionId: 'session-123',
            status: 'active',
            isNext: true,
        }
    ]

    async getAll(): Promise<Questionnaire[]> {
        return Promise.resolve(this.questionnaires)
    }
}