import { type Question } from '@/core/entities/Session'
import { TextQuestion } from './questions';
import { ReactNode } from 'react';

interface ItemQuestionProps {
    question: Question
}

export function ItemQuestion({ question }: ItemQuestionProps) {
    let node: ReactNode = <></>
    switch (question.type) {
        case "text":
            node = <TextQuestion value={question.value} />
    }

    return (
        <div className='flex pb-4'>
            {node}
        </div>
    )
}