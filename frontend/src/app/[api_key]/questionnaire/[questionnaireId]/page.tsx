'use client';

import { useParams } from 'next/navigation';

import { useSession } from '@/ui/hooks/useSession';
import { QuestionnaireApiRepository } from '@/adapters/api/QuestionnaireApiRepository';

const questionnaireRepository = new QuestionnaireApiRepository()

export default function QuestionnairePage() {
    const params = useParams<{ api_key: string, questionnaireId: string }>()
    const { session, loading, error } = useSession(params.api_key, params.questionnaireId, questionnaireRepository)

    return (
        <main className="container mx-auto p-4">
            {session &&
                <ul>
                    <li>{session.id}</li>
                    <li>{session.questionnaireId}</li>
                    <li>Items:<ol>{session.items.map(el => <ul key={el.id}>{el.name}</ul>)}</ol></li>
                    <li>Réponses:<ol>{session.answers.map(el => <ul key={el.itemId}>{el.itemId}: {el.value}</ul>)}</ol></li>
                    <li>{session.currentItem.name}</li>
                </ul>
            }
            {error && <p>{error}</p>}
        </main>
    )
}