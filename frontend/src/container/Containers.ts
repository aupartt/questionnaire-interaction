import { AuthApiRepository } from '@/adapters/api/AuthApiRepository';
import { VerifyApiKey } from '@/core/usecases/VerifyApiKey';


export function getVerifyApiKeyUseCase(): VerifyApiKey {
    return new VerifyApiKey(new AuthApiRepository())
}