QUESTIONNAIRES = [
    {
        "id": 1,
        "name": "Information utilisateur",
        "description": "Vos informations.",
        "order": 1,
    },
    {
        "id": 2,
        "name": "Préférences",
        "description": "Vos attentes professionnelles",
        "order": 2,
    },
]

ITEMS = [
    {
        "id": 1,
        "questionnaire_id": 1,
        "name": "Votre nom et prénom",
        "question": {"type": "text", "value": "Votre nom et prénom"},
        "content": {"type": "text"},
        "order": 1,
    },
    {
        "id": 2,
        "questionnaire_id": 1,
        "name": "Votre email",
        "question": {"type": "text", "value": "Votre email"},
        "content": {"type": "text"},
        "order": 2,
    },
    {
        "id": 3,
        "questionnaire_id": 2,
        "name": "Pouvoir amenez son chien",
        "question": {"type": "text", "value": "Pouvoir amenez son chien"},
        "content": {"type": "text"},
        "order": 1,
    },
    {
        "id": 4,
        "questionnaire_id": 2,
        "name": "Avoir un distributeur de patisserie artisanal",
        "question": {
            "type": "text",
            "value": "Avoir un distributeur de patisserie artisanal",
        },
        "content": {"type": "text"},
        "order": 2,
    },
]
