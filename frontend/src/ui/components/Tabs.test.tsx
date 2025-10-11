import '@testing-library/jest-dom';
import { renderHook, act, render, cleanup, screen } from '@testing-library/react';
import { Tabs, Tab } from './Tabs';
import { ItemShort } from '@/core/entities/Session';

const mockUsePathname = jest.fn();

jest.mock('next/navigation', () => ({
    usePathname() {
        return mockUsePathname();
    },
}));


describe('Tab', () => {
    afterEach(cleanup);

    it("devrait être marqué comme actif", () => {
        mockUsePathname.mockImplementation(() => '/foo/bar/1');

        const mockBasePath = '/foo/bar'
        const mockItem = {
            id: 1,
            name: "foo"
        }
        const { container } = render(<Tab basePath={mockBasePath} item={mockItem} />);

        expect(container.children[0].getAttribute("class")).toContain("bg-")
    });

    it("devrait être marqué comme inactif", () => {
        mockUsePathname.mockImplementation(() => '/foo/bar/2');

        const mockBasePath = '/foo/bar'
        const mockItem = {
            id: 1,
            name: "foo"
        }
        const { container } = render(<Tab basePath={mockBasePath} item={mockItem} />);

        expect(container.children[0].getAttribute("class")).not.toContain("bg-")
    });
});


describe('Tabs', () => {
    afterEach(cleanup);

    it("devrait rendre les enfants (le salop !)", () => {
        mockUsePathname.mockImplementation(() => '/foo/bar/1');

        const mockBasePath = '/foo/bar'
        const mockItems = [
            {
                id: 1,
                name: "foo"
            },
            {
                id: 2,
                name: "bar"
            },
        ]
        const { container } = render(<Tabs basePath={mockBasePath} items={mockItems} />);

        const wrapper = container.firstChild as HTMLElement;
        expect(wrapper.children).toHaveLength(2)
    });
})
