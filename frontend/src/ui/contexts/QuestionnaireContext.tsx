"use client";

import { createContext, useContext, ReactNode, useState, useEffect, useCallback } from "react";
import { Questionnaire } from "@/core/entities/Questionnaire";

type ContextType = {
    questionnaires: Questionnaire[];
    nextQuestionnaire: Questionnaire | null;
};

export const QuestionnaireContext = createContext<ContextType | undefined>(undefined);

type ProviderProps = {
    children: ReactNode;
    questionnaires: Questionnaire[];
}

export const QuestionnaireProvider = ({ children, questionnaires }: ProviderProps) => {
    const [nextQuestionnaire, setNextQuestionnaire] = useState<Questionnaire | null>(null)

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
        <QuestionnaireContext value={{ questionnaires, nextQuestionnaire }}>
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
