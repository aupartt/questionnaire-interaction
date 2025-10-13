import type { Item } from "./Session";
import { SessionStatus } from "@/core/entities/Session";

export type AnswerStatus = "completed" | "skipped";

export interface Answer {
    itemId: number;
    value?: string | null;
    status: AnswerStatus;
}

export type AnswerResponse = {
    nextItem?: Item;
    resultUrl?: string;
    sessionStatus: SessionStatus;
};
