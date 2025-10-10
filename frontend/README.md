# Questionnaire Interaction App

> L'application ne fonctionne actuellement pas en version Docker, dû à un manque de connaissance de Next.js de ma part. Une refactorisation est en cours, incluant les bonne pratiques de routing (layout, page, ...). Pour plus de détails c'est [ici](./docs/front_refactorisation.md).

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
 