import { Badge } from "@/components/ui/badge";
import { useSessionContext } from "@/ui/contexts/SessionContext";

const Spacer = () => <span className="flex-grow mx-1 h-0.5 bg-gray-300"></span>;

const ProgressBadge = ({
    isActive,
    value,
}: {
    isActive: boolean | null;
    value: number;
}) => {
    const statusClass = isActive ? "bg-green-600" : "bg-gray-400";
    return (
        <Badge
            className={`h-5 min-w-5 rounded-full px-1 border-0 text-white ${statusClass}`}
            variant="default"
        >
            {value}
        </Badge>
    );
};

export function ProgressStepper() {
    const { session } = useSessionContext();

    const itemIsActive = (itemId: number) => {
        return (
            itemId === session!.currentItem.id ||
            session!.getItemStatus(itemId) !== null
        );
    };

    const separatedList = session!.items
        .map((item, id) => (
            <ProgressBadge
                key={item.id}
                value={id}
                isActive={itemIsActive(item.id)}
            />
        ))
        .reduce((prev, current) => {
            if (prev.length === 0) {
                return [current];
            }
            prev.push(<Spacer key={`spacer-${current.key}`} />);
            prev.push(current);
            return prev;
        }, [] as React.ReactNode[]);

    return (
        <div className="flex items-center justify-between w-full px-1">
            {separatedList}
        </div>
    );
}
