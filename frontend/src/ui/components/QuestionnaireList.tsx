import { Questionnaire } from "@/core/entities/Questionnaire";

interface QuestionnaireListProps {
    questionnaires: Questionnaire[];
    loading: boolean;
    error: string | null;
}

export function QuestionnaireList({
    questionnaires,
    loading,
    error,
}: QuestionnaireListProps) {
    if (loading) {
        return <div className="text-center p-4">Chargement...</div>;
    }

    if (error) {
        return <div className="text-red-500 p-4">Erreur : {error}</div>;
    }

    if (questionnaires.length === 0) {
        return <div className="p-4">Aucun questionnaire disponible</div>;
    }

    return (
        <div className="flex flex-wrap justify-center items-center gap-5 md:flex-row pb-5">
            {questionnaires.map((q) => (
                <h2
                    key={q.id}
                    className={`text-sm font-${q.isNext ? "bold" : "semibold"}`}
                >
                    {q.name}
                </h2>
            ))}
        </div>
    );
}
