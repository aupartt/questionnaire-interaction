'use client';

import { useParams } from 'next/navigation';
import { useRouter } from 'next/navigation';

import { QuestionnaireList } from '@/ui/components/QuestionnaireList';
import { NextQuestionnaireDetails } from '@/ui/components/NextQuestionnaireDetails';
import { StyledButton } from '@/ui/components/StyledButton';
import { useSessionContext } from '@/ui/contexts/SessionContext';


export default function OnboardingPage() {
    const router = useRouter()
    const params = useParams<{ api_key: string }>()
    const { questionnaires, loadingSession, error } = useSessionContext()

    const next = questionnaires.find((q) => q.isNext)

    return (
        <main className="container mx-auto p-4">
            <QuestionnaireList
                questionnaires={questionnaires}
                loading={loadingSession}
                error={error}
            />

            {next && (
                <div className='flex flex-wrap items-center gap-5 flex-col'>
                    <NextQuestionnaireDetails name={next.name} description={next.description} />
                    <StyledButton value="Continuer" action={() => router.push(`/${params.api_key}/questionnaire/${next.id}`)} />
                </div>
            )}

            {!next && !loadingSession && !error && (
                <p className="text-center text-green-600 font-semibold">Tous les questionnaires sont complétés 🎉</p>
            )}
        </main>
    )
}