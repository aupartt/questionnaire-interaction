import { Badge } from "@/components/ui/badge";
import { useSessionContext } from "@/ui/contexts/SessionContext";
import { useTheme } from "@/ui/contexts/ThemeContext";
import { SpacerWrapper } from "../SpacerWrapper";

const Spacer = <span className="flex-grow mx-1 h-0.5 bg-gray-300"></span>;

export function ItemStepper() {
    const { session } = useSessionContext();

    return (
        <div className="flex items-center justify-between w-full px-1">
            <SpacerWrapper spacer={Spacer}>
                {session?.items.map((item, id) => (
                    <Item
                        key={item.id}
                        id={id + 1}
                        isActive={
                            session.getItemStatus(item.id) === "completed" ||
                            item.id === session.currentItem.id
                        }
                    />
                ))}
            </SpacerWrapper>
        </div>
    );
}

const Item = ({ id, isActive }: { id: number; isActive: boolean }) => {
    const { className } = useTheme();
    const bgClassName = isActive ? className.bgPrimary : className.bgSecondary;
    return (
        <Badge
            className={`h-5 min-w-5 rounded-full px-1 border-0 text-white ${bgClassName}`}
            variant="default"
        >
            {id}
        </Badge>
    );
};
