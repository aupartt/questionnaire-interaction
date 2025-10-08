import { ApiNotReachableError } from '@/adapters/api/errors'
import { getVerifyApiKeyUseCase } from '@/container/Containers'
import { SessionProvider } from "@/ui/contexts/SessionContext";

export default async function ApiKeyLayout({
    params,
    children,
}: {
    params: Promise<{ api_key: string }>
    children: React.ReactNode;
}) {
    const verifyApiKey = getVerifyApiKeyUseCase()
    const { api_key } = await params

    try {
        const apiStatus = await verifyApiKey.execute(api_key)

        if (apiStatus?.isValid) {
            return <SessionProvider apiKey={api_key}>
                {children}
            </SessionProvider>
        }

        return (
            <div style={{ padding: '20px', textAlign: 'center', color: 'red' }}>
                <p>Clé API non valide</p>
            </div>
        )
    }
    catch (err) {
        if (err instanceof ApiNotReachableError) {
            return <p>{err.message}</p>
        }
    }
}
