"use client";

import type { Answer } from "@/core/entities/Answer";
import { ItemSection } from "@/ui/components/item/Item";
import { ItemStepper } from "@/ui/components/item/ItemStepper";
import { useSessionContext } from "@/ui/contexts/SessionContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function ApiKeyPage() {
    const { session, addAnswer } = useSessionContext();
    const router = useRouter();

    if (!session) return "No session"; // For lint

    useEffect(() => {
        if (session.status === "completed") {
            router.push(`results`);
        }
    }, [session]);

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
                <ItemSection
                    currentItem={session.currentItem}
                    submit={submitAnswer}
                />
            </div>
        </div>
    );
}
