# Analyse Automatisée des Dépenses avec CrewAI

Ce projet utilise CrewAI pour analyser automatiquement les dépenses à partir des factures, générer des rapports détaillés et négocier avec les fournisseurs.

## 🚀 Installation

1. Clonez le dépôt
2. Créez un environnement virtuel Python :
```bash
python -m venv venv
source venv/bin/activate  # Sur Unix/MacOS
.\venv\Scripts\activate   # Sur Windows
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurez les variables d'environnement dans un fichier `.env` :
```env
OPENAI_API_KEY="votre-clé-openai"
NEEDLE_API_KEY="votre-clé-needle"
NEEDLE_COLLECTION_ID="votre-id-collection"
SERPER_API_KEY="votre-clé-serper"  # Pour la recherche de fournisseurs
```

## 📊 Utilisation

### Interface en Ligne de Commande
Pour lancer l'analyse des dépenses via la ligne de commande :

```bash
python src/main.py
```

### Interface Web
Pour lancer l'interface web :

```bash
streamlit run src/app.py
```

L'interface web propose :
- Un tableau de bord intuitif
- Trois sections principales : Analyse, Rapports et Audit
- Configuration facile des clés API
- Génération et visualisation des rapports en temps réel
- Fonctionnalité d'export des rapports

## 🤖 Agents AI

Le système utilise quatre agents AI spécialisés :
1. **Analyste des Dépenses** : Analyse les factures et identifie les tendances 
2. **Rédacteur Financier** : Transforme l'analyse en rapport structuré 
3. **Auditeur de Conformité** : Vérifie les erreurs, la fraude et la conformité 
4. **Négociateur Fournisseurs** : Recherche et négocie avec des fournisseurs alternatifs pour obtenir des réductions

## 📝 Rapports Générés

Le système produit quatre rapports distincts :
1. `expense_report.md` : Analyse détaillée des dépenses 
2. `final_expense_report.md` : Rapport financier stratégique 
3. `compliance_audit.md` : Rapport d'audit de conformité 
4. `negotiated_suppliers.md` : Analyse des fournisseurs alternatifs et négociations 

## 📂 Structure du Projet

```
.
├── src/
│   ├── main.py           # Interface en ligne de commande
│   ├── app.py            # Interface web Streamlit
│   └── tools/            # Outils personnalisés
│       └── custom_tool.py
├── requirements.txt      # Dépendances Python
└── .env                 # Variables d'environnement
```

## 🔑 Prérequis

- Python 3.8+
- Clé API OpenAI
- Clé API Needle
- ID de Collection Needle
- Clé API Serper (pour la recherche de fournisseurs)

## 📈 Fonctionnalités

- Analyse détaillée des dépenses par fournisseur
- Détection des anomalies et des fraudes potentielles
- Recommandations d'optimisation des coûts
- Recherche automatisée de fournisseurs alternatifs et négociation des prix
- Interface utilisateur moderne et intuitive
- Génération de rapports en format Markdown 