import type { ReactNode } from "react";
import type { Question } from "@/core/entities/Session";
import { TextQuestion } from "./questions";

interface ItemQuestionProps {
    question: Question;
}

export function ItemQuestion({ question }: ItemQuestionProps) {
    let node: ReactNode = <></>;
    switch (question.type) {
        case "text":
            node = (
                <TextQuestion className="font-bold" value={question.value} />
            );
    }

    return node;
}
