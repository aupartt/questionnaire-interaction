# API Backend pour l'application Questionnaire

## Structure

### /adapter
Les adapter sont des class utilisés par les services et se bases sur des `/services/protocol`

- **InMemoryAdapter[DataAdapterProtocol]:** Permet d'utiliser l'application avec des données en mémoire (pratique pour les tests ou prototypage)
- **PostgresAdapter[DataAdapterProtocol]:** A venir, intégre postgres à l'application 


### /services
Logique métier, utilisé par les `/controller` et dépendes des `/adapter`

**protocol:**
- **DataAdapterProtocol:** Logique de récupération et modification des données de questionnaires (Questionnaire / Item / Session ...)

### /controller
La base de l'API, c'est ici que les chemin d'API sont fait et les dépendences créés.

### /middleware
Tout ce qui est middleware personnalisé pour l'API

- **APIKeyMiddleware:** Vérifie que la requête contient bien une clé d'API valide et la passe en tant que state (plus simple)

### /models
Modèle pydantic pour la validation des données
- **schemas:** Tout ce qui est data
- **common:** Tout ce qui est Enum, Type


## Endpoints:

GET `/questionnaires` HEADER `X-API-KEY`

**Descrition:**
Permet de récupérer la liste de questionnaires avec le status
> Savoir si le questionnaire à déjà été fait, passé et de facilement voir quel est le prochain à passer

La liste de questionnaire sera récupéré et stocker en front.
A chaque fin de questionnaire ce endpoint sera appelé pour mettre à jours les status

**Retourne:**
```json
{
[
    {
        "id": "string",
        "name": "string",
        "description": "string",
        "status": "string", // null, ACTIVE / SKIPPED / COMPLETED
        "session_id": "string", // ID de la session existante ou null
        "is_next": "boolean"
    }
]
```
---

POST `/questionnaire/{id}/session` HEADER `X-API-KEY`

**Description:**
Initialise un questionnaire ou retourne une session existante

Du point de vu du front, une fois la liste de questionnaire récupéré, il n'y a plus qu'à récupérer le questionnaire `is_next == true`


**Retourne:**
```json
{
    "id": "string", // id de session
    "questionnaire_id": "string",
    "items": [ // Tous les items du questionnaires (sans le content)
        {
            "id": "string",
            "name": "string",
            "status": "string" // ACTIVE / COMPLETED / SKIPPED
        }
    ],
    "answers": [ // Toutes les réponses 
        {
            "id": "string",
            "item_id": "string",
            "value": "string / dict"
        }
    ],
    "current_item": {
        "id": "string",
        "name": "string",
        "question": "ItemQuestion",
        "content": "ItemContent"
    }
}
```

---

POST `/questionnaire/{id}/session/{id}/answer` HEADER `X-API-KEY`

**Description:**
Envois la réponse d'un item et recois le content du prochain item s'il existe

**Retourne:**
```json
// S'il y a un item suivant
{
    "next_item": {
        "id": "string",
        "name": "string",
        "question": "ItemQuestion",
        "content": "ItemContent"
    },
    "session_status": "active"
}

// Si le questionnaire est fini
{
    "result_url": "string", // Url pour récupérer les résultats de la session
    "session_status": "completed"
}
```

---

POST `/questionnaire/{id}/session/{id}/result` HEADER `X-API-KEY`

**Description:**
Retourne le résultat d'une session terminé

**Retourne:**
*Will Smith*