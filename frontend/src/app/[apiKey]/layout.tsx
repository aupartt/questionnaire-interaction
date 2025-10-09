export default async function ApiKeyLayout({
    children,
    params
}: Readonly<{
    children: React.ReactNode;
    params: Promise<{ apiKey: string }>
}>) {
    const { apiKey } = await params
    return (
        <main>
            {children}
        </main>
    );
}
