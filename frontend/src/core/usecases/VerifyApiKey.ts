import type { IAuthRepository } from "../ports/IAuthRepository";

export class VerifyApiKey {
    constructor(private readonly authRepository: IAuthRepository) {}

    async execute(apiKey: string): Promise<boolean> {
        const apiKeyStatus = await this.authRepository.verify(apiKey);
        return apiKeyStatus.isValid;
    }
}
