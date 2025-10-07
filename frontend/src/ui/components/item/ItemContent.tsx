import { ReactNode } from 'react';

import { Content } from '@/core/entities/Session'
import { TextContent } from './contents/TextContent'
import { Label } from '@radix-ui/react-label';
import { Input } from '@/components/ui/input';

type ItemContentProps = {
    name: string;
    content: Content;
    handleChange: (x: string) => void;
}

export function ItemContent({ name, content, handleChange }: ItemContentProps) {
    switch (content.type) {
        case "text":
            return <TextContent value={name} handleChange={handleChange} />
        default:
            return <p>Type de content invalide</p>
    }
}