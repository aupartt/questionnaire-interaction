import { useState } from "react";

import { useSessionContext } from "@/ui/contexts/SessionContext";
import { StyledButton } from "../StyledButton";
import { ItemContent } from "./ItemContent";
import { ItemQuestion } from "./ItemQuestion";
import { ProgressStepper } from "./ProgressStepper";

export function Item() {
    const [answerValue, setAnswerValue] = useState<string | null>(null);
    const { session, addAnswer } = useSessionContext();

    const handleChange = (newValue: string) => {
        setAnswerValue(newValue);
    };

    const handleSubmit = () => {
        if (!answerValue) return;

        addAnswer({
            itemId: session!.currentItem.id,
            value: answerValue,
            status: "completed",
        });
    };

    return (
        <div className="flex flex-col gap-5">
            <ProgressStepper />
            <ItemQuestion question={session!.currentItem.question} />
            <ItemContent
                content={session!.currentItem.content}
                handleChange={handleChange}
            />
            <div className="flex flex-row-reverse">
                <StyledButton value="Continuer" action={handleSubmit} />
            </div>
        </div>
    );
}
