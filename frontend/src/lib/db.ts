import "server-only";

const items = [
    {
        id: 1,
        questionnaireId: 1,
        name: "Vous êtes actuellement...",
        value: {
            type: "choice",
            value: [
                "En période de transition",
                "En formation",
                "En recherche d'emploi",
                "En reconversion",
            ],
        },
    },
    {
        id: 2,
        questionnaireId: 1,
        name: "Ma dernière formation",
        value: {
            type: "choice",
            value: [
                "Niveau Bac ou équivalent",
                "Niveau Bac +2 / BTS / DUT",
                "Niveau Licence / Bac +3",
                "Niveau Master / Ingénieur / Bac +5",
                "Niveau Doctorat / Bac +8",
                "Certificat ou Titre Professionnel",
            ],
        },
    },
    {
        id: 3,
        questionnaireId: 1,
        name: "Ma dernière expérience professionnelle",
        value: {
            type: "choice",
            value: [
                "Moins de 6 mois",
                "Entre 6 mois et 1 an",
                "Entre 1 an et 3 ans",
                "Plus de 3 ans",
                "Je n'ai pas encore d'expérience professionnelle significative",
            ],
        },
    },
    {
        id: 4,
        questionnaireId: 2,
        name: "Votre objectif professionnel principal est de...",
        value: {
            type: "choice",
            value: [
                "Changer complètement de secteur d'activité",
                "Évoluer vers un poste à plus haute responsabilité",
                "Acquérir de nouvelles compétences ou certifications",
                "Trouver un meilleur équilibre entre vie professionnelle et personnelle",
            ],
        },
    },
    {
        id: 5,
        questionnaireId: 2,
        name: "La rémunération annuelle (brut) que vous visez se situe...",
        value: {
            type: "choice",
            value: [
                "Moins de 30 000 €",
                "Entre 30 000 € et 45 000 €",
                "Entre 45 000 € et 60 000 €",
                "Plus de 60 000 €",
            ],
        },
    },
    {
        id: 6,
        questionnaireId: 2,
        name: "Qu'est-ce qui vous motive le plus dans un nouveau rôle ?",
        value: {
            type: "choice",
            value: [
                "La culture d'entreprise et l'environnement de travail",
                "Les défis techniques et la complexité des projets",
                "Les opportunités de formation et de développement personnel",
                "L'impact social ou environnemental du travail",
            ],
        },
    },
];

const questionnaires = [
    {
        id: 1,
        name: "Bilan de Compétences et Statut Actuel",
        description:
            "Ce questionnaire initial permet de dresser un aperçu concis de votre situation professionnelle actuelle.",
    },
    {
        id: 2,
        name: "Objectifs et Motivation",
        description:
            "Déterminez et clarifiez vos aspirations futures. Ces questions portent sur votre niveau de rémunération souhaité.",
    },
];

const db = {
    getQuestionnaires: () => {
        return questionnaires;
    },
    getQuestionnaire: (qId: number) => {
        return questionnaires.find((q) => q.id == qId);
    },
    getItems: (qId: number) => {
        const res = items.filter((i) => i.questionnaireId == qId);
        return res;
    },
    getItem: (itemId: number) => {
        return items.find((i) => i.id == itemId);
    },
    getFirstItemId: (qId: number) => {
        const qItems = db.getItems(qId);
        return qItems[0];
    },
    getNextItemId: (itemId: number) => {
        const res = items.find((i) => i.id == itemId);
        if (!res) return;
        const qItems = db.getItems(res.questionnaireId);
        const iIdx = qItems.indexOf(res);
        if (iIdx + 1 < qItems.length) {
            return iIdx;
        }
    },
};

export default db;

// export default class db {
//     getQuestionnaires() {
//         return questionnaires
//     }
//     getQuestionnaire(qId: number) {
//         const questionnaire = questionnaires.filter(q => q.id == qId)
//         if (questionnaire.length == 0) {
//             return null
//         }
//         return questionnaire[0]
//     }
//     getItems(qId: number) {
//         const res = items.filter(i => i.questionnaireId == qId)
//         return res
//     }
//     getItem(itemId: number) {
//         const res = items.filter(i => i.id == itemId)
//         if (res.length == 0) {
//             return null
//         }
//         return res[0]
//     }
//     getFirstItemId(qId: number) {
//         const qItems = this.getItems(qId)
//         return qItems[0]
//     }
// }
