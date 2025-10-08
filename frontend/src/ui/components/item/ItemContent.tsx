import { Label } from "@radix-ui/react-label";
import { ReactNode } from "react";
import { Input } from "@/components/ui/input";
import type { Content } from "@/core/entities/Session";
import { TextContent } from "./contents/TextContent";

type ItemContentProps = {
    name: string;
    content: Content;
    handleChange: (x: string) => void;
};

export function ItemContent({ name, content, handleChange }: ItemContentProps) {
    switch (content.type) {
        case "text":
            return <TextContent value={name} handleChange={handleChange} />;
        default:
            return <p>Type de content invalide</p>;
    }
}
