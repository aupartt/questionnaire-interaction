import { ReactNode, useState } from 'react';

import { type Item } from '@/core/entities/Session'

import { ItemQuestion } from './ItemQuestion';
import { ItemContent } from './ItemContent';
import { Button } from '@/components/ui/button';
import { useSessionContext } from '@/ui/contexts/SessionContext';

type ItemProps = {
    currentItem: Item
}

export function Item({ currentItem }: ItemProps) {
    const [answerValue, setAnswerValue] = useState<string | null>(null)
    const { addAnswer } = useSessionContext()

    const handleChange = (newValue: string) => {
        setAnswerValue(newValue)
    }

    const handleSubmit = () => {
        if (!answerValue)
            return

        addAnswer({
            itemId: currentItem.id,
            value: answerValue,
            status: "completed"
        })
    }

    return <div className='content'>
        <ItemQuestion question={currentItem.question} />
        <ItemContent name={currentItem.name} content={currentItem.content} handleChange={handleChange} />
        <Button onClick={handleSubmit}>Continuer</Button>
    </div>
} 