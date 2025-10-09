'use client'

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button"
import Image from "next/image";
import Link from "next/link";
import { use } from "react";

export default function ApiKeyPage({
    params
}: {
    params: Promise<{ apiKey: string }>
}) {
    const { apiKey } = use(params)

    return (
        <div className="flex h-screen">
            <div className="w-1/3 border-r border-gray-200">
                <div className="h-10"></div>
                <h2 className="font-black text-2xl text-green-600 p-3">Aurélien</h2>
                <p className="text-sm pl-3">Aidez-nous à personnaliser votre expérience en nous parlant un peu de vous !</p>
                <div className="flex flex-col my-4">
                    <div className="flex bg-green-100 p-3 justify-between">
                        <p className="font-bold">Vous êtes actuellement...</p>
                        <span>x</span>
                    </div>
                    <div className="flex p-3 justify-between">
                        <p className="font-bold text-gray-400">Ma dernière formation</p>
                        <span>o</span>
                    </div>
                    <div className="flex p-3 justify-between">
                        <p className="font-bold text-gray-400">Ma dernière expérience professionnelle</p>
                        <span>o</span>
                    </div>
                </div>
            </div>

            <div className="flex-1 p-4 overflow-auto">
                <div className="h-10"></div>
                <div className="flex flex-col item-center gap-7 mx-auto min-w-2xl w-1/2">
                    <div className="flex items-center justify-between w-full px-1">
                        <Badge
                            className="h-5 min-w-5 rounded-full px-1 border-0 text-white bg-green-600" // bg-gray-400
                            variant="default"
                        >
                            1
                        </Badge>
                        <span className="flex-grow mx-1 h-0.5 bg-gray-300"></span>
                        <Badge
                            className="h-5 min-w-5 rounded-full px-1 border-0 text-white bg-green-600" // bg-gray-400
                            variant="default"
                        >
                            2
                        </Badge>
                        <span className="flex-grow mx-1 h-0.5 bg-gray-300"></span>
                        <Badge
                            className="h-5 min-w-5 rounded-full px-1 border-0 text-white bg-gray-400"
                            variant="default"
                        >
                            3
                        </Badge>
                    </div>
                    <h2 className="font-bold">Vous êtes actuellement...</h2>
                    <ul className="">
                        <li className="p-3 text-center border-2 rounded-t-sm font-bold border-gray-400 text-gray-400">En période de transition</li>
                        <li className="p-3 text-center border-x-2 font-bold border-gray-400 text-gray-400">En formation</li>
                        <li className="p-3 text-center border-2 font-bold border-gray-400 text-gray-400">En poste</li>
                        <li className="p-3 text-center border-x-2 font-bold border-gray-400 text-green-600 bg-green-100">En recherche d'emploi</li>
                        <li className="p-3 text-center border-2 rounded-b-sm font-bold border-gray-400 text-gray-400">En reconversion</li>
                    </ul>
                    <div className="flex flex-row-reverse">
                        <Button
                            className="rounded-full bg-green-600 hover:bg-green-700 transition-colors"
                        >Suivant</Button>
                    </div>
                </div>
            </div>
        </div>
    )
}
