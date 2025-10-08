"use client";

import { useParams } from "next/navigation";
import { useEffect } from "react";
import { ErrorMessage } from "@/ui/components/ErrorMessage";
import { Item } from "@/ui/components/item";
import { useSessionContext } from "@/ui/contexts/SessionContext";

export default function QuestionnairePage() {
    const params = useParams<{ questionnaireId: string }>();
    const { session, loadingAnswer, error, initSession } = useSessionContext();

    useEffect(() => {
        initSession(params.questionnaireId);
    }, [params]);

    return (
        <main className="container mx-auto p-4">
            {session && <Item />}
            {loadingAnswer && <p>Loading...</p>}
            {error && <ErrorMessage className="mt-5" title={error} />}
        </main>
    );
}
