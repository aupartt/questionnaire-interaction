interface TextQuestionProps {
    className?: string
    value: string
}

export function TextQuestion({ value, className }: TextQuestionProps) {
    return <p className={className} >{value}</p>
}