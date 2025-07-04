# 📘 MODULE 4 – Données, IA & transformation digitale
## Exercice d'évaluation automatisé

---

## 🎯 Vue d'ensemble

**Cours :** MODULE 4 – Données, IA & transformation digitale  
**Date :** 19 janvier 2026  
**Enseignant :** Antoine Coppin  
**Format :** QCM + Code completion (20 questions, 20 points)  
**Durée :** 20 minutes  
**Seuil de validation :** 14/20  

---

## 📋 Instructions pour les étudiants

### 1. **Fork** ce repository
- Cliquez sur **"Fork"** en haut à droite
- Sélectionnez votre compte personnel

### 2. **Complétez** l'exercice
- Modifiez le fichier `pipeline-exercise.json`
- Remplacez **tous** les `________________` par vos réponses
- **QCM** : Répondez A, B, C ou D
- **Code** : Écrivez la syntaxe exacte

### 3. **Soumettez** avant 9h30
- **Commit** vos modifications
- Créez une **Pull Request**
- Le système corrige automatiquement en 1-2 minutes

### 4. **Consultez** vos résultats
- Score et feedback dans les commentaires de votre PR
- Les solutions seront révélées en classe après l'exercice

---

## 🏆 Barème

| Score | Note | Signification |
|-------|------|---------------|
| 18-20 | A | 🏆 Excellent ! Maîtrise exceptionnelle |
| 16-17 | B+ | 🥇 Très bon niveau technique |
| 14-15 | B | 👍 Bien ! Module validé |
| 12-13 | C+ | ⚠️ Passable, quelques lacunes |
| 10-11 | C | 📚 Insuffisant, révision nécessaire |
| 0-9 | D | ❌ À reprendre |

**Seuil de validation :** 14/20

---

## 📚 Ressources

### Avant l'exercice
- **Documentation officielle** : MLflow, pandas, scikit-learn, Docker
- **TP précédents** : Pipeline ML, feature engineering

### Aide GitHub (débutants)
- **Fork** : Bouton en haut à droite → Sélectionner votre compte
- **Éditer** : Cliquer sur `pipeline-exercise.json` → Icône crayon ✏️
- **Commit** : "Commit changes" en bas de page
- **Pull Request** : Bouton vert "Compare & pull request"

---

### Structure du repository
```
pipeline-exercise/
├── README.md                           # Ce fichier
├── pipeline-exercise.json             # Template étudiant
├── .github/workflows/                 
│   └── grade-submission.yml           # Workflow CI/CD
├── system/
│   └── runner.py  # Runner sécurisé
└── .gitignore
```

---

## ⚙️ Configuration GitHub Actions

### Workflow automatique
- **Déclencheur** : Pull Request sur `pipeline-exercise.json`
- **Action** : Correction automatique
- **Résultat** : Commentaire avec score et feedback
- **Durée** : 1-2 minutes

### Permissions requises
```yaml
permissions:
  contents: read
  pull-requests: write
  issues: write
```
