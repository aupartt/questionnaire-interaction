"use client";

import { useSessionContext } from "@/ui/contexts/SessionContext";
import { ItemStepper } from "@/ui/components/item/ItemStepper";
import { Item } from "@/ui/components/item";
import { Answer } from "@/core/entities/Answer";
import { useRouter } from "next/navigation";
import { use } from "react";

export default function ApiKeyPage({
    params
}: {
    params: Promise<{ apiKey: string }>
}) {
    const { apiKey } = use(params)
    const router = useRouter()
    const { session, addAnswer } = useSessionContext()

    if (!session) return "No session" // For lint

    const submitAnswer = (answer: Answer) => {
        if (session.status === "active") {
            if (!answer) return;
            addAnswer(answer);
        } else {
            router.push(`/${apiKey}/onboarding`);
        }
    }

    return (
        <div className="flex-1 p-4 overflow-auto">
            <div className="h-10"></div>
            <div className="flex flex-col item-center gap-7 mx-auto min-w-2xl w-1/2">
                <ItemStepper />
                <h2 className="font-bold">{session?.currentItem.name}</h2>
                <Item submit={submitAnswer} />
            </div>
        </div>
    )
}
