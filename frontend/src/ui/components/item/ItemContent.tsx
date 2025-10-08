import type { Content } from "@/core/entities/Session";
import { TextContent } from "./contents/TextContent";

type ItemContentProps = {
    content: Content;
    handleChange: (x: string) => void;
};

export function ItemContent({ content, handleChange }: ItemContentProps) {
    switch (content.type) {
        case "text":
            return <TextContent handleChange={handleChange} />;
        default:
            return <p>Type de content invalide</p>;
    }
}
