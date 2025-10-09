import type { Results } from "@/core/entities/Results";
import type { IResultsRepository } from "@/core/ports/IResultsRepository";
import { ApiNotReachableError } from "./errors";

type ResultsResponse = {
    img_url: string;
};

export class ResultsApiRepository implements IResultsRepository {
    private apiUrl = `${process.env.API_URL}`;
    private apiKeyName = `${process.env.API_KEY_NAME}`;

    async get(
        apiKey: string,
        questionnaireId: number,
        sessionId: number,
    ): Promise<Results> {
        const response = await fetch(
            `${this.apiUrl}/questionnaire/${questionnaireId}/session/${sessionId}/results`,
            {
                method: "POST",
                headers: {
                    [this.apiKeyName]: apiKey,
                },
            },
        );

        if (!response.ok) {
            throw new ApiNotReachableError();
        }

        const data: ResultsResponse = await response.json();

        // Transformation snake_case → camelCase
        return {
            imgUrl: data.img_url,
        };
    }
}
