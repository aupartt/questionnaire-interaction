interface TextQuestionProps {
    value: string
}

export function TextQuestion({ value }: TextQuestionProps) {
    return <p>{value}</p>
}