# Exemple de Mauvaise Réponse (À éviter)

## ❌ Séquence Incorrecte

[Données brutes] → [Entraînement] → [Validation] → [Entraînement] → [Déploiement] → [Monitoring] → [Preprocessing]

**Problèmes :** 
- Entraînement avant preprocessing
- Étapes manquantes
- Ordre illogique

## ❌ Choix d'Outils Non Justifiés

| Étape | Outil choisi | Justification |
|-------|-------------|---------------|
| Collecte/Ingestion | Excel | _________ |
| Preprocessing | _________ | _________ |
| Feature Engineering | TensorFlow | C'est populaire |
| Entraînement | _________ | _________ |
| Validation | _________ | _________ |
| Déploiement | _________ | _________ |
| Monitoring | _________ | _________ |

**Problèmes :**
- Outils inappropriés (Excel pour l'ingestion)
- Justifications vides ou simplistes
- Sections non complétées

## ❌ Cas d'Usage Vague

**Domaine :** _________________  
**Problème métier :** Faire de l'IA  
**Type de données :** Des données  
**Algorithme ML :** Un algorithme  

**Problèmes :**
- Manque de spécificité
- Pas de contexte métier
- Réponses génériques

## ❌ Réflexions Superficielles

### 1. Quel est le défi principal de ce pipeline ?
**Réponse :** C'est difficile

### 2. Comment gérer la dérive des données ?
**Réponse :** ________________

### 3. Quels sont les risques de biais ?
**Réponse :** Il y en a

**Problèmes :**
- Réponses trop courtes
- Pas de compréhension technique
- Sections vides