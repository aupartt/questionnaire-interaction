import { Item } from "./Session";

export type AnswerStatus = 'completed' | 'skipped'

export interface Answer {
    itemId: string;
    value: string;
    status: AnswerStatus;
}

export type AnswerResponse = {
    nextItem?: Item;
    resultUrl?: string;
    sessionStatus: string;
}