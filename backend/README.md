# Questionnaire Interaction API


## 🚀 Lancement rapide

### Prérequis
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### Installation & Setup

1. **Installe les dépendances**
```bash
uv sync
```

2. **Lance en mode development**
```bash
uv run -m main
```

2. **Lancer les tests**
```bash
uv run pytest
```

Ouvre ton navigateur avec http://localhost:3000


## 📁 Structure

### /adapter
Les adapter sont des class utilisés par les services et se bases sur des `/services/protocol`

### /services
Logique métier, utilisé par les `/controller` et dépendes des `/adapter`

### /controller
La base de l'API, c'est ici que les chemin d'API sont fait et les dépendences créés.

### /middleware
Tout ce qui est middleware personnalisé pour l'API

- **APIKeyMiddleware:** Vérifie que la requête contient bien une clé d'API valide et la passe en tant que state (plus simple)

### /models
Modèle ORM sqlalchemy 

### /schema
Modèle pydantic pour la validation des données
- **common:** Tout ce qui est Enum, Type


## 🎯 Endpoints:

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
        "id": "number",
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
    "id": "number", // id de session
    "questionnaire_id": "number",
    "items": [ // Tous les items du questionnaires (sans le content)
        {
            "id": "number",
            "name": "string",
            "status": "string" // ACTIVE / COMPLETED / SKIPPED
        }
    ],
    "answers": [ // Toutes les réponses 
        {
            "id": "number",
            "item_id": "number",
            "value": "string / dict"
        }
    ],
    "current_item": {
        "id": "number",
        "name": "string",
        "question": "ItemQuestion",
        "content": "ItemContent"
    }
}
```

---

POST `/questionnaire/{id}/session/{id}/answer` HEADER `X-API-KEY`

**Description:**
Envois la réponse d'un item et reçois le content du prochain item s'il existe

**Retourne:**
```json
// S'il y a un item suivant
{
    "next_item": {
        "id": "number",
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
