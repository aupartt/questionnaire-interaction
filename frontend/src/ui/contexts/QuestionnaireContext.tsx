"use client";

import { createContext, useContext, ReactNode, useState, useEffect } from "react";
import { Questionnaire } from "@/core/entities/Questionnaire";

type ContextType = {
    questionnaires: Questionnaire[];
    loading: boolean;
    error: string | null;
    nextQuestionnaire: Questionnaire | null;
    refresh: () => void;
};

export const QuestionnaireContext = createContext<ContextType | undefined>(undefined);

type ProviderProps = {
    children: ReactNode;
    apiKey: string
}

export const QuestionnaireProvider = ({ children, apiKey }: ProviderProps) => {
    const [questionnaires, setQuestionnaires] = useState<Questionnaire[]>([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [nextQuestionnaire, setNextQuestionnaire] = useState<Questionnaire | null>(null)

    const refresh = async () => {
        try {
            setLoading(true)

            const resp = await fetch(`/api/questionnaires?apiKey=${apiKey}`)

            if (!resp.ok) {
                throw new Error("Impossible de récupérer les questionnaires.")
            }

            const data = await resp.json()

            setQuestionnaires(data)
            setError(null)
        } catch (err) {
            setError(err instanceof Error ? err.message : String(err))
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        refresh()
    }, [apiKey])

    // Met à jours le prochain questionnaire quand la liste change
    useEffect(() => {
        if (questionnaires) {
            const nextQ = questionnaires.find(q => q.isNext)
            if (nextQ) {
                setNextQuestionnaire(nextQ)
            }
            else {
                setNextQuestionnaire(null)
            }
        }
    }, [questionnaires])

    return (
        <QuestionnaireContext value={{ questionnaires, loading, error, nextQuestionnaire, refresh }}>
            {children}
        </QuestionnaireContext>
    );
};

export function useQuestionnaireContext() {
    const context = useContext(QuestionnaireContext);
    if (!context) {
        throw new Error("useQuestionnaireContext must be used within a QuestionnaireProvider");
    }
    return context;
}
