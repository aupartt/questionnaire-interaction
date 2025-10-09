import Image from "next/image";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { useSessionContext } from "@/ui/contexts/SessionContext";
import { StyledButton } from "../StyledButton";
import { ItemContent } from "./ItemContent";
import { ItemQuestion } from "./ItemQuestion";
import { ProgressStepper } from "./ProgressStepper";

export function Item() {
    const [answerValue, setAnswerValue] = useState<string | null>(null);
    const { session, status, results, apiKey, addAnswer } = useSessionContext();
    const router = useRouter();

    const handleChange = (newValue: string) => {
        setAnswerValue(newValue);
    };

    const handleSubmit = () => {
        if (status === "active") {
            if (!answerValue) return;

            addAnswer({
                itemId: session!.currentItem.id,
                value: answerValue,
                status: "completed",
            });
        } else {
            router.push(`/${apiKey}/onboarding`);
        }
    };

    return (
        <div className="flex flex-col gap-5">
            <ProgressStepper />
            {status === "active" && (
                <>
                    <ItemQuestion question={session!.currentItem.question} />
                    <ItemContent
                        content={session!.currentItem.content}
                        handleChange={handleChange}
                    />
                </>
            )}
            {status === "completed" && results && (
                <>
                    <div className="flex flex-col justify-center items-center">
                        <p className="font-bold pb-5">Questionnaire fini !</p>
                        <Image
                            src={results.imgUrl}
                            alt="result img"
                            width={180}
                            height={180}
                            priority
                        />
                        <p className="pt-5">
                            Cliquez sur continuer pour retourner à la liste des
                            questionnaires
                        </p>
                    </div>
                </>
            )}
            <div className="flex flex-row-reverse">
                <StyledButton value="Continuer" action={handleSubmit} />
            </div>
        </div>
    );
}
