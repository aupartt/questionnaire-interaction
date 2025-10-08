import { IAuthRepository } from "@/core/ports/IAuthRepository";
import { ApiKeyStatus } from "@/core/entities/ApiKeyStatus";
import { ApiNotReachableError } from "./errors";

export class AuthApiRepository implements IAuthRepository {
    private apiUrl = `${process.env.NEXT_PUBLIC_API_URL}`;

    async verify(apiKey: string): Promise<ApiKeyStatus> {
        const response = await fetch(`${this.apiUrl}/verify`, {
            headers: {
                "X-API-Key": apiKey,
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
