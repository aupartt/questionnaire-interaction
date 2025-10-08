import { useEffect, useState } from "react";
import type { Questionnaire } from "@/core/entities/Questionnaire";
import type { IQuestionnaireRepository } from "@/core/ports/IQuestionnaireRepository";

export function useQuestionnaires(
    apiKey: string,
    repository: IQuestionnaireRepository,
) {
    const [questionnaires, setQuestionnaires] = useState<Questionnaire[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        repository
            .getAll(apiKey)
            .then((data) => {
                setQuestionnaires(data);
                setLoading(false);
            })
            .catch((err) => {
                setError(err.message);
                setLoading(false);
            });
    }, [repository]);

    return { questionnaires, loading, error };
}
