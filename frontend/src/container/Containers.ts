import { AnswerApiRepository } from "@/adapters/api/AnswerApiRepository";
import { AuthApiRepository } from "@/adapters/api/AuthApiRepository";
import { QuestionnaireApiRepository } from "@/adapters/api/QuestionnaireApiRepository";
import { ResultsApiRepository } from "@/adapters/api/ResultsApiRepository";
import { SessionApiRepository } from "@/adapters/api/SessionApiRepository";
import { GetAllQuestionnaire } from "@/core/usecases/GetAllQuestionnaire";
import { GetResults } from "@/core/usecases/GetResults";
import { GetSession } from "@/core/usecases/GetSession";
import { SubmitAnswer } from "@/core/usecases/SubmitAnswer";
import { VerifyApiKey } from "@/core/usecases/VerifyApiKey";

export function getVerifyKeyUseCase(): VerifyApiKey {
    return new VerifyApiKey(new AuthApiRepository());
}

export function getAllQuestionnaireUseCase(): GetAllQuestionnaire {
    return new GetAllQuestionnaire(new QuestionnaireApiRepository());
}

export function getSessionUseCase(): GetSession {
    return new GetSession(new SessionApiRepository());
}

export function getSubmitAnswerUseCase(): SubmitAnswer {
    return new SubmitAnswer(new AnswerApiRepository());
}

export function getResultsUseCase(): GetResults {
    return new GetResults(new ResultsApiRepository());
}
