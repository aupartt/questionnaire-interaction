import { SessionProvider } from "@/ui/contexts/SessionContext";

export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
        <SessionProvider>
            {children}
        </SessionProvider>
    );
}