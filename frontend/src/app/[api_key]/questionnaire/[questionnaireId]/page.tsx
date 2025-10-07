'use client';

import { useParams } from 'next/navigation';

import { Item } from '@/ui/components/item'
import { useEffect } from 'react';
import { useSessionContext } from '@/ui/contexts/SessionContext'

export default function QuestionnairePage() {
    const params = useParams<{ api_key: string, questionnaireId: string }>()
    const { session, loading, error, initSession } = useSessionContext()

    useEffect(() => {
        initSession(params.api_key, params.questionnaireId)
    }, [])

    return (
        <main className="container mx-auto p-4">
            {session &&
                <Item currentItem={session.currentItem} />
            }
            {loading && <p>Loading...</p>}
            {error && <p>{error}</p>}
        </main>
    )
}