import type { ApiKeyStatus } from "@/core/entities/ApiKeyStatus";
import type { IAuthRepository } from "@/core/ports/IAuthRepository";

export class MockAuthRepository implements IAuthRepository {
    private sessionStatus = { isValid: true };

    async verify(): Promise<ApiKeyStatus> {
        return Promise.resolve(this.sessionStatus);
    }
}
