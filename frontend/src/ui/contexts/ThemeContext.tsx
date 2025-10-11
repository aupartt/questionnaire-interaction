"use client";

import { createContext, useContext, ReactNode } from "react";

type Theme = {
    class: {
        textPrimary: string;
        textSecondary: string;
        bgPrimary: string;
        bgSecondary: string;
    }
};

const defaultTheme: Theme = {
    class: {
        textPrimary: "text-green-600",
        textSecondary: "string",
        bgPrimary: "bg-green-600",
        bgSecondary: "bg-green-100"
    }
}

export const ThemeContext = createContext<Theme | undefined>(undefined);

export const ThemeProvider = ({ children }: { children: ReactNode; }) => {
    return (
        <ThemeContext value={defaultTheme}>
            {children}
        </ThemeContext>
    );
};

export function useTheme() {
    const context = useContext(ThemeContext);
    if (!context) {
        throw new Error("useQuestionnaireContext must be used within a ThemeProvider");
    }
    return context;
}
