# Questionnaire Interaction App

## 🚀 Lancement rapide

### Prérequis
- [bun](https://bun.com/docs/installation)
- **backend** qui tourne

### Installation & Setup

1. **Installe les dépendances**
```bash
bun install
```
2. **Lance en mode development**
```bash
bun run dev
```

Ouvre ton navigateur avec http://localhost:3000

## 📁 Structure
```
frontend/
└── src/
    ├── app/
    │   ├── api/ # API Routes
    │   └── page.tsx # Main page
    ├── lib/
    │   └── utils.ts  # Tools
    ├── components/  # Composants @shadcn
    ├── adapters/ 
    │   ├── api/  # External adapters
    │   └── public/ # Internal adapters
    ├── container/
    │   └── Containers/ # Connecter (usecases -> adapter)
    ├── core/ # Entities, interfaces and usecases
    └── ui/
        ├── components/  # React Components
        └── contexts/  # React Contexts
```

## 🛣️ Routes

```
app/
└── [apiKey]/
    ├── layout.tsx  # Récupérer et vérifie la clé API
    └── questionnaires/
        ├── page.tsx
        ├── layout.tsx # QuestionnaireProvider
        └── [qID]/
            ├── layout.tsx  # SessionProvider
            ├── items/ # Affichage des questions
            │   ├── layout.tsx
            │   ├── @sidebar/
            │   │   └── page.tsx
            │   └── @item/
            │       └── page.tsx
            └── results/
                └── page.tsx # Affichage des résultats
```

 