import { useState } from 'react';

import { type Item } from '@/core/entities/Session'

import { ItemQuestion } from './ItemQuestion';
import { ItemContent } from './ItemContent';
import { useSessionContext } from '@/ui/contexts/SessionContext';
import { StyledButton } from '../StyledButton';
import { ProgressStepper } from './ProgressStepper';

export function Item() {
    const [answerValue, setAnswerValue] = useState<string | null>(null)
    const { session, error, loadingAnswer, addAnswer } = useSessionContext()

    const handleChange = (newValue: string) => {
        setAnswerValue(newValue)
    }

    const handleSubmit = () => {
        if (!answerValue)
            return

        addAnswer({
            itemId: session!.currentItem.id,
            value: answerValue,
            status: "completed"
        })
    }

    return <div className='flex flex-col gap-5'>
        <ProgressStepper />
        <ItemQuestion question={session!.currentItem.question} />
        <ItemContent name={session!.currentItem.name} content={session!.currentItem.content} handleChange={handleChange} />
        <div className='flex flex-row-reverse'>
            <StyledButton value="Continuer" action={handleSubmit} />
        </div>
    </div>
} 