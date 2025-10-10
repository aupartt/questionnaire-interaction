import { Tabs } from "@/ui/components/Tabs"
import db from "@/lib/db";


export default async function QuestionnaireLayout({
    children,
    params
}: Readonly<{
    children: React.ReactNode;
    params: Promise<{ qId: number, apiKey: string }>
}>) {
    const { qId, apiKey } = await params

    const items = db.getItems(qId)
    const basePath = `/${apiKey}/questionnaires/${qId}/items`

    return (
        <main className="">
            <div className="flex h-screen">
                <div className="w-1/3 border-r border-gray-200">
                    <div className="h-10"></div>
                    <h2 className="font-black text-2xl text-green-600 p-3">Aurélien</h2>
                    <p className="text-sm pl-3">Aidez-nous à personnaliser votre expérience en nous parlant un peu de vous !</p>
                    <Tabs basePath={basePath} items={items} />
                </div>
                {children}
            </div>
        </main>
    );
}
