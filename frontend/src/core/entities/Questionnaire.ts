export type QuestionnaireStatus = "active" | "completed" | "skipped";

export interface Questionnaire {
    id: number;
    name: string;
    description: string;
    sessionId: number | null;
    status: QuestionnaireStatus | null;
    isNext: boolean;
}
