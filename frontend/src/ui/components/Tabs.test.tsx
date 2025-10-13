import "@testing-library/jest-dom";
import { cleanup, render } from "@testing-library/react";
import { Session } from "@/core/entities/Session";
import { Tab, Tabs } from "./Tabs";

const mockUsePathname = jest.fn();
const mockUseQuestionnaireContext = jest.fn();

jest.mock("next/navigation", () => ({
    usePathname() {
        return mockUsePathname();
    },
}));

jest.mock("../contexts/SessionContext", () => ({
    useSessionContext() {
        return mockUseQuestionnaireContext();
    },
}));

describe("Tab", () => {
    let sessionMock: Session;

    beforeEach(() => {
        sessionMock = new Session(
            1,
            1,
            [],
            [],
            {
                id: 1,
                name: "Foo",
                question: {
                    type: "text",
                    value: "Who?",
                },
                content: {
                    type: "text",
                },
            },
            "active",
        );
    });

    afterEach(cleanup);

    it("devrait être marqué comme actif", () => {
        sessionMock.currentItem.id = 42;
        mockUseQuestionnaireContext.mockImplementation(() => ({
            session: sessionMock,
        }));
        const mockItem = {
            id: 42,
            name: "foo",
        };

        const { container } = render(<Tab item={mockItem} />);

        expect(container.children[0].getAttribute("class")).toContain("bg-");
    });

    it("devrait être marqué comme inactif", () => {
        sessionMock.currentItem.id = 42;
        mockUseQuestionnaireContext.mockImplementation(() => ({
            session: sessionMock,
        }));
        const mockItem = {
            id: 1,
            name: "foo",
        };
        const { container } = render(<Tab item={mockItem} />);

        expect(container.children[0].getAttribute("class")).not.toContain(
            "bg-",
        );
    });
});

describe("Tabs", () => {
    let sessionMock: Session;

    beforeEach(() => {
        sessionMock = new Session(
            1,
            1,
            [],
            [],
            {
                id: 1,
                name: "Foo",
                question: {
                    type: "text",
                    value: "Who?",
                },
                content: {
                    type: "text",
                },
            },
            "active",
        );
    });

    afterEach(cleanup);

    it("devrait rendre les enfants (le salop !)", () => {
        const mockItems = [
            {
                id: 1,
                name: "foo",
            },
            {
                id: 2,
                name: "bar",
            },
        ];
        sessionMock.items = mockItems;
        mockUseQuestionnaireContext.mockImplementation(() => ({
            session: sessionMock,
        }));

        const { container } = render(<Tabs />);

        const wrapper = container.firstChild as HTMLElement;
        expect(wrapper.children).toHaveLength(2);
    });
});
