"use client";

import { Tabs } from "@/ui/components/Tabs"
import { useSessionContext } from "@/ui/contexts/SessionContext";

export default function SidebarPage() {
    const { session } = useSessionContext()

    return (
        <div className="w-1/3 border-r border-gray-200">
            <div className="h-10"></div>
            <h2 className="font-black text-2xl text-green-600 p-3">Session: {session?.id} ({session?.answers.length} réponses)</h2>
            <p className="text-sm pl-3">Aidez-nous à personnaliser votre expérience en nous parlant un peu de vous !</p>
            <Tabs />
        </div>)
}
