import type { Results } from "../entities/Results";

export interface IResultsRepository {
    get(apiKey: string): Promise<Results>;
}
