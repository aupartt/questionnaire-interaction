"use client";

import { useSessionContext } from "@/ui/contexts/SessionContext";
import { ItemStepper } from "@/ui/components/item/ItemStepper";
import { Item } from "@/ui/components/item";
import { Answer } from "@/core/entities/Answer";

export default function ApiKeyPage() {
    const { session, addAnswer } = useSessionContext();

    if (!session) return "No session"; // For lint

    const submitAnswer = (answer: Answer) => {
        if (!answer) return;
        addAnswer(answer);
    };

    return (
        <div className="flex-1 p-4 overflow-auto">
            <div className="h-10"></div>
            <div className="flex flex-col item-center gap-7 mx-auto min-w-2xl w-1/2">
                <ItemStepper />
                <h2 className="font-bold">{session?.currentItem.name}</h2>
                <Item currentItem={session.currentItem} submit={submitAnswer} />
            </div>
        </div>
    );
}
