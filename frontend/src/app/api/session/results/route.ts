import { NextRequest, NextResponse } from "next/server";
import { getResultsUseCase } from "@/container/Containers"

export async function GET(request: NextRequest) {
    const searchParams = request.nextUrl.searchParams;
    const apiKey = searchParams.get("apiKey");
    const questionnaireId = searchParams.get("questionnaireId");
    const sessionId = searchParams.get("sessionId");

    if (!apiKey || !questionnaireId || !sessionId) {
        return NextResponse.json(
            { error: "Paramètres non valide." },
            { status: 400 }
        );
    }

    try {
        const getResults = getResultsUseCase()
        const res = await getResults.execute(apiKey, parseInt(questionnaireId), parseInt(sessionId))
        return NextResponse.json(res);
    } catch (error) {
        console.error("Erreur API:", error);
        return NextResponse.json(
            { error: "Erreur lors de la récupération des résultats" },
            { status: 500 }
        );
    }
}
