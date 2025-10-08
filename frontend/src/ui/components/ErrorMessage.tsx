import { AlertCircleIcon } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

type ErrorMessageProps = {
    className?: string;
    title: string;
    message?: string;
};

export function ErrorMessage({ className, title, message }: ErrorMessageProps) {
    return (
        <Alert className={className} variant="destructive">
            <AlertCircleIcon />
            <AlertTitle>{title}</AlertTitle>
            {message && (
                <AlertDescription>
                    <p>{message}</p>
                </AlertDescription>
            )}
        </Alert>
    );
}
