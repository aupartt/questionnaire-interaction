"use client";

import {
    createContext,
    type ReactNode,
    useCallback,
    useContext,
    useEffect,
    useState,
} from "react";
import type { Answer, AnswerResponse } from "@/core/entities/Answer";
import { Session } from "@/core/entities/Session";

type ContextType = {
    session: Session | null;
    loading: boolean;
    error: string | null;
    addAnswer: (answer: Answer) => void;
    clearSession: () => void;
};

export const SessionContext = createContext<ContextType | undefined>(undefined);

type ProviderProps = {
    children: ReactNode;
    apiKey: string;
    questionnaireId: number;
};

export const SessionProvider = ({
    children,
    apiKey,
    questionnaireId,
}: ProviderProps) => {
    const [session, setSession] = useState<Session | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const initSession = useCallback(async () => {
        try {
            setLoading(true);
            setError(null);

            const resp = await fetch(
                `/api/session?apiKey=${apiKey}&questionnaireId=${questionnaireId}`,
            );

            if (!resp.ok) {
                throw new Error("Impossible de récupérer la session.");
            }

            const data = await resp.json();

            if (!data) throw new Error("Session introuvable");

            const newSession = new Session(
                data.id,
                data.questionnaireId,
                data.items,
                data.answers,
                data.currentItem,
                "active",
            );
            setSession(newSession);
        } catch (err) {
            const message = err instanceof Error ? err.message : String(err);
            setError(message);
            throw err;
        } finally {
            setLoading(false);
        }
    }, [apiKey, questionnaireId]);

    useEffect(() => {
        console.info(
            "Initialisation de la session pour le questionnaire:",
            questionnaireId,
        );
        initSession();
    }, [questionnaireId, initSession]);

    const addAnswer = async (answer: Answer) => {
        if (!session) throw new Error("Aucune session active");
        setLoading(true);
        setError(null);

        try {
            const res = await fetch(
                `/api/session/answer?apiKey=${apiKey}&questionnaireId=${questionnaireId}&sessionId=${session.id}`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ answer }),
                },
            );

            if (!res.ok) {
                throw new Error("Impossible de récupérer la session.");
            }

            const data: AnswerResponse = await res.json();

            if (!data) throw new Error("Session introuvable");

            // Ajoute la réponse à la session et change l'item s'il existe
            const updatedSession = session.addAnswer(answer);
            if (data.nextItem) updatedSession.currentItem = data.nextItem;
            updatedSession.status = data.sessionStatus;

            setSession(updatedSession);
        } catch (err) {
            setError(err instanceof Error ? err.message : String(err));
        } finally {
            setLoading(false);
        }
    };

    const clearSession = useCallback(() => {
        setSession(null);
        setError(null);
    }, []);

    return (
        <SessionContext
            value={{ session, loading, error, addAnswer, clearSession }}
        >
            {children}
        </SessionContext>
    );
};

export function useSessionContext() {
    const context = useContext(SessionContext);
    if (!context) {
        throw new Error(
            "useSessionContext must be used within a SessionContext",
        );
    }
    return context;
}
