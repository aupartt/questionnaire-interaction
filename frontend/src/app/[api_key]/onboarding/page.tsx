"use client";

import { useRouter } from "next/navigation";
import { ErrorMessage } from "@/ui/components/ErrorMessage";
import { NextQuestionnaireDetails } from "@/ui/components/NextQuestionnaireDetails";
import { QuestionnaireList } from "@/ui/components/QuestionnaireList";
import { StyledButton } from "@/ui/components/StyledButton";
import { useSessionContext } from "@/ui/contexts/SessionContext";

export default function OnboardingPage() {
    const router = useRouter();
    const { apiKey, questionnaires, loadingSession, error } = useSessionContext();

    if (questionnaires.length == 0) {
        return <p>Liste de questionnaire vide.</p>
    }

    const next = questionnaires.find((q) => q.isNext);

    return (
        <main className="container mx-auto p-4">
            <h2 className="font-bold text-center">Onboarding</h2>
            <QuestionnaireList
                questionnaires={questionnaires}
                loading={loadingSession}
                error={error}
            />

            {next && (
                <div className="flex flex-wrap items-center gap-5 flex-col">
                    <NextQuestionnaireDetails
                        name={next.name}
                        description={next.description}
                    />
                    <StyledButton
                        value="Continuer"
                        action={() =>
                            router.push(
                                `/${apiKey}/questionnaire/${next.id}`,
                            )
                        }
                    />
                </div>
            )}

            {
                loadingSession && <p>Loading...</p>
            }

            {!next && !loadingSession && !error && (
                <p className="text-center text-green-600 font-semibold">
                    Tous les questionnaires sont complétés 🎉
                </p>
            )}

            {error && <ErrorMessage className="mt-5" title={error} />}
        </main>
    );
}
