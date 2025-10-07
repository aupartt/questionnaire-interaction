export class ApiError extends Error {
    constructor(message: string) {
        super(message)
        this.name = this.constructor.name
    }
}

export class ApiNotReachableError extends ApiError {
    constructor() {
        super(`API non disponible, vérifier l'url ou votre connexion.`)
    }
}