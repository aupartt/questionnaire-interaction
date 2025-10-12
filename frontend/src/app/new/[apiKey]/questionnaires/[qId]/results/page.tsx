import { type Results } from '@/core/entities/Results';
import { QuestionnaireResults } from '@/ui/components/questionnaire/QuestionnaireResults';

export default function ResultsPage() {
    const results = {
        imgUrl: ""
    } as Results
    return (
        <QuestionnaireResults results={results} />
    )
}
