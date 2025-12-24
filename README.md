# RAG-based Adaptive Learning System

Un système d'orientation IT adaptatif utilisant la technologie RAG (Retrieval-Augmented Generation) avec l'API Groq pour analyser les profils des étudiants et recommander des domaines IT appropriés.

## 🚀 Fonctionnalités

- **Questionnaire interactif** : Évalue les compétences, intérêts et expériences des étudiants
- **Base de connaissances vectorielle** : Utilise ChromaDB pour stocker et rechercher des informations sur les domaines IT
- **Analyse LLM avancée** : Intègre l'API Groq (Llama 3.3) pour des recommandations personnalisées
- **Recommandations détaillées** : Fournit des scores, niveaux de confiance et axes d'amélioration

## 📋 Prérequis

- Python 3.8+
- Clé API Groq (obtenir sur https://console.groq.com/)

## 🛠️ Installation

1. **Cloner le repository**
   ```bash
   git clone https://github.com/Adaptative-Learning/RAG-based-Interface-Agent.git
   cd RAG-based-Interface-Agent
   git checkout Groq
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Sur Windows
   # ou
   source .venv/bin/activate  # Sur Linux/Mac
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer la clé API**
   - Créer un fichier `.env` dans le répertoire racine
   - Ajouter votre clé API Groq :
   ```
   GROQ_API_KEY=votre_clé_api_ici
   ```

## 🎯 Utilisation

### Lancement du système
```bash
python src/main.py
```

### API REST

Le système inclut également une API FastAPI pour une intégration facile.

#### Lancement de l'API
```bash
python api_runner.py
```

#### Endpoints disponibles

##### GET `/questions`
Retourne toutes les questions du questionnaire avec leurs options.

**Exemple de réponse :**
```json
{
  "title": "Questionnaire de Profil IT pour Adaptive Learning",
  "description": "Évaluez vos préférences et compétences...",
  "questions": [
    {
      "id": 1,
      "question": "Comment préférez-vous résoudre un problème complexe...",
      "type": "multiple_choice",
      "options": ["Option 1", "Option 2", ...],
      "linked_domains": ["Domaine1", "Domaine2"]
    }
  ]
}
```

##### POST `/analyze`
Analyse les réponses du questionnaire et retourne les recommandations.

**Corps de la requête :**
```json
{
  "answers": [
    {
      "question_id": 1,
      "answer": "Coder une solution testable et itérative"
    },
    {
      "question_id": 2,
      "answer": "Optimiser les paramètres et la performance du système"
    }
  ]
}
```

**Exemple de réponse :**
```json
{
  "predictions": [
    {
      "domaine": "data science",
      "score": 85,
      "raisons": ["Intérêt marqué pour l'analyse de données", "Compétences techniques alignées"],
      "confiance": "haute",
      "points_forts": ["Analyse de données", "Python"],
      "axes_amelioration": ["Machine Learning avancé"]
    }
  ],
  "resume_global": "Profil orienté vers l'analyse de données...",
  "top_3_recommandations": ["data science", "devops", "software"]
}
```

##### GET `/health`
Vérification de l'état de l'API.

**Réponse :**
```json
{
  "status": "healthy",
  "service": "RAG IT Orientation API"
}
```

#### Documentation interactive
Accédez à la documentation complète de l'API sur `http://localhost:8000/docs` une fois le serveur lancé.

### Processus d'utilisation (Interface CLI)

1. **Chargement de la base de connaissances**
   - Le système charge automatiquement les descriptions des domaines IT depuis `data/domaines/`

2. **Questionnaire interactif**
   - Répondez aux 10 questions sur vos compétences, expériences et intérêts
   - Chaque question propose plusieurs choix numérotés

3. **Analyse et recommandations**
   - Le système analyse vos réponses en utilisant l'IA
   - Fournit des recommandations personnalisées avec scores et justifications

### Exemple de sortie
```
Système de prédiction de domaines IT

Chargement de la base de connaissances...
   ✓ cloud
   ✓ cybersecurite
   ✓ data science
   ✓ devops
   ✓ reseaux
   ✓ software

Début du questionnaire
Question 1: Comment préférez-vous résoudre un problème complexe...
[Questions interactives]

Analyse en cours...
RÉSULTATS

data science : 85%
   Confiance : haute
   Raisons :
   ✓ Intérêt marqué pour l'analyse de données
   ✓ Compétences techniques alignées
   ✓ Motivation pour les projets data
```

## 📁 Structure du projet

```
├── data/
│   └── domaines/          # Descriptions des domaines IT
│       ├── cloud.txt
│       ├── cybersecurite.txt
│       ├── data science.txt
│       ├── devops.txt
│       ├── reseaux.txt
│       └── software.txt
├── src/
│   ├── main.py           # Point d'entrée principal
│   ├── vector_store.py   # Gestion de la base vectorielle ChromaDB
│   ├── llm_analyzer.py   # Analyseur LLM avec API Groq
│   └── questionnaire.py   # Gestionnaire du questionnaire
├── .env                  # Variables d'environnement (non versionné)
├── .gitignore           # Fichiers à ignorer
├── requirements.txt     # Dépendances Python
└── questionnaire.json    # Configuration du questionnaire
```

## 🔧 Technologies utilisées

- **Python 3.8+** : Langage principal
- **ChromaDB** : Base de données vectorielle pour le RAG
- **Groq API** : Service LLM (Llama 3.3 70B)
- **python-dotenv** : Gestion des variables d'environnement

## 🎨 Domaines IT couverts

- **Cloud Computing** : Infrastructure et services cloud
- **Cybersécurité** : Protection et sécurité des systèmes
- **Data Science** : Analyse et traitement des données
- **DevOps** : Développement et opérations
- **Réseaux** : Architecture et administration réseau
- **Software Development** : Développement logiciel

## 🔍 Comment ça marche

1. **Indexation** : Les descriptions des domaines IT sont vectorisées et stockées dans ChromaDB
2. **Questionnaire** : Collecte des informations sur le profil de l'étudiant
3. **Recherche sémantique** : Recherche des domaines les plus pertinents
4. **Analyse LLM** : Génération de recommandations personnalisées avec justifications
5. **Rapport** : Présentation des résultats avec scores et conseils

## 🚨 Dépannage

### Erreur "ModuleNotFoundError"
Assurez-vous d'avoir activé l'environnement virtuel et installé les dépendances :
```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

### Erreur API Groq
Vérifiez que votre clé API est correctement configurée dans `.env` :
```
GROQ_API_KEY=votre_clé_api_ici
```

### Erreur de chargement des domaines
Vérifiez que le dossier `data/domaines/` existe et contient les fichiers `.txt`.

## 🤝 Contribution

1. Fork le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.

## 👥 Auteurs

- **Soufiane** - *Développement initial* - [Soufiane-2005](https://github.com/Soufiane-2005)

## 🙏 Remerciements

- Groq pour l'API LLM
- ChromaDB pour la base de données vectorielle
- La communauté Python pour les bibliothèques open source