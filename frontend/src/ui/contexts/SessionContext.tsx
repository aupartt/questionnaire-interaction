"use client";

import {
    createContext,
    useContext,
    useState,
    ReactNode,
    useEffect,
} from "react";
import { useRouter } from "next/navigation";

import { Session } from "@/core/entities/Session";
import { Answer } from "@/core/entities/Answer";
import {
    getAllQuestionnaireUseCase,
    getSessionUseCase,
    getSubmitAnswerUseCase,
} from "@/container/Containers";
import { Questionnaire } from "@/core/entities/Questionnaire";
import { ApiNotReachableError } from "@/adapters/api/errors";

type SessionContextType = {
    apiKey: string | null;
    questionnaires: Questionnaire[];
    session: Session | null;
    loadingSession: boolean;
    loadingAnswer: boolean;
    error: string | null;
    clearSession: () => void;
    addAnswer: (answer: Answer) => void;
    initSession: (questionnaireId: string) => void;
};

const SessionContext = createContext<SessionContextType | undefined>(undefined);

export function SessionProvider({
    children,
    apiKey,
}: {
    children: ReactNode;
    apiKey: string;
}) {
    const [questionnaires, setQuestionnaires] = useState<Questionnaire[]>([]);
    const [session, setSessionState] = useState<Session | null>(null);
    const [loadingSession, setLoadingSession] = useState(false);
    const [loadingAnswer, setLoadingAnswer] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const submitAnswer = getSubmitAnswerUseCase();
    const getSession = getSessionUseCase();
    const getAllQuestionnaire = getAllQuestionnaireUseCase();
    const router = useRouter();

    const setSession = (s: Session) => setSessionState(s);
    const clearSession = () => setSessionState(null);

    const addAnswer = async (answer: Answer) => {
        if (!session) return;
        setLoadingAnswer(true);
        setError(null);

        try {
            const res = await submitAnswer.execute(
                apiKey,
                session.id,
                session.questionnaireId,
                answer,
            );
            session.addAnswer(answer);
            if (res.sessionStatus == "active" && res.nextItem) {
                session.currentItem = res.nextItem;
                setSession(session);
            } else {
                // Redirige vers onboarding (temporaire)
                router.push(`/${apiKey}/onboarding`);
            }
        } catch (err) {
            if (err instanceof ApiNotReachableError) {
                setError(err.message);
            }
        } finally {
            setLoadingAnswer(false);
        }
    };

    useEffect(() => {
        getAllQuestionnaire
            .execute(apiKey)
            .then((questionnaires) => {
                setQuestionnaires(questionnaires);
            })
            .catch((err) => setError(err));
    }, [apiKey]);

    const initSession = async (questionnaireId: string) => {
        setLoadingSession(true);
        setError(null);

        try {
            const data = await getSession.execute(apiKey, questionnaireId);

            if (!data) return;

            setSession(data);
            setLoadingSession(false);
        } catch (err) {
            if (err instanceof Error) setError(err.message);
        } finally {
            setLoadingSession(false);
        }
    };

    return (
        <SessionContext.Provider
            value={{
                apiKey,
                questionnaires,
                session,
                loadingSession,
                loadingAnswer,
                error,
                clearSession,
                addAnswer,
                initSession,
            }}
        >
            {children}
        </SessionContext.Provider>
    );
}

export function useSessionContext() {
    const context = useContext(SessionContext);
    if (!context) {
        throw new Error("useSession must be used within a SessionProvider");
    }
    return context;
}
