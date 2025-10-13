import React, { Children } from "react";

interface SpacerWrapperProps {
    spacer: React.ReactNode;
    children: React.ReactNode;
}

export function SpacerWrapper({ children, spacer }: SpacerWrapperProps) {
    // 1. Converti les children en un tableau pour pouvoir itérer dessus
    const childList = Children.toArray(children);

    const separatedChild = childList.reduce<React.ReactNode[]>(
        (acc, child, index) => {
            const childKey = React.isValidElement(child)
                ? child.key
                : `child-${index}`;
            const safeChildKey =
                childKey !== null ? String(childKey) : `child-index-${index}`;
            if (index > 0) {
                const spacerElement = React.isValidElement(spacer)
                    ? React.cloneElement(spacer, {
                          key: `spacer-${safeChildKey}`,
                      })
                    : spacer;

                acc.push(spacerElement);
            }

            acc.push(child);

            return acc;
        },
        [] as React.ReactNode[],
    );

    return <>{separatedChild}</>;
}
