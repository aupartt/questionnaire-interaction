import { Input } from "@/components/ui/input";

type TextContentProps = {
    handleChange: (x: string) => void;
};

export function TextContent({ handleChange }: TextContentProps) {
    return <Input
        type="text"
        onChange={(e) => handleChange(e.currentTarget.value)}
    />;
}
