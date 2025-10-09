import type { ApiKeyStatus } from "@/core/entities/ApiKeyStatus";
import type { IAuthRepository } from "@/core/ports/IAuthRepository";
import { ApiNotReachableError } from "./errors";

export class AuthApiRepository implements IAuthRepository {
    private apiUrl = `${process.env.NEXT_PUBLIC_API_URL}`;
    private apiKeyName = `${process.env.NEXT_PUBLIC_API_KEY_NAME}`

    async verify(apiKey: string): Promise<ApiKeyStatus> {
        const response = await fetch(`${this.apiUrl}/verify`, {
            headers: {
                [this.apiKeyName]: apiKey,
            },
        });

        if (!response.ok) {
            throw new ApiNotReachableError();
        }

        const data = await response.json();

        // Transformation snake_case → camelCase
        return { isValid: data.is_valid } as ApiKeyStatus;
    }
}
