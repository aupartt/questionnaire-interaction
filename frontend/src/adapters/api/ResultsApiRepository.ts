import type { Results } from "@/core/entities/Results";
import type { IResultsRepository } from "@/core/ports/IResultsRepository";
import { ApiNotReachableError } from "./errors";

type ResultsResponse = {
    img_url: string;
};

export class ResultsApiRepository implements IResultsRepository {
    private apiUrl = `${process.env.NEXT_PUBLIC_API_URL}`;

    async get(apiKey: string): Promise<Results> {
        const response = await fetch(`${this.apiUrl}/questionnaires`, {
            headers: {
                "X-API-Key": apiKey,
            },
        });

        if (!response.ok) {
            throw new ApiNotReachableError();
        }

        const data: ResultsResponse = await response.json();

        // Transformation snake_case → camelCase
        return {
            imgUrl: data.img_url
        }
    }
}
