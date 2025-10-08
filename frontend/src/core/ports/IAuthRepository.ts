import type { ApiKeyStatus } from "../entities/ApiKeyStatus";

export interface IAuthRepository {
    verify(apiKey: string): Promise<ApiKeyStatus>;
}
