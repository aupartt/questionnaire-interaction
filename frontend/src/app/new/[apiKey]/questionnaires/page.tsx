import { Button } from "@/components/ui/button"
import Image from "next/image";
import Link from "next/link";
import db from "@/lib/db";


export default async function ApiKeyPage({
    params
}: {
    params: Promise<{ apiKey: string }>
}) {
    const { apiKey } = await params

    const qId = 0

    const questionnaires = db.getQuestionnaires()

    const nextQ = questionnaires[qId]

    return (
        <div className="grid place-items-center h-screen">
            <div className="flex flex-wrap gap-10 max-w-sm flex-col items-center">
                <div className="flex px-[50px] items-center w-full justify-center gap-4">
                    <span className="font-bold text-gray-900">Étape 1</span>
                    <div className="flex-grow border-t border-dotted border-green-700 relative">
                    </div>
                    <span className="font-bold text-gray-400">Étape 2</span>
                </div>
                <div className="flex w-full justify-between">
                    <Image
                        className="border-1"
                        src="https://a.pinatafarm.com/540x494/76636b7956/tada-will-smith.jpg"
                        alt="result img"
                        width={150}
                        height={150}
                        priority
                    />
                    <Image
                        className="border-1"
                        src="https://a.pinatafarm.com/540x494/76636b7956/tada-will-smith.jpg"
                        alt="result img"
                        width={150}
                        height={150}
                        priority
                    />
                </div>
                <div>
                    <h2 className="text-2xl text-center font-black text-green-600">{nextQ.name}</h2>
                </div>
                <div>
                    <p className="text-center text-gray-500">{nextQ.description}</p>
                </div>
                <Link href={`questionnaires/${nextQ.id}`}>
                    <Button
                        className="rounded-full bg-green-600 hover:bg-green-700 transition-colors"
                    >
                        C'est parti !
                    </Button>
                </Link>
                <div className="w-full flex flex-col items-center">
                    <p className="pb-3 text-gray-500 text-sm" >Je m'arrête là pour aujourd'hui</p>
                    <Link className="font-bold text-gray-500 underline" href="#">Voir mes résultats</Link>
                </div>
            </div>
        </div>
    )
}
