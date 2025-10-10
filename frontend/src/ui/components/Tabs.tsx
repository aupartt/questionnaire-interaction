// This is inspired from next-app-router-playground parallel-routing

"use client";

import { ItemShort } from "@/core/entities/Session";
import { usePathname } from "next/navigation";


export function Tabs({ basePath, items }: { basePath: string; items: ItemShort[] }) {
    return (
        <div className="flex flex-col my-4">
            {items.map((item) => (
                <Tab key={basePath + item.id} item={item} basePath={basePath} />
            ))}
        </div>
    );
}

export function Tab({
    basePath = '',
    item,
}: {
    basePath?: string;
    item: ItemShort;
}) {
    const href = item.id ? `${basePath}/${item.id}` : basePath;
    const pathname = usePathname();
    const isActive = pathname === href;

    return (
        <div className={`flex ${isActive ? "bg-green-100" : ""} p-3 justify-between`}>
            <p className="font-bold">{item.name}</p>
            <span>{isActive ? 'x' : 'o'}</span>
        </div>
    )
}
