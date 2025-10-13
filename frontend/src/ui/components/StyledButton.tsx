import { Button } from "@/components/ui/button";
import Link from "next/link";
import { ReactNode } from "react";

type StyledButtonProps = {
    className?: string;
    value: string;
    action?: () => void;
    href?: string;
};
export function StyledButton({
    className,
    value,
    action,
    href,
}: StyledButtonProps) {
    const buttonComponent = (
        <Button
            className={`rounded-full bg-green-600 hover:bg-green-700 cursor-pointer transition-colors ${className}`}
            onClick={action}
        >
            {value}
        </Button>
    );

    if (action) {
        buttonComponent.props.onClick = action;
        return buttonComponent;
    }

    if (href) return <Link href={href}>{buttonComponent}</Link>;

    return "action and href not specified.";
}
