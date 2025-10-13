"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { QuestImages } from "@/ui/components/questionnaire/QuestImages";
import { QuestSteps } from "@/ui/components/questionnaire/QuestSteps";
import { useQuestionnaireContext } from "@/ui/contexts/QuestionnaireContext";
import { useTheme } from "@/ui/contexts/ThemeContext";

export default function QuestionnairesPage() {
    const { loading, error, nextQuestionnaire } = useQuestionnaireContext();
    const { className } = useTheme();

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div className="grid place-items-center h-screen">
            <div className="flex flex-wrap gap-10 w-1/3 max-w-lg min-w-sm flex-col items-center">
                <QuestSteps />
                <QuestImages />
                {
                    nextQuestionnaire && <>
                        <div>
                            <h2
                                className={`text-2xl text-center font-black ${className.textPrimary}`}
                            >
                                {nextQuestionnaire.name}
                            </h2>
                        </div>
                        <div>
                            <p className="text-center text-gray-500">
                                {nextQuestionnaire.description}
                            </p>
                        </div>
                        <Link href={`questionnaires/${nextQuestionnaire.id}/items`}>
                            <Button
                                className={`rounded-full ${className.bgPrimary} hover:bg-green-700 transition-colors`}
                            >
                                C'est parti !
                            </Button>
                        </Link>
                    </>
                }
                <div className="w-full flex flex-col items-center">
                    <p className="pb-3 text-gray-500 text-sm">
                        Je m'arrête là pour aujourd'hui
                    </p>
                    <Link
                        className="font-bold text-gray-500 underline"
                        href="#"
                    >
                        Voir mes résultats
                    </Link>
                </div>
            </div>
        </div>
    );
}
