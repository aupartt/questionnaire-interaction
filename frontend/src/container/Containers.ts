import { AuthApiRepository } from '@/adapters/api/AuthApiRepository';
import { VerifyApiKey } from '@/core/usecases/VerifyApiKey';
import { GetAllQuestionnaire } from '@/core/usecases/GetAllQuestionnaire';
import { QuestionnaireApiRepository } from '@/adapters/api/QuestionnaireApiRepository';
import { GetSession } from '@/core/usecases/GetSession'
import { SessionApiRepository } from '@/adapters/api/SessionApiRepository';
import { SubmitAnswer } from '@/core/usecases/SubmitAnswer';
import { AnswerApiRepository } from '@/adapters/api/AnswerApiRepository';


export function getVerifyApiKeyUseCase(): VerifyApiKey {
    return new VerifyApiKey(new AuthApiRepository())
}

export function getAllQuestionnaireUseCase(): GetAllQuestionnaire {
    return new GetAllQuestionnaire(new QuestionnaireApiRepository())
}

export function getSessionUseCase(): GetSession {
    return new GetSession(new SessionApiRepository())
}

export function getSubmitAnswerUseCase(): SubmitAnswer {
    return new SubmitAnswer(new AnswerApiRepository())
}