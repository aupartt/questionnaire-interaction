import { Item } from "./Session";

export type AnswerStatus = 'completed' | 'skipped'

export interface Answer {
    itemId: string;
    value: string;
    status: AnswerStatus;
}

export type AnswerResponse = {
    next_item: Item;
    result_url: string | null;
    session_status: string;
}