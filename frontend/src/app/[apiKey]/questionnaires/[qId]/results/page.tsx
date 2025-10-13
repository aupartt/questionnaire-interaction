"use client";

import useSWR from "swr";

import type { Results } from "@/core/entities/Results";
import Image from "next/image";
import { use } from "react";
import { useSessionContext } from "@/ui/contexts/SessionContext";
import { StyledButton } from "@/ui/components/StyledButton";
import { useRouter } from "next/navigation";

type FetchArgs = Parameters<typeof fetch>;
const fetcher = (...args: FetchArgs) =>
    fetch(...args).then((res) => res.json());

export default function ResultsPage({
    params,
}: {
    params: Promise<{ apiKey: string; qId: number }>;
}) {
    const router = useRouter();
    const { apiKey, qId } = use(params);
    const { session } = useSessionContext();
    const { data, error, isLoading } = useSWR<Results>(
        `/api/session/results?apiKey=${apiKey}&questionnaireId=${qId}&sessionId=${session?.id}`,
        fetcher,
    );

    if (isLoading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;

    return (
        <div className="w-full flex flex-col justify-center items-center">
            <div className="flex flex-col justify-center items-center">
                <p className="font-bold pb-5">Questionnaire fini !</p>
                {data?.imgUrl && (
                    <Image
                        src={data.imgUrl}
                        alt="result img"
                        width={180}
                        height={180}
                        priority
                    />
                )}
                <p className="pt-5">
                    Cliquez sur continuer pour retourner à la liste des
                    questionnaires
                </p>
                <div className="pt-5">
                    <StyledButton
                        value="Continuer"
                        action={() => router.push(`/${apiKey}/questionnaires`)}
                    />
                </div>
            </div>
        </div>
    );
}
