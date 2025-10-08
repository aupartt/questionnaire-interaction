'use client';

import { useParams } from 'next/navigation';

import { Item } from '@/ui/components/item'
import { useEffect } from 'react';
import { useSessionContext } from '@/ui/contexts/SessionContext'

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
            {loading && <p>Loading...</p>}
            {error && <p>{error}</p>}
        </main>
    )
}