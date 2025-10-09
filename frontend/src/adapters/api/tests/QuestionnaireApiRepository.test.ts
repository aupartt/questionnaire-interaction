import { QuestionnaireApiRepository } from "../QuestionnaireApiRepository";

const mockApiResponse = [
    {
        id: 1,
        name: "Foo",
        description: "FooDesc",
        session_id: 1,
        status: "completed",
        is_next: false,
    },
    {
        id: 2,
        name: "Bar",
        description: "BarDesc",
        session_id: null,
        status: null,
        is_next: true,
    },
];

const mockRepositoryResponse = [
    {
        id: 1,
        name: "Foo",
        description: "FooDesc",
        sessionId: 1,
        status: "completed",
        isNext: false,
    },
    {
        id: 2,
        name: "Bar",
        description: "BarDesc",
        sessionId: null,
        status: null,
        isNext: true,
    },
];

describe("QuestionnaireApiRepository", () => {
    let repository: QuestionnaireApiRepository;
    let fetchMock: jest.SpyInstance;
    const OLD_ENV = process.env;

    beforeEach(() => {
        jest.resetModules();

        process.env.API_URL = "https://api.com";
        process.env.API_KEY_NAME = "MY_API_NAME";

        fetchMock = jest.spyOn(global, "fetch").mockImplementation(() =>
            Promise.resolve({
                ok: true,
                json: () => Promise.resolve(mockApiResponse),
            } as Response),
        );

        repository = new QuestionnaireApiRepository();
        process.env = { ...OLD_ENV };
    });

    it("devrait récupérer et transformer les questionnaires", async () => {
        const questionnaires = await repository.getAll("foo");

        process.env.API_URL = "https://api.com";
        process.env.API_KEY_NAME = "MY_API_NAME";

        expect(fetchMock).toHaveBeenCalledWith(
            expect.stringContaining(`${process.env.API_URL}/questionnaires`),
            expect.objectContaining({
                headers: {
                    [process.env.API_KEY_NAME]: "foo",
                },
            }),
        );

        expect(questionnaires).toStrictEqual(mockRepositoryResponse);
    });

    it("devrait lancer une erreur si la réponse est ko", async () => {
        fetchMock.mockResolvedValueOnce({
            ok: false,
            status: 500,
        });

        await expect(repository.getAll("foo")).rejects.toThrow(
            "API non disponible, vérifier l'url ou votre connexion.",
        );
    });

    it("devrait lancer une erreur si fetch échoue", async () => {
        fetchMock.mockRejectedValueOnce(new Error("Network error"));

        await expect(repository.getAll("foo")).rejects.toThrow("Network error");
    });
});
