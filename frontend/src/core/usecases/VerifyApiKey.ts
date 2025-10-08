import { ApiKeyStatus } from "../entities/ApiKeyStatus";
import { IAuthRepository } from "../ports/IAuthRepository";

export class VerifyApiKey {
    constructor(private readonly authRepository: IAuthRepository) {}

    async execute(apiKey: string): Promise<ApiKeyStatus | null> {
        const apiKeyStatus = await this.authRepository.verify(apiKey);
        return apiKeyStatus;
    }
}
