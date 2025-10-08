export type QuestionnaireStatus = "active" | "completed" | "skipped";

export interface Questionnaire {
    id: string;
    name: string;
    description: string;
    sessionId: string | null;
    status: QuestionnaireStatus | null;
    isNext: boolean;
}
