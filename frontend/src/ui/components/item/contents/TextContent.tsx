import { Label } from '@radix-ui/react-label';
import { Input } from '@/components/ui/input';

type TextContentProps = {
    value: string
    handleChange: (x: string) => void;
}

export function TextContent({ value, handleChange }: TextContentProps) {
    return <>
        <Input type='text' onChange={e => handleChange(e.currentTarget.value)} />
    </>
} 