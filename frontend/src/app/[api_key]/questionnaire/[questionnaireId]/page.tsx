'use client';

import { useParams } from 'next/navigation';

import { Item } from '@/ui/components/item'
import { useEffect } from 'react';
import { useSessionContext } from '@/ui/contexts/SessionContext'
import { ErrorMessage } from '@/ui/components/ErrorMessage';

export default function QuestionnairePage() {
    const params = useParams<{ questionnaireId: string }>()
    const { session, loadingAnswer, error, initSession } = useSessionContext()

    useEffect(() => {
        initSession(params.questionnaireId)
    }, [params])

    return (
        <main className="container mx-auto p-4">
            {session &&
                <Item />
            }
            {loadingAnswer && <p>Loading...</p>}
            {error && <ErrorMessage className="mt-5" title={error} />}
        </main>
    )
}