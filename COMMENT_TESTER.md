# 🚀 Comment Tester le Projet MASI Dashboard

## ⚡ Démarrage Ultra-Rapide (3 commandes)

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Lancer le dashboard
streamlit run Main.py

# 3. Ouvrir dans le navigateur
# → http://localhost:8501
```

---

## 📝 Méthodes de Test

### **Méthode 1 : Script Interactif (Recommandé)**

```bash
./quick_start.sh
```

Ce script va :
- ✅ Vérifier votre environnement Python
- ✅ Créer/activer l'environnement virtuel si besoin
- ✅ Installer les dépendances manquantes
- ✅ Tester la structure du projet
- ✅ Vous proposer différents modes de lancement

---

### **Méthode 2 : Test Automatique Complet**

```bash
./test_project.sh
```

Résultat attendu :
```
✓✓✓ TOUS LES TESTS SONT PASSÉS ✓✓✓
Tests réussis: 19
Tests échoués: 0
```

---

### **Méthode 3 : Test Manuel Étape par Étape**

#### Étape 1 : Environnement Virtuel

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

#### Étape 2 : Installation

```bash
pip install -r requirements.txt
```

#### Étape 3 : Tests Rapides

```bash
# Test des imports
python3 -c "from sentiment_calculator import MASISentimentCalculator; print('✓ OK')"

# Test de génération de données
python3 -c "
from data_handler import DataHandler
from datetime import date
handler = DataHandler()
data = handler.get_historical_data(date.today())
print(f'✓ MASI Close: {data[\"close\"]:.2f}')
"

# Test de calcul de sentiment
python3 -c "
from data_handler import DataHandler
from sentiment_calculator import MASISentimentCalculator
from datetime import date

handler = DataHandler()
calculator = MASISentimentCalculator()

data = handler.get_historical_data(date.today())
result = calculator.calculate_sentiment(data, date.today())

print(f'✓ Sentiment: {result[\"overall_score\"]:.1f} ({result[\"sentiment_label\"]})')
"
```

#### Étape 4 : Lancer le Dashboard

```bash
streamlit run Main.py
```

---

## 🧪 Tests Spécifiques

### Test 1 : Cache System

```python
from utils.cache import cache_data, get_cached_data

cache_data("test", {"value": 123}, ttl=60)
result = get_cached_data("test")
print(f"Cache: {result}")  # {'value': 123}
```

### Test 2 : Formatters

```python
from utils.formatters import format_number, format_percentage

print(format_number(1234567.89))    # 1,234,567.89
print(format_percentage(5.23))       # +5.23%
```

### Test 3 : Données Synthétiques

```python
from data_handler import DataHandler
from datetime import date

handler = DataHandler()
data = handler.get_historical_data(date.today())

print(f"MASI: {data['close']:.2f}")
print(f"Volume: {data['volume']:.0f}M")
print(f"Advances: {data['advances']}")
```

### Test 4 : Sentiment Complet

```python
from data_handler import DataHandler
from sentiment_calculator import MASISentimentCalculator
from datetime import date

handler = DataHandler()
calculator = MASISentimentCalculator()

data = handler.get_historical_data(date.today())
sentiment = calculator.calculate_sentiment(data, date.today())

print(f"Score: {sentiment['overall_score']:.1f}")
print(f"Label: {sentiment['sentiment_label']}")
print(f"Breadth: {sentiment['components']['breadth_score']:.1f}")
print(f"Momentum: {sentiment['components']['momentum_score']:.1f}")
```

---

## 🎯 Test du Dashboard (Sans Installation Locale)

Si vous voulez juste voir le résultat sans installer, voici les étapes :

### Navigation dans le Dashboard

1. **Page Dashboard (📈)** :
   - Score de sentiment au centre
   - Métriques MASI en haut
   - Composantes de sentiment
   - Niveaux techniques

2. **Market Analysis (📊)** :
   - Price Action (OHLC)
   - Breadth Analysis
   - Technical Indicators
   - Market Summary

3. **Historical Data (📅)** :
   - Sélectionner une période
   - Charger les données
   - Voir les graphiques
   - Exporter (CSV/Excel/JSON)

4. **Configuration (⚙️)** :
   - Ajuster les poids
   - Modifier les seuils
   - Configurer les indicateurs
   - Gérer le cache

5. **Backtesting (🔍)** :
   - Définir une stratégie
   - Lancer la simulation
   - Analyser les performances
   - Voir l'equity curve

---

## 🔧 Dépannage Rapide

### Problème : Dépendances manquantes

```bash
pip install -r requirements.txt
```

### Problème : Streamlit ne démarre pas

```bash
# Vérifier l'installation
pip show streamlit

