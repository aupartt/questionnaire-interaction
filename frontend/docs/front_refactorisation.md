# Refactorisation de l'application Front


## 🛣️ Routes

```
app/
└── [apiKey]/
    ├── providers.tsx # Context provider (Session)
    ├── layout.tsx  # Récupérer et vérifie la clé API + providers
    └── questionnaires/
        ├── page.tsx
        └── [qID]/
            ├── layout.tsx  # Switch sur le status de la session (next ou result)
            ├── @sidebar/
            │   └── page.tsx
            ├── @item/
            │   └── page.tsx
            └── @results/
                └── page.tsx
```


## 📄 Pages

### `/[apiKey]/questionnaires`
Page principale d'onboarding (liste questionnaires)

### `/[apiKey]/questionnaires/[qId]/item?id={itemId}`
Page qui affiche la question posé à l'utilisateur

### `/[apiKey]/questionnaires/[qId]/results`
Affiche des résultats d'un questionnaire

