import { ReactNode } from 'react';
import { QuestionnaireProvider } from '@/ui/contexts/QuestionnaireContext'
import { getAllQuestionnaireUseCase } from '@/container/Containers';

const GetAllQuestionnaire = getAllQuestionnaireUseCase()

export default async function QuestionnairesLayout({ children, params }: {
    children: ReactNode,
    params: Promise<{ apiKey: string }>
}) {
    const { apiKey } = await params
    const questionnaires = await GetAllQuestionnaire.execute(apiKey)

    return <div>
        <QuestionnaireProvider questionnaires={questionnaires}>
            {
                children
            }
        </QuestionnaireProvider>
    </div>
} 