# Réinstaller si nécessaire
pip install --upgrade streamlit

# Lancer avec verbose
streamlit run Main.py --logger.level=debug
```

### Problème : Erreurs d'import

```bash
# Vérifier que vous êtes dans le bon dossier
pwd  # Doit afficher .../first

# Vérifier que les fichiers existent
ls -la

# Tester les imports
python3 -c "import sys; sys.path.insert(0, '.'); from config import SENTIMENT_WEIGHTS; print(SENTIMENT_WEIGHTS)"
```

### Problème : Port déjà utilisé

```bash
# Utiliser un autre port
streamlit run Main.py --server.port=8502
```

---

## 📊 Résultats Attendus

### Test Automatique (./test_project.sh)

```
✓ PASS - Python installé
✓ PASS - pip installé
✓ PASS - Fichier Main.py existe
✓ PASS - Dossier components/ existe
✓ PASS - Imports Python basiques
✓ PASS - Système de cache
✓ PASS - Fonctions de formatage
✓ PASS - Calculateur de sentiment
✓ PASS - Gestionnaire de données
✓ PASS - Workflow complet
```

### Dashboard Lancé

```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### Sentiment Calculé

```
📊 ANALYSE DE SENTIMENT - 2025-12-10
==================================================
Score Global: 45.3/100
Label: ↗️ Bullish

📈 Composantes:
  - Breadth:    52.1 (poids: 30%)
  - Momentum:   38.5 (poids: 25%)
  - Trend:      41.2 (poids: 25%)
  - Volume:     48.9 (poids: 20%)

✓ Confiance: 87.5%
```

---

## 🎯 Checklist de Test Rapide

- [ ] ✅ Python 3.8+ installé
- [ ] ✅ Dépendances installées
- [ ] ✅ `./test_project.sh` passe tous les tests
- [ ] ✅ Dashboard se lance avec `streamlit run Main.py`
- [ ] ✅ Page principale affiche le sentiment
- [ ] ✅ Navigation fonctionne (5 pages)
- [ ] ✅ Données historiques chargent
- [ ] ✅ Export CSV fonctionne
- [ ] ✅ Backtesting s'exécute
- [ ] ✅ Configuration modifiable

---

## 💡 Commandes Utiles

```bash
# Lancer le dashboard
streamlit run Main.py

# Lancer avec un port différent
streamlit run Main.py --server.port=8502

# Lancer en mode debug
streamlit run Main.py --logger.level=debug

# Lancer sans ouvrir le navigateur
streamlit run Main.py --server.headless=true

# Test automatique
./test_project.sh

# Démarrage interactif
./quick_start.sh

# Vérifier les dépendances
pip list | grep -E "streamlit|pandas|numpy|plotly"

# Test Python rapide
python3 -c "from sentiment_calculator import MASISentimentCalculator; print('✓ OK')"
```

---

## 📞 Besoin d'Aide ?

1. **Lisez le guide complet** : `GUIDE_TEST.md`
2. **Exécutez le script de test** : `./test_project.sh`
3. **Lancez le quick start** : `./quick_start.sh`
4. **Consultez le README** : `README.md`

---

## 🎉 C'est Tout !

**Le plus simple :**
```bash
pip install -r requirements.txt && streamlit run Main.py
```

**Votre dashboard s'ouvrira sur http://localhost:8501** 🚀

---

*Dernière mise à jour : Décembre 2025*
