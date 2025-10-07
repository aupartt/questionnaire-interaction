import { Item } from "./Session";

export type AnswerStatus = 'completed' | 'skipped'

export interface Answer {
    itemId: string;
    value: string;
    status: AnswerStatus;
}

export type AnswerResponse = {
    next_item: Item;
    resultUrl: string | null;
    sessionStatus: string;
}