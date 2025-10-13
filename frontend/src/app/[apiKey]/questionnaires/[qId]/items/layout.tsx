export default async function QuestionnaireLayout({
    sidebar,
    item,
}: {
    sidebar: React.ReactNode;
    item: React.ReactNode;
}) {
    return (
        <>
            {sidebar}
            {item}
        </>
    );
}
