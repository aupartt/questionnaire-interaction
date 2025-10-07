import { ISessionRepository } from '@/core/ports/ISessionRepository';
import { Session } from '@/core/entities/Session';

export class MockSessionRepository implements ISessionRepository {
    private session: Session = new Session(
        "1",
        "2",
        [{ id: "1", name: "foo" }],
        [],
        {
            id: "1",
            name: "foo",
            question: {
                type: "text",
                value: "Yahoo",
            },
            content: {
                type: "text",
                likertValue: null
            }
        }
    )

    async get(): Promise<Session> {
        return Promise.resolve(this.session)
    }
}