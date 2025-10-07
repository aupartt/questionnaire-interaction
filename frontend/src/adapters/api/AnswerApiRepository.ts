import { IAnswerRepository } from '@/core/ports/IAnswerRepository';
import { AnswerResponse } from '@/core/entities/Answer';
import { ApiNotReachableError } from './errors';

export class AnswerApiRepository implements IAnswerRepository {
    private apiUrl = `${process.env.NEXT_PUBLIC_API_URL}`;

    async getNext(apiKey: string, sessionId: string, questionnaireId: string): Promise<AnswerResponse> {
        const response = await fetch(`${this.apiUrl}/questionnaire/${questionnaireId}/session${sessionId}/answer`, {
            method: 'POST',
            headers: {
                'X-API-Key': apiKey,
            },
        });

        if (!response.ok) {
            throw new ApiNotReachableError()
        }

        const data = await response.json();

        return {
            nextItem: data.next_item,
            resultUrl: data.result_url,
            sessionStatus: data.session_status
        }
    }
}