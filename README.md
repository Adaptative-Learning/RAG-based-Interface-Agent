# RAG-based Interface Agent 🤖

**Système Intelligent de Prédiction de Domaines IT** basé sur une architecture RAG (Retrieval-Augmented Generation)

Un outil interactif qui aide les utilisateurs à identifier les domaines IT qui correspondent le mieux à leur profil et leurs préférences par le biais d'un questionnaire intelligent.

---

## 📋 Vue d'ensemble

Ce projet combine :
- **Questionnaire adaptatif** : Pose des questions ciblées sur les préférences IT
- **Vector Store (ChromaDB)** : Stocke les domaines IT et recherche les correspondances
- **LLM Ollama** : Analyse les réponses avec un modèle de langage local
- **RAG** : Récupère les domaines pertinents et génère des recommandations personnalisées

### Domaines IT couverts
- ☁️ Cloud et Automatisation
- 🔒 Cybersécurité
- 📊 Data Science et IA
- 🚀 DevOps
- 🌐 Réseaux informatiques
- 💻 Développement logiciel

---

## 🚀 Installation

### 1. Prérequis
- **Python 3.8+**
- **Ollama** (pour le LLM local) → [Télécharger ici](https://ollama.ai)
- **pip** (gestionnaire de paquets Python)

### 2. Cloner le projet

```bash
git clone https://github.com/Adaptative-Learning/RAG-based-Interface-Agent.git
cd RAG-based-Interface-Agent
git checkout ollama  # Switch to ollama branch
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

**Dépendances principales :**
- `chromadb` : Base de données vectorielle pour la recherche sémantique
- `requests` : Pour communiquer avec Ollama

### 4. Configurer Ollama

**Installation d'Ollama :**
1. Téléchargez Ollama depuis [ollama.ai](https://ollama.ai)
2. Installez-le sur votre machine
3. Lancez le service Ollama
4. Téléchargez un modèle léger :

```bash
ollama pull llama3.2:1b
```

> **Note** : Le modèle `llama3.2:1b` est très léger et rapide. Vous pouvez essayer d'autres modèles comme `mistral`, `neural-chat`, etc.

---

## 📖 Utilisation

### Lancer l'application

```bash
python src/main.py
```

### Flux d'exécution

1. **Chargement de la base de connaissances** 🔄
   - Les domaines IT sont chargés depuis `data/domaines/`
   - Une base vectorielle est créée pour la recherche sémantique

2. **Questionnaire interactif** ❓
   - Répondez aux 10+ questions sur vos préférences IT
   - Pour chaque question, choisissez l'option (1, 2, 3, etc.) qui vous correspond

3. **Analyse avec LLM** 🧠
   - Ollama analyse vos réponses
   - Recherche les domaines pertinents dans la base vectorielle
   - Génère une recommandation personnalisée

4. **Résultats** 📊
   - Affichage du domaine recommandé
   - Explication détaillée basée sur vos réponses

### Exemple d'interaction

```
======================================================================
SYSTEME DE PREDICTION DE DOMAINES IT
======================================================================

[INFO] Chargement de la base de connaissances...
[OK] 6 domaines charges avec succes

[QUESTIONNAIRE] DEBUT DU QUESTIONNAIRE

Question 1: Comment préférez-vous résoudre un problème complexe dans un projet ?
1. Analyser les données disponibles pour trouver la solution
2. Coder une solution testable et itérative
3. Tester différentes hypothèses rapidement pour identifier le problème
4. Collaborer avec l'équipe pour brainstormer
5. Appliquer des méthodologies standardisées (agile, design thinking)

Choisis une option (numéro) : 2

...
```

---

## 📁 Structure du projet

```
RAG-based-Interface-Agent/
├── src/
│   ├── main.py                 # Point d'entrée principal
│   ├── questionnaire.py        # Gestion du questionnaire
│   ├── vector_store.py         # Intégration ChromaDB
│   └── llm_analyzer.py         # Intégration Ollama LLM
├── data/
│   └── domaines/               # Fichiers texte des domaines IT
│       ├── cloud.txt
│       ├── cybersecurite.txt
│       ├── data science.txt
│       ├── devops.txt
│       ├── reseaux.txt
│       └── software.txt
├── questionnaire.json          # Définition des questions
├── requirements.txt            # Dépendances Python
└── README.md                   # Ce fichier
```

---

## 🔑 Fichiers clés

### `questionnaire.json`
Définit les 10+ questions posées aux utilisateurs avec les domaines liés :
```json
{
  "questions": [
    {
      "id": 1,
      "question": "Comment préférez-vous résoudre un problème complexe ?",
      "options": ["Option 1", "Option 2", ...],
      "linked_domains": ["Développement logiciel", "Data et IA"]
    }
  ]
}
```

### `data/domaines/`
Contient les descriptions textuelles de chaque domaine IT :
- **cloud.txt** : Cloud, containerisation, infrastructure
- **cybersecurite.txt** : Sécurité, chiffrement, audit
- **data science.txt** : ML, IA, analytics
- **devops.txt** : CI/CD, monitoring, automatisation
- **reseaux.txt** : Réseaux, TCP/IP, routing
- **software.txt** : Programmation, frameworks, design

### `src/main.py`
Orchestre tout le flux :
1. Charge les domaines dans ChromaDB
2. Lance le questionnaire
3. Analyse avec Ollama
4. Affiche les recommandations

---

## 🛠️ Personnalisation

### Ajouter une nouvelle question

Modifiez `questionnaire.json` :
```json
{
  "id": 11,
  "question": "Votre nouvelle question ?",
  "type": "multiple_choice",
  "options": [
    "Option 1",
    "Option 2",
    "Option 3"
  ],
  "linked_domains": ["Domaine 1", "Domaine 2"]
}
```

### Ajouter un nouveau domaine

1. Créez un fichier texte dans `data/domaines/` (ex: `machine_learning.txt`)
2. Décrivez le domaine avec des détails pertinents
3. Le domaine sera automatiquement chargé au prochain lancement

### Changer le modèle LLM

Dans `src/main.py`, modifiez :
```python
analyzer = LLMAnalyzer(model="mistral")  # ou un autre modèle Ollama
```

Modèles recommandés :
- `llama3.2:1b` (très rapide, léger)
- `mistral` (équilibré)
- `llama3.2:7b` (plus puissant, demande plus de RAM)

---

## ⚙️ Dépannage

### Erreur : "Connection refused" (Ollama)
**Solution :**
```bash
# Vérifiez qu'Ollama est en cours d'exécution
ollama serve
# Dans un autre terminal
ollama pull llama3.2:1b
```

### Erreur : "Module not found"
**Solution :**
```bash
pip install -r requirements.txt
```

### Performances lentes
- Utilisez un modèle plus léger : `ollama pull llama3.2:1b`
- Augmentez la RAM disponible
- Vérifiez votre CPU

### ChromaDB ne charge pas les domaines
**Solution :**
```bash
# Vérifiez que les fichiers existent
ls data/domaines/
# Assurez-vous que les fichiers ne sont pas vides
```

---

## 🔄 Architecture

```
User Input (Questionnaire)
        ↓
    Responses
        ↓
Vector Store (ChromaDB) ← Similarity Search
        ↓
LLM Analyzer (Ollama) ← Contextual Analysis
        ↓
Recommendations Output
```

### Flux RAG :
1. **Retrieval** : Recherche les domaines similaires aux réponses
2. **Augmentation** : Enrichit le contexte avec le contenu des domaines
3. **Generation** : Génère une réponse personnalisée avec Ollama

---

## 📊 Branche `ollama`

Vous êtes sur la branche `ollama` qui contient :
- ✅ Intégration complète d'Ollama
- ✅ Modèles légers optimisés
- ✅ Architecture RAG fonctionnelle
- ✅ Questionnaire adaptatif

---

## 🤝 Contribution

Pour contribuer :
1. Créez une branche (`git checkout -b feature/ma-feature`)
2. Committez vos changements (`git commit -m "Add: ma feature"`)
3. Poussez la branche (`git push origin feature/ma-feature`)
4. Créez une Pull Request

---

## 📝 Licence

Ce projet est fourni à titre éducatif.

---

## 📞 Support

Pour toute question ou problème :
- Vérifiez le section **Dépannage**
- Consultez les logs d'exécution
- Vérifiez que toutes les dépendances sont installées

---

## 🎯 Améliorations futures

- [ ] Interface web avec Streamlit
- [ ] Stockage des résultats en base de données
- [ ] Modèles multi-langues
- [ ] Historique des questionnaires
- [ ] Analyse comparative des domaines

---

**Dernière mise à jour** : Décembre 2025  
**Branche active** : `ollama`
