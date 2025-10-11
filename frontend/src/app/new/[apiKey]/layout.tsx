import { getVerifyKeyUseCase } from "@/container/Containers";
import { ThemeProvider } from "@/ui/contexts/ThemeContext";

const VerifyApiKey = getVerifyKeyUseCase();

export default async function ApiKeyLayout({
    children,
    params
}: {
    children: React.ReactNode;
    params: Promise<{ apiKey: string }>
}) {
    const { apiKey } = await params

    const keyStatus = await VerifyApiKey.execute(apiKey)

    if (!keyStatus) {
        return <div>Clé API non valide.</div>
    }

    return (
        <main>
            <ThemeProvider>
                {children}
            </ThemeProvider>
        </main>
    );
}
