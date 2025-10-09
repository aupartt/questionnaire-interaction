import { Button } from "@/components/ui/button";

type StyledButtonProps = {
    className?: string;
    value: string;
    action?: () => void;
};

export function StyledButton({ className, value, action }: StyledButtonProps) {
    if (action) {
        return (
            <Button
                className={`rounded-full bg-green-600 hover:bg-green-700 cursor-pointer transition-colors ${className}`}
                onClick={action}
            >
                {value}
            </Button>
        );
    }

    return (
        <Button
            className={`rounded-full bg-green-600 hover:bg-green-700 cursor-pointer transition-colors ${className}`}
        >
            {value}
        </Button>
    );
}
