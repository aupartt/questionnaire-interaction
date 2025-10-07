'use client';

import { createContext, useContext, useState, ReactNode } from 'react';

import { Session } from '@/core/entities/Session'
import { Answer } from '@/core/entities/Answer'
import { getSessionUseCase } from '@/container/Containers';

type SessionContextType = {
    session: Session | null;
    loading: boolean;
    error: string | null;
    setSession: (session: Session) => void;
    clearSession: () => void;
    addAnswer: (answer: Answer) => void;
    initSession: (apiKey: string, questionnaireId: string) => void;
}

const SessionContext = createContext<SessionContextType | undefined>(undefined)

export function SessionProvider({ children }: { children: ReactNode }) {
    const [session, setSessionState] = useState<Session | null>(null);
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    const setSession = (s: Session) => setSessionState(s)
    const clearSession = () => setSessionState(null)

    const addAnswer = (answer: Answer) => {
        if (!session) return;
        session.addAnswer(answer)
        setSession(session);
    };

    const initSession = async (apiKey: string, questionnaireId: string) => {
        setLoading(true)
        setError(null)

        const repo = getSessionUseCase()

        try {
            const data = await repo.execute(apiKey, questionnaireId)

            if (!data)
                return

            setSession(data)
            setLoading(false)
        }
        catch (err) {
            if (err instanceof Error)
                setError(err.message)
        }
        finally {
            setLoading(false)
        }
    }

    return (
        <SessionContext.Provider value={{ session, loading, error, setSession, clearSession, addAnswer, initSession }}>
            {children}
        </SessionContext.Provider>
    )
}

export function useSessionContext() {
    const context = useContext(SessionContext)
    if (!context) {
        throw new Error('useSession must be used within a SessionProvider')
    }
    return context
}