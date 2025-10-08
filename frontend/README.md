# Fronted pour l'application Questionnaire

## Routes

Afin de faciliter l'utilisation de la clé API, celle-ci sera directement l'intégrer au routes: `/{api_key}/path`.
> http://example.com/foo123/onboarding

---

`/{api_key}/onboarding`

**Description:**
Affichage des questionnaires avec mise en avant du prochain à réaliser (bouton pour le commencer).

**Composants:**
- Bouton (continuer / commencer)
- Alert (pour les erreurs)

---