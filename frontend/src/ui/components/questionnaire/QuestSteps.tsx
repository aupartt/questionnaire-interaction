"use client";

import { useQuestionnaireContext } from "@/ui/contexts/QuestionnaireContext";
import { SpacerWrapper } from "../SpacerWrapper";

export function QuestSteps() {
    const { questionnaires } = useQuestionnaireContext();

    return (
        <div className="flex px-[50px] items-center w-full justify-center gap-5">
            <SpacerWrapper spacer={Spacer()}>
                {questionnaires.map((item, id) => (
                    <Step key={item.id} isActive={item.isNext}>
                        Etape {id + 1}
                    </Step>
                ))}
            </SpacerWrapper>
        </div>
    );
}

function Spacer() {
    return (
        <div className="flex-grow border-t-2 border-dashed border-green-700 relative"></div>
    );
}

function Step({
    isActive,
    children,
}: {
    isActive: boolean;
    children: React.ReactNode;
}) {
    return (
        <span
            className={`text-nowrap font-bold ${isActive ? "text-gray-900" : "text-gray-400"}`}
        >
            {children}
        </span>
    );
}
