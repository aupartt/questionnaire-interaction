import { Input } from "@/components/ui/input";

type TextContentProps = {
    handleChange: (x: string) => void;
    value: string;
};

export function TextContent({ handleChange, value }: TextContentProps) {
    return (
        <Input
            type="text"
            onChange={(e) => handleChange(e.currentTarget.value)}
            value={value}
        />
    );
}
