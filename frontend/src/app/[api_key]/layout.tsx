import { ApiNotReachableError } from '@/adapters/api/errors'
import { getVerifyApiKeyUseCase } from '@/container/Containers'

export default async function ApiKeyLayout({
    params,
    children,
}: {
    params: { api_key: string }
    children: React.ReactNode;
}) {
    const verifyApiKey = getVerifyApiKeyUseCase()

    try {
        const apiStatus = await verifyApiKey.execute(params.api_key)

        if (apiStatus?.isValid) {
            return <div>{children}</div>
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
