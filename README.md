# RAG-based Adaptive Learning System

Un système complet d'orientation IT adaptatif utilisant la technologie RAG (Retrieval-Augmented Generation) avec l'API Groq pour analyser les profils des étudiants et recommander des domaines IT appropriés. Inclut une API FastAPI backend et une interface React frontend moderne.

## 🚀 Fonctionnalités

- **Questionnaire interactif** : Évalue les compétences, intérêts et expériences des étudiants
- **Base de connaissances vectorielle** : Utilise ChromaDB pour stocker et rechercher des informations sur les domaines IT
- **Analyse LLM avancée** : Intègre l'API Groq (Llama 3.3) pour des recommandations personnalisées
- **API REST complète** : FastAPI avec endpoints documentés pour l'intégration
- **Interface React moderne** : Interface utilisateur responsive et intuitive
- **Recommandations détaillées** : Fournit des scores, niveaux de confiance et axes d'amélioration

## 📋 Prérequis

- Python 3.8+
- Node.js 16+ et npm
- Clé API Groq (obtenir sur https://console.groq.com/)

## 🛠️ Installation et Configuration

### 1. Cloner le repository
```bash
git clone https://github.com/Adaptative-Learning/RAG-based-Interface-Agent.git
cd RAG-based-Interface-Agent
git checkout Demo  # Pour la version complète avec interface React
```

### 2. Configuration du Backend (Python/FastAPI)

#### Créer un environnement virtuel
```bash
python -m venv .venv
.venv\Scripts\activate  # Sur Windows
# ou
source .venv/bin/activate  # Sur Linux/Mac
```

#### Installer les dépendances Python
```bash
pip install -r requirements.txt
```

#### Configurer la clé API
Créer un fichier `.env` dans le répertoire racine :
```
GROQ_API_KEY=votre_clé_api_ici
```

### 3. Configuration du Frontend (React)

#### Installer les dépendances Node.js
```bash
cd rag-interface
npm install
cd ..
```

## 🎯 Utilisation

### Option 1: Interface Web Complète (Recommandé)

#### Lancement du Backend API
```bash
# Depuis le répertoire racine
python api_runner.py
```
L'API sera disponible sur `http://localhost:8000`

#### Lancement du Frontend React
```bash
# Dans un nouveau terminal
cd rag-interface
npm start
```
L'interface sera disponible sur `http://localhost:3000`

### Option 2: Interface CLI (Originale)

#### Lancement du système CLI
```bash
python src/main.py
```

## 🌐 API REST Documentation

### Endpoints Disponibles

#### GET `/questions`
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

#### POST `/analyze`
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

#### GET `/health`
Vérification de l'état de l'API.

**Réponse :**
```json
{
  "status": "healthy",
  "service": "RAG IT Orientation API"
}
```

### Documentation Interactive
Accédez à la documentation complète de l'API sur `http://localhost:8000/docs` une fois le serveur lancé.

## 🖥️ Interface Web (React)

### Fonctionnalités de l'Interface

- **Questionnaire Progressif** : Navigation intuitive avec barre de progression
- **Affichage des Résultats** : Visualisation moderne des recommandations
- **Gestion d'Erreurs** : Messages d'erreur informatifs et récupération
- **États de Chargement** : Indicateurs visuels pendant l'analyse
- **Design Responsive** : Compatible mobile et desktop
- **Recommencement Facile** : Possibilité de refaire le questionnaire

### Composants Principaux

- **Questionnaire** : Interface de questions avec navigation
- **Results** : Affichage détaillé des recommandations
- **Loading** : État de chargement avec étapes
- **ErrorMessage** : Gestion des erreurs avec options de retry

## 📁 Structure du Projet

```
├── data/
│   └── domaines/              # Descriptions des domaines IT
│       ├── cloud.txt
│       ├── cybersecurite.txt
│       ├── data science.txt
│       ├── devops.txt
│       ├── reseaux.txt
│       └── software.txt
├── src/                       # Backend Python
│   ├── api.py                # API FastAPI
│   ├── main.py               # Interface CLI originale
│   ├── vector_store.py       # Gestion ChromaDB
│   ├── llm_analyzer.py       # Analyseur Groq
│   └── questionnaire.py       # Gestion questionnaire
├── rag-interface/            # Frontend React
│   ├── public/
│   ├── src/
│   │   ├── components/       # Composants React
│   │   │   ├── Questionnaire.js
│   │   │   ├── Results.js
│   │   │   ├── Loading.js
│   │   │   └── ErrorMessage.js
│   │   ├── services/
│   │   │   └── api.js       # Service API frontend
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
├── .env                      # Variables d'environnement
├── api_runner.py             # Script de lancement API
├── requirements.txt          # Dépendances Python
├── questionnaire.json         # Configuration questionnaire
└── README.md
```

## 🔧 Technologies Utilisées

### Backend
- **Python 3.8+** : Langage principal
- **FastAPI** : Framework API REST
- **ChromaDB** : Base de données vectorielle
- **Groq API** : Service LLM (Llama 3.3 70B)
- **python-dotenv** : Gestion des variables d'environnement

### Frontend
- **React 18** : Bibliothèque JavaScript
- **Axios** : Client HTTP pour API
- **CSS Modules** : Styles composants
- **Create React App** : Outil de build

## 🎨 Domaines IT Couvert

- **Cloud Computing** : Infrastructure et services cloud
- **Cybersécurité** : Protection et sécurité des systèmes
- **Data Science** : Analyse et traitement des données
- **DevOps** : Développement et opérations
- **Réseaux** : Architecture et administration réseau
- **Software Development** : Développement logiciel

## 🔍 Architecture et Fonctionnement

1. **Indexation** : Les descriptions des domaines IT sont vectorisées et stockées dans ChromaDB
2. **Questionnaire** : Collecte des informations sur le profil de l'étudiant (CLI ou Web)
3. **Recherche Sémantique** : Recherche des domaines les plus pertinents dans la base vectorielle
4. **Analyse LLM** : Génération de recommandations personnalisées avec justifications via Groq
5. **Rapport** : Présentation des résultats avec scores, confiance et conseils d'amélioration

## 🚨 Dépannage

### Erreur "ModuleNotFoundError" (Python)
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

### Problèmes avec l'interface React
```bash
cd rag-interface
npm install  # Réinstaller les dépendances
npm start    # Relancer le serveur de développement
```

### Port déjà utilisé
Si le port 3000 (React) ou 8000 (API) est déjà utilisé :
```bash
# Pour React (dans rag-interface/)
npm start -- --port 3001

# Pour l'API
python api_runner.py --port 8001
```

## 🧪 Tests

### Test de l'API
```bash
python test_api.py
```

### Test du Frontend
```bash
cd rag-interface
npm test
```

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
- FastAPI pour le framework API
- React pour la bibliothèque frontend
- La communauté open source Python et JavaScript

---

## 📞 Support

Pour toute question ou problème, ouvrez une issue sur GitHub ou contactez les contributeurs du projet.