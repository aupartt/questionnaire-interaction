import { useEffect, useState } from 'react';
import { Session } from '@/core/entities/Session';
import { IQuestionnaireRepository } from '@/core/ports/IQuestionnaireRepository';

export function useSession(apiKey: string, questionnaireId: string, repository: IQuestionnaireRepository) {
    const [session, setSession] = useState<Session | null>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        repository.getSession(apiKey, questionnaireId)
            .then(data => {
                setSession(data)
                setLoading(false)
            })
            .catch(err => {
                setError(err.message)
                setLoading(false)
            })
    }, [repository, apiKey])

    return { session, loading, error }
}