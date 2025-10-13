import { useEffect, useState } from "react";
import { useSessionContext } from "@/ui/contexts/SessionContext";
import { StyledButton } from "../StyledButton";
import { ItemContent } from "./ItemContent";
import { ItemQuestion } from "./ItemQuestion";
import { Answer } from "@/core/entities/Answer";
import { type Item } from '@/core/entities/Session'

export function Item({ currentItem, submit }: { currentItem: Item, submit: (answer: Answer) => void }) {
    const [answerValue, setAnswerValue] = useState<string>("");

    useEffect(() => {
        setAnswerValue("")
    }, [currentItem])

    const handleChange = (newValue: string) => {
        setAnswerValue(newValue);
    };

    // Crée l'objet Answer et le submit
    const onSubmit = () => {
        submit({
            itemId: currentItem.id,
            value: answerValue,
            status: "completed"
        })
    }

    return (
        <div className="flex flex-col gap-5">
            <ItemQuestion question={currentItem.question} />
            <ItemContent
                content={currentItem.content}
                handleChange={handleChange}
                value={answerValue}
            />
            <div className="flex flex-row-reverse">
                <StyledButton value="Continuer" action={onSubmit} />
            </div>
        </div>
    );
}



{/* <ul className="">
    <li className="p-3 text-center border-2 rounded-t-sm font-bold border-gray-400 text-gray-400">En période de transition</li>
    <li className="p-3 text-center border-x-2 font-bold border-gray-400 text-gray-400">En formation</li>
    <li className="p-3 text-center border-2 font-bold border-gray-400 text-gray-400">En poste</li>
    <li className="p-3 text-center border-x-2 font-bold border-gray-400 text-green-600 bg-green-100">En recherche d'emploi</li>
    <li className="p-3 text-center border-2 rounded-b-sm font-bold border-gray-400 text-gray-400">En reconversion</li>
</ul>
<div className="flex flex-row-reverse">
    <Button
        onClick={nextItem}
        className="rounded-full bg-green-600 hover:bg-green-700 transition-colors"
    >Suivant</Button>
</div> */}
