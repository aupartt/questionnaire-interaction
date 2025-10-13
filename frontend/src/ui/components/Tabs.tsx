// This is inspired from next-app-router-playground parallel-routing

"use client";

import type { ItemShort } from "@/core/entities/Session";
import { useSessionContext } from "../contexts/SessionContext";

export function Tabs() {
    const { session } = useSessionContext();
    return (
        <div className="flex flex-col my-4">
            {session?.items.map((item, _id) => (
                <Tab key={item.id} item={item} />
            ))}
        </div>
    );
}

export function Tab({ item }: { item: ItemShort }) {
    const { session } = useSessionContext();

    const isActive = item.id === session?.currentItem.id;
    const isDone = Boolean(session?.answers.find((i) => i.itemId === item.id));
    let statusItem = isActive ? "-" : "o";
    if (isDone) statusItem = "x";

    return (
        <div
            className={`flex ${isActive ? "bg-green-100" : ""} p-3 justify-between`}
        >
            <p className="font-bold">{item.name}</p>
            <span>{statusItem}</span>
        </div>
    );
}
