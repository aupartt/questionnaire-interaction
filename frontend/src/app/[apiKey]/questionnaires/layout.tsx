import { ReactNode } from "react";
import { QuestionnaireProvider } from "@/ui/contexts/QuestionnaireContext";

export default async function QuestionnairesLayout({
    children,
    params,
}: {
    children: ReactNode;
    params: Promise<{ apiKey: string }>;
}) {
    const { apiKey } = await params;

    return (
        <div>
            <QuestionnaireProvider apiKey={apiKey}>
                {children}
            </QuestionnaireProvider>
        </div>
    );
}
