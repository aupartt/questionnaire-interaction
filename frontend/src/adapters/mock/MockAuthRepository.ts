import { IAuthRepository } from '@/core/ports/IAuthRepository';
import { ApiKeyStatus } from '@/core/entities/ApiKeyStatus';

export class MockAuthRepository implements IAuthRepository {
    private sessionStatus = { isValid: true }

    async verify(): Promise<ApiKeyStatus> {
        return Promise.resolve(this.sessionStatus)
    }
}