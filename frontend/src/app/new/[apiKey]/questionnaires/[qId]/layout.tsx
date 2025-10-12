import { SessionProvider } from "@/ui/contexts/SessionContext";

export default async function QuestionnaireLayout({
    children,
    params
}: {
    children: React.ReactNode;
    params: Promise<{ qId: string, apiKey: string }>
}) {
    const { qId, apiKey } = await params

    return (
        <main className="">
            <div className="flex h-screen">
                <SessionProvider apiKey={apiKey} questionnaireId={parseInt(qId)}>
                    {children}
                </SessionProvider>
            </div>
        </main>
    );
}
