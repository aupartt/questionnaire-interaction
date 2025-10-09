import { AnswerApiRepository } from "@/adapters/api/AnswerApiRepository";
import { AuthApiRepository } from "@/adapters/api/AuthApiRepository";
import { QuestionnaireApiRepository } from "@/adapters/api/QuestionnaireApiRepository";
import { ResultsApiRepository } from "@/adapters/api/ResultsApiRepository";
import { SessionApiRepository } from "@/adapters/api/SessionApiRepository";
import { AnswerPubRepository } from "@/adapters/public/AnswerPubRepository";
import { QuestionnairePubRepository } from "@/adapters/public/QuestionnairePubRepository";
import { ResultsPubRepository } from "@/adapters/public/ResultsPubRepository";
import { SessionPubRepository } from "@/adapters/public/SessionPubRepository";
import { GetAllQuestionnaire } from "@/core/usecases/GetAllQuestionnaire";
import { GetResults } from "@/core/usecases/GetResults";
import { GetSession } from "@/core/usecases/GetSession";
import { SubmitAnswer } from "@/core/usecases/SubmitAnswer";
import { VerifyApiKey } from "@/core/usecases/VerifyApiKey";

export function getVerifyApiKeyApiUseCase(): VerifyApiKey {
    return new VerifyApiKey(new AuthApiRepository());
}

export function getAllQuestionnaireApiUseCase(): GetAllQuestionnaire {
    return new GetAllQuestionnaire(new QuestionnaireApiRepository());
}

export function getSessionApiUseCase(): GetSession {
    return new GetSession(new SessionApiRepository());
}

export function getSubmitAnswerApiUseCase(): SubmitAnswer {
    return new SubmitAnswer(new AnswerApiRepository());
}

export function getResultsApiUseCase(): GetResults {
    return new GetResults(new ResultsApiRepository());
}

export function getAllQuestionnairePubUseCase(): GetAllQuestionnaire {
    return new GetAllQuestionnaire(new QuestionnairePubRepository());
}

export function getSessionPubUseCase(): GetSession {
    return new GetSession(new SessionPubRepository());
}

export function getSubmitAnswerPubUseCase(): SubmitAnswer {
    return new SubmitAnswer(new AnswerPubRepository());
}

export function getResultsPubUseCase(): GetResults {
    return new GetResults(new ResultsPubRepository());
}
