interface NextQuestionnaireDetailsProps {
    name: string;
    description: string;
}

export function NextQuestionnaireDetails({
    name,
    description,
}: NextQuestionnaireDetailsProps) {
    return (
        <>
            <h2 className="font-bold text-green-600 text-lg">{name}</h2>
            <p className=" text-gray-500 text-sm">{description}</p>
        </>
    );
}
