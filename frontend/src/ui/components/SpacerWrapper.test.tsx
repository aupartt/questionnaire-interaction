import "@testing-library/jest-dom";
import { cleanup, render, screen } from "@testing-library/react";
import { SpacerWrapper } from "./SpacerWrapper";

describe("SpacerWrapper", () => {
    afterEach(cleanup);

    it("devrait correctement ajouter les spacer entre chaque enfants", () => {
        const { container } = render(
            <SpacerWrapper
                spacer={<span data-testid="spacer">space-spacer</span>}
            >
                <div>1</div>
                <div>2</div>
                <div>3</div>
            </SpacerWrapper>,
        );

        expect(container.children).toHaveLength(5);
        const spacers = screen.getAllByTestId("spacer");
        expect(spacers).toHaveLength(2);
        expect(spacers[0]).toHaveTextContent("space-spacer");
    });

    it("devrait ne pas ajouter des spacer si un seul enfant", () => {
        const { container } = render(
            <SpacerWrapper
                spacer={<span data-testid="spacer">space-spacer</span>}
            >
                <div>1</div>
            </SpacerWrapper>,
        );

        expect(container.children).toHaveLength(1);
    });

    it("devrait rendre zero éléments si aucun enfant fournis", () => {
        const { container } = render(
            <SpacerWrapper
                spacer={<span data-testid="spacer">space-spacer</span>}
            >
                <></>
            </SpacerWrapper>,
        );

        expect(container.children).toHaveLength(0);
    });

    it("devrait rendre les enfants dans le bon ordre", () => {
        const { container } = render(
            <SpacerWrapper
                spacer={<span data-testid="spacer">space-spacer</span>}
            >
                <div data-testid="child-1"></div>
                <div data-testid="child-2"></div>
            </SpacerWrapper>,
        );

        expect(container.children).toHaveLength(3);
        expect(container.children[0].getAttribute("data-testid")).toBe(
            "child-1",
        );
        expect(container.children[1].getAttribute("data-testid")).toBe(
            "spacer",
        );
        expect(container.children[2].getAttribute("data-testid")).toBe(
            "child-2",
        );
    });
});
