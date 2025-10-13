import "@testing-library/jest-dom";
import type { ApiKeyStatus } from "@/core/entities/ApiKeyStatus";
import type { IAuthRepository } from "@/core/ports/IAuthRepository";
import { VerifyApiKey } from "./VerifyApiKey";

describe("VerifyApiKey", () => {
    it("devrait correctement renvoyer la valeur de isValid", async () => {
        const mockValidStatus: ApiKeyStatus = { isValid: true };
        const mockAuthRepository: IAuthRepository = {
            verify: jest.fn().mockResolvedValue(mockValidStatus),
        };

        const usecase = new VerifyApiKey(mockAuthRepository);

        const res = await usecase.execute("foo");
        expect(res).toBeTruthy();
    });
});
