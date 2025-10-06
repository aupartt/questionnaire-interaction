'use client';

import { useParams } from 'next/navigation';
import { useRouter } from 'next/navigation';

import { Button } from "@/components/ui/button";

import { QuestionnaireList } from '@/ui/components/QuestionnaireList';
import { useQuestionnaires } from '@/ui/hooks/useQuestionnaires';
import { QuestionnaireApiRepository } from '@/adapters/api/QuestionnaireApiRepository';
import { NextQuestionnaireDetails } from '@/ui/components/NextQuestionnaireDetails';

const questionnaireRepository = new QuestionnaireApiRepository()

export default function QuestionnairesPage() {
    const router = useRouter()
    const params = useParams<{ api_key: string }>()
    const { questionnaires, loading, error } = useQuestionnaires(params.api_key, questionnaireRepository)

    const next = questionnaires.find((q) => q.isNext)

    return (
        <main className="container mx-auto p-4">
            <QuestionnaireList
                questionnaires={questionnaires}
                loading={loading}
                error={error}
            />

            {next && (
                <div className='flex flex-wrap items-center gap-5 flex-col'>
                    <NextQuestionnaireDetails name={next.name} description={next.description} />
                    <Button
                        className='rounded-full bg-green-600 hover:bg-green-700 cursor-pointer transition-colors'
                        onClick={() => router.push(`/${params.api_key}/questionnaires/${next.id}`)}
                    >
                        Continuer
                    </Button>
                </div>
            )}

            {!next && (
                <p className="text-center text-green-600 font-semibold">Tous les questionnaires sont complétés 🎉</p>
            )}
        </main>
    )
}