import { NextRequest, NextResponse } from "next/server";
import { getSubmitAnswerUseCase } from "@/container/Containers"

export async function POST(request: NextRequest) {
    const searchParams = request.nextUrl.searchParams;
    const apiKey = searchParams.get("apiKey");
    const questionnaireId = searchParams.get("questionnaireId");
    const sessionId = searchParams.get("sessionId");

    const body = await request.json();
    const { answer } = body;

    if (!apiKey || !questionnaireId || !sessionId || !answer) {
        return NextResponse.json(
            { error: "Paramètres non valide." },
            { status: 400 }
        );
    }

    try {
        const getSubmitAnswer = getSubmitAnswerUseCase()
        const res = await getSubmitAnswer.execute(apiKey, parseInt(questionnaireId), parseInt(sessionId), answer)
        return NextResponse.json(res);
    } catch (error) {
        console.error("Erreur API:", error);
        return NextResponse.json(
            { error: "Erreur lors de l'envois de la réponse" },
            { status: 500 }
        );
    }
}
