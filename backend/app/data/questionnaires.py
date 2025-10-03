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
    {"id": 1, "type": "text", "question": "Nom Prénom", "order": 1},
    {"id": 2, "type": "text", "question": "Address mail", "order": 2},
    {
        "id": 3,
        "type": "text",
        "question": "Pouvoir amenez son chien",
        "order": 1,
    },
    {
        "id": 4,
        "type": "text",
        "question": "Avoir un distributeur de patisserie artisanal",
        "order": 2,
    },
]

# Permet de liée les sessions entre elles
USERS = []  # [{ id: .., status: "in_progress/ended" }]
SESSIONS = []  # [{ id: .., user_id: .., questionnaire_id: .., status: "in_progress/ended"}]
RESPONSES = []  # [ { id: 1, session_id: .., item_id: .., value: .. } ]
