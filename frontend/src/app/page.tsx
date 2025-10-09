import { StyledButton } from "@/ui/components/StyledButton";
import Link from "next/link";

export default function Home() {
    const apiKeyMock = process.env.API_KEY_MOCK;

    return (
        <div className="flex flex-col gap-3 items-center justify-center min-h-svh">
            <h2 className="font-bold">Questionnaire Interaction</h2>
            <Link href={`/${apiKeyMock}/onboarding`}>
                <StyledButton value="on board !" />
            </Link>
        </div>
    );
}
