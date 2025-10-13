"use client";

import { useQuestionnaireContext } from "@/ui/contexts/QuestionnaireContext";
import Image from "next/image";

export function QuestImages() {
    const { questionnaires } = useQuestionnaireContext();

    const mockImg =
        "https://a.pinatafarm.com/500x375/1d1a525df0/charlie-day-13b7e9bf65e171e96d26b497469962c8-meme.jpeg";

    return (
        <div className="flex w-full justify-between">
            {questionnaires.map((el, id) => (
                <ImgChild
                    key={id}
                    url={mockImg}
                    alt={`Image Questionnaire ${id + 1}`}
                />
            ))}
        </div>
    );
}

function ImgChild({ url, alt }: { url: string; alt: string }) {
    return (
        <Image
            className="border-1"
            src={url}
            alt={alt}
            width={150}
            height={150}
            priority
        />
    );
}
