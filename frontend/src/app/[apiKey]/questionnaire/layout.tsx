export default async function QuestionnaireLayout({
    children,
    params
}: Readonly<{
    children: React.ReactNode;
    params: Promise<{ apiKey: string }>
}>) {
    const { apiKey } = await params
    return (
        <main className="">
            {children}
        </main>
    );
}
