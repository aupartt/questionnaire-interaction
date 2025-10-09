import type { Answer, AnswerStatus } from "./Answer";

export type ItemShort = {
    id: number;
    name: string;
};
export type Question = {
    type: string;
    value: string;
};

export type Content = {
    type: string;
    likertValue?: string[];
};

export type Item = {
    id: number;
    name: string;
    question: Question;
    content: Content;
};

export class Session {
    constructor(
        public readonly id: number,
        public readonly questionnaireId: number,
        public items: ItemShort[],
        public answers: Answer[],
        public currentItem: Item,
    ) {}

    addAnswer(answer: Answer): void {
        // Regarde si la réponse existe
        const exist_idx = this.answers.findIndex(
            (x) => x.itemId === answer.itemId,
        );

        // Update la réponse
        if (exist_idx > -1) {
            this.answers[exist_idx] = answer;
        }

        // Ajoute une nouvelle réponse
        else {
            this.answers.push(answer);
        }
    }

    getItemStatus(itemId: number): AnswerStatus | null {
        const item = this.answers.find((x) => x.itemId === itemId);

        if (item) {
            return item.status;
        }
        return null;
    }
}
