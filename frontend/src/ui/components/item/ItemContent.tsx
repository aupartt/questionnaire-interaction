import type { Content } from "@/core/entities/Session";
import { TextContent } from "./contents/TextContent";

type ItemContentProps = {
    content: Content;
    value: string;
    handleChange: (x: string) => void;
};

export function ItemContent({ content, value, handleChange }: ItemContentProps) {
    switch (content.type) {
        case "text":
            return <TextContent handleChange={handleChange} value={value} />;
        default:
            return <p>Type de content invalide</p>;
    }
}
