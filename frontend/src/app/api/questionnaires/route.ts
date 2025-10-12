import { type NextRequest, NextResponse } from "next/server";
import { getAllQuestionnaireUseCase } from "@/container/Containers";

export async function GET(request: NextRequest) {
    const searchParams = request.nextUrl.searchParams;
    const apiKey = searchParams.get("apiKey");

    if (!apiKey) {
        return NextResponse.json(
            { error: "API Key manquante" },
            { status: 400 },
        );
    }

    try {
        const getAllQuestionnaire = getAllQuestionnaireUseCase();
        const questionnaire = await getAllQuestionnaire.execute(apiKey);
        return NextResponse.json(questionnaire);
    } catch (error) {
        console.error("Erreur API:", error);
        return NextResponse.json(
            { error: "Erreur lors de la récupération des questionnaires" },
            { status: 500 },
        );
    }
}
