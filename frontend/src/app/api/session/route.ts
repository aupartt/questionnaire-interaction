import { NextRequest, NextResponse } from "next/server";
import { getSessionUseCase } from "@/container/Containers"

export async function GET(request: NextRequest) {
    const searchParams = request.nextUrl.searchParams;
    const apiKey = searchParams.get("apiKey");
    const questionnaireId = searchParams.get("questionnaireId");

    if (!apiKey) {
        return NextResponse.json(
            { error: "API Key manquante" },
            { status: 400 }
        );
    }

    if (!questionnaireId) {
        return NextResponse.json(
            { error: "ID Questionnaire requis" },
            { status: 400 }
        );
    }

    try {
        const getSession = getSessionUseCase()
        const session = await getSession.execute(apiKey, parseInt(questionnaireId))
        return NextResponse.json(session);
    } catch (error) {
        console.error("Erreur API:", error);
        return NextResponse.json(
            { error: "Erreur lors de la récupération de la session" },
            { status: 500 }
        );
    }
}
