import Image from "next/image";
import type { Results } from "@/core/entities/Results";

export function QuestionnaireResults({ results }: { results: Results }) {
    return (
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
    );
}
