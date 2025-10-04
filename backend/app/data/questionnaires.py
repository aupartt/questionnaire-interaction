QUESTIONNAIRES = [
    {
        "id": "1",
        "name": "Information utilisateur",
        "description": "Vos informations.",
        "order": 1,
    },
    {
        "id": "2",
        "name": "Préférences",
        "description": "Vos attentes professionnelles",
        "order": 2,
    },
]

ITEMS = [
    {
        "id": "1",
        "questionnaire_id": "1",
        "question_type": "text",
        "question": "Nom Prénom",
        "item_content": {"type": "text"},
        "order": 1,
    },
    {
        "id": "2",
        "questionnaire_id": "1",
        "question_type": "text",
        "question": "Address mail",
        "item_content": {"type": "text"},
        "order": 2,
    },
    {
        "id": "3",
        "questionnaire_id": "2",
        "question_type": "text",
        "question": "Pouvoir amenez son chien",
        "item_content": {"type": "text"},
        "order": 1,
    },
    {
        "id": "4",
        "questionnaire_id": "2",
        "question_type": "text",
        "question": "Avoir un distributeur de patisserie artisanal",
        "item_content": {"type": "text"},
        "order": 2,
    },
]
