# Questionnaire Interaction API


## 🔎 Voir aussi:
- [Informations sur les endpoints](./docs/description_endpoints.md)
- [Base de donnée](./docs/database.md)

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


## 📁 Structure

```
backend/
├── alembic/
│   ├── env.py
│   ├── versions/
│   │   └── 97956a213ec7_seed_data.py  # Révision de seed
│   └── seed_data/  
│       ├── items.json  # Fichier JSON pour le seeding de postgres
│       └── questionnaires.json
└── app/
    ├── adapter/
    │   └── repository.py  # Couche database
    ├── service/
    │   └── service.py  # Couche métier
    ├── controller/
    │   ├── dependencies/
    │   │   └── security.py  # Middleware
    │   └── controller.py
    ├── core/
    │   ├── config.py
    │   └── database.py  # Connection db
    ├── models/
    │   └── items.py  # Modèles ORM sqlalchemy
    ├── schema/
    │   └── items.py  # Modèles de validation pydantic
    └── test/
        ├── conftest.py
        └── .../
```


## 🐦‍⬛ Migration

Utilisation d'alembic pour gérer la base de donnée.
Pour initialiser la base avec les tables et la data lancez
```
uv run alembic upgrade head
```

Pour réinitialiser la base (si vous avez modifier les données de seed)
```
# Undo la dernière révision
uv run alembic downgrade -1

# Redo l'initialisation
uv run alembic upgrade head
```

### 🌱 Seeding
Vous trouverez les fichiers avec les données initiales dans `/backend/alembic/seed_data`
Un utilisateur est automatiquement créé avec comme **api_key**: `API_KEY_MOCK`