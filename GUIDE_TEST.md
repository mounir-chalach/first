# 🧪 Guide Complet de Test - MASI Dashboard

Ce guide vous explique comment tester votre projet étape par étape.

## 📋 Table des Matières

1. [Installation et Configuration](#1-installation-et-configuration)
2. [Test Automatique](#2-test-automatique)
3. [Test Manuel des Composants](#3-test-manuel-des-composants)
4. [Test avec Bloomberg Terminal](#4-test-avec-bloomberg-terminal)
5. [Test sans Bloomberg (Mode Synthétique)](#5-test-sans-bloomberg-mode-synthétique)
6. [Dépannage](#6-dépannage)

---

## 1. Installation et Configuration

### Étape 1.1 : Vérifier Python

```bash
python3 --version
# Doit afficher Python 3.8 ou supérieur
```

### Étape 1.2 : Créer un environnement virtuel

```bash
# Créer l'environnement
python3 -m venv venv

# Activer l'environnement
# Sur Linux/Mac:
source venv/bin/activate

# Sur Windows:
venv\Scripts\activate
```

Vous devriez voir `(venv)` apparaître dans votre terminal.

### Étape 1.3 : Installer les dépendances

```bash
# Mettre à jour pip
pip install --upgrade pip

# Installer toutes les dépendances
pip install -r requirements.txt

# Vérifier l'installation
pip list
```

**Dépendances installées :**
- ✅ streamlit (interface web)
- ✅ pandas (manipulation de données)
- ✅ numpy (calculs numériques)
- ✅ plotly (graphiques interactifs)
- ✅ blpapi (API Bloomberg - optionnel)
- ✅ python-dateutil (dates)
- ✅ pytz (fuseaux horaires)
- ✅ requests (requêtes HTTP)

---

## 2. Test Automatique

### Option A : Script de Test Complet

```bash
# Lancer le script de test automatique
./test_project.sh
```

Ce script vérifie :
- ✅ Structure du projet
- ✅ Imports Python
- ✅ Système de cache
- ✅ Formatage des données
- ✅ Calcul de sentiment
- ✅ Workflow complet

**Résultat attendu :**
```
✓✓✓ TOUS LES TESTS SONT PASSÉS ✓✓✓
Tests réussis: 19
Tests échoués: 0
```

### Option B : Test Python Direct

```bash
# Test des imports
python3 -c "
from utils.cache import cache_data
from utils.formatters import format_number
from sentiment_calculator import MASISentimentCalculator
from data_handler import DataHandler
print('✓ Tous les imports fonctionnent !')
"

# Test du calculateur
python3 -c "
from sentiment_calculator import MASISentimentCalculator
from datetime import date

calc = MASISentimentCalculator()
data = {
    'close': 13000, 'open': 12950, 'high': 13100, 'low': 12900,
    'volume': 2000, 'volume_avg_20d': 1800,
    'advances': 450, 'declines': 250, 'unchanged': 50,
    'total_issues': 750, 'new_highs': 15, 'new_lows': 5,
    'change_pct': 0.4, 'rsi': 55, 'macd': 5, 'macd_signal': 3,
    'stochastic': 60, 'ma_20': 12980, 'ma_50': 12950, 'ma_200': 12900
}

result = calc.calculate_sentiment(data, date.today())
print(f'✓ Sentiment calculé: {result[\"overall_score\"]:.1f} ({result[\"sentiment_label\"]})')
"
```

---

## 3. Test Manuel des Composants

### Test 3.1 : Système de Cache

```python
# Créer un fichier test_cache.py
from utils.cache import cache_data, get_cached_data, clear_cache

# Test 1: Écrire dans le cache
cache_data("test_key", {"valeur": 123, "nom": "test"}, ttl=60)
print("✓ Donnée écrite dans le cache")

# Test 2: Lire du cache
result = get_cached_data("test_key")
print(f"✓ Donnée lue: {result}")

# Test 3: Nettoyer le cache
clear_cache("test_key")
print("✓ Cache nettoyé")
```

```bash
python3 test_cache.py
```

### Test 3.2 : Formatage des Nombres

```python
# Créer un fichier test_formatters.py
from utils.formatters import (
    format_number, format_percentage, format_currency,
    format_large_number, format_volume
)

print("Tests de formatage:")
print(f"Nombre: {format_number(1234567.89)}")
print(f"Pourcentage: {format_percentage(5.234)}")
print(f"Devise: {format_currency(100000, currency='MAD')}")
print(f"Grand nombre: {format_large_number(1234567)}")
print(f"Volume: {format_volume(2500000)}")
```

```bash
python3 test_formatters.py
```

### Test 3.3 : Génération de Données Synthétiques

```python
# Créer un fichier test_data.py
from data_handler import DataHandler
from datetime import date

handler = DataHandler()
today = date.today()

# Générer des données pour aujourd'hui
data = handler.get_historical_data(today)

print(f"📊 Données générées pour {today}")
print(f"  - MASI Close: {data['close']:.2f}")
print(f"  - Volume: {data['volume']:.0f}M")
print(f"  - Advances: {data['advances']}")
print(f"  - Declines: {data['declines']}")
print(f"  - RSI: {data['rsi']:.1f}")
print(f"  - Change: {data['change_pct']:.2f}%")
```

```bash
python3 test_data.py
```

### Test 3.4 : Calcul de Sentiment Complet

```python
# Créer un fichier test_sentiment.py
from data_handler import DataHandler
from sentiment_calculator import MASISentimentCalculator
from datetime import date

# Initialiser
handler = DataHandler()
calculator = MASISentimentCalculator()
today = date.today()

# Récupérer des données
market_data = handler.get_historical_data(today)
print(f"✓ Données récupérées pour {today}")

# Calculer le sentiment
result = calculator.calculate_sentiment(market_data, today)

print(f"\n📊 ANALYSE DE SENTIMENT - {today}")
print(f"{'='*50}")
print(f"Score Global: {result['overall_score']:.1f}/100")
print(f"Label: {result['sentiment_label']}")
print(f"\n📈 Composantes:")
print(f"  - Breadth:   {result['components']['breadth_score']:>6.1f} (poids: 30%)")
print(f"  - Momentum:  {result['components']['momentum_score']:>6.1f} (poids: 25%)")
print(f"  - Trend:     {result['components']['trend_score']:>6.1f} (poids: 25%)")
print(f"  - Volume:    {result['components']['volume_score']:>6.1f} (poids: 20%)")
print(f"\n🎯 Niveaux Techniques:")
print(f"  - Pivot Point: {result['technical_levels']['pivot_point']:.2f}")
print(f"  - Resistance R1: {result['technical_levels']['resistance_r1']:.2f}")
print(f"  - Support S1: {result['technical_levels']['support_s1']:.2f}")
print(f"\n✓ Confiance: {result['confidence']:.1%}")
```

```bash
python3 test_sentiment.py
```

---

## 4. Test avec Bloomberg Terminal

### Prérequis
- Bloomberg Terminal installé et ouvert
- Bloomberg API (blpapi) installé
- Connexion active au terminal

### Test 4.1 : Vérifier la Connexion Bloomberg

```python
# Créer un fichier test_bloomberg.py
from bl_client import BloombergClient

print("🔌 Test de connexion Bloomberg...")
client = BloombergClient(host='localhost', port=8194)

if client.connected:
    print("✓ Connecté à Bloomberg Terminal")

    # Test de récupération de données
    from datetime import datetime
    data = client.get_masi_data(datetime.now())

    if data:
        print(f"\n📊 Données MASI récupérées:")
        print(f"  - Close: {data.get('close', 'N/A')}")
        print(f"  - Volume: {data.get('volume', 'N/A')}")
        print(f"  - Advances: {data.get('advances', 'N/A')}")
        print(f"  - Declines: {data.get('declines', 'N/A')}")
    else:
        print("⚠️  Pas de données disponibles")
else:
    print("✗ Impossible de se connecter à Bloomberg")
    print("  → Vérifiez que Bloomberg Terminal est ouvert")
    print("  → Vérifiez la connexion sur localhost:8194")
```

```bash
python3 test_bloomberg.py
```

### Test 4.2 : Lancer le Dashboard avec Bloomberg

```bash
# Lancer l'application
streamlit run Main.py

# Ou avec le script fourni
./run.sh
```

1. Le dashboard s'ouvre dans votre navigateur
2. Dans la sidebar, cliquez sur "Use Bloomberg Live Data"
3. Cliquez sur "Connect to Bloomberg"
4. Vérifiez le statut de connexion

---

## 5. Test sans Bloomberg (Mode Synthétique)

C'est le moyen le plus simple de tester !

### Étape 5.1 : Lancer l'Application

```bash
streamlit run Main.py
```

Le navigateur s'ouvre automatiquement à `http://localhost:8501`

### Étape 5.2 : Navigation et Tests

#### Test du Dashboard Principal
1. Observez le **score de sentiment** au centre
2. Vérifiez les **4 cartes métriques** en haut (MASI Close, Volume, Advances, Declines)
3. Regardez les **composantes de sentiment** (Breadth, Momentum, Trend, Volume)
4. Consultez les **niveaux techniques** en bas

#### Test de l'Analyse de Marché
1. Cliquez sur "📊 Market Analysis" dans la sidebar
2. Explorez les 4 onglets :
   - **Price Action** : Graphique OHLC
   - **Breadth Analysis** : Ratio Advances/Declines
   - **Technical Indicators** : RSI, MACD, Stochastic
   - **Summary** : Table récapitulative

#### Test des Données Historiques
1. Cliquez sur "📅 Historical Data"
2. Sélectionnez une plage de dates (ex: 30 derniers jours)
3. Cliquez sur "📊 Load Historical Data"
4. Observez :
   - Statistiques résumées
   - Graphique de timeline
   - Graphique des composantes
   - Table de données
5. Testez les exports (CSV, Excel, JSON)

#### Test de la Configuration
1. Cliquez sur "⚙️ Configuration"
2. Testez les 5 onglets :
   - **Sentiment Weights** : Ajustez les poids (total = 100%)
   - **Thresholds** : Modifiez les seuils de classification
   - **Technical Indicators** : Changez les périodes (RSI, MA, etc.)
   - **Cache Settings** : Gérez le cache
   - **Display Settings** : Options d'affichage

#### Test du Backtesting
1. Cliquez sur "🔍 Backtesting"
2. Configurez une stratégie :
   - Période: 90 derniers jours
   - Buy Signal: 30 (sentiment bullish)
   - Sell Signal: -30 (sentiment bearish)
   - Capital initial: 100,000 MAD
   - Position size: 100%
3. Cliquez sur "🚀 Run Backtest"
4. Analysez les résultats :
   - Performance metrics
   - Equity curve
   - Drawdown chart
   - Trade log

---

## 6. Dépannage

### Problème : "No module named 'streamlit'"

**Solution :**
```bash
pip install streamlit
# ou
pip install -r requirements.txt
```

### Problème : "No module named 'pandas'"

**Solution :**
```bash
pip install pandas numpy
```

### Problème : Bloomberg ne se connecte pas

**Solutions possibles :**
1. Vérifiez que Bloomberg Terminal est ouvert
2. Vérifiez le port (par défaut 8194)
3. Testez avec des données synthétiques d'abord
4. Vérifiez les logs dans le terminal

### Problème : Le dashboard ne se lance pas

**Solutions :**
```bash
# 1. Vérifier streamlit
streamlit version

# 2. Lancer avec verbose
streamlit run Main.py --logger.level=debug

# 3. Vérifier le port
streamlit run Main.py --server.port=8502
```

### Problème : Erreur d'import

**Solution :**
```bash
# S'assurer d'être dans le bon répertoire
cd /path/to/first

# Vérifier PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

---

## 7. Checklist de Test Complète

Utilisez cette checklist pour valider votre installation :

### Tests Basiques
- [ ] Python 3.8+ installé
- [ ] Environnement virtuel créé et activé
- [ ] Dépendances installées (`pip list`)
- [ ] Structure de projet vérifiée

### Tests Fonctionnels
- [ ] Système de cache fonctionne
- [ ] Formatters fonctionnent
- [ ] Génération de données synthétiques OK
- [ ] Calcul de sentiment OK
- [ ] Workflow complet fonctionne

### Tests Interface
- [ ] Dashboard se lance
- [ ] Page principale affiche le sentiment
- [ ] Market Analysis accessible
- [ ] Historical Data fonctionne
- [ ] Configuration modifiable
- [ ] Backtesting exécutable

### Tests Optionnels (avec Bloomberg)
- [ ] Connexion Bloomberg réussie
- [ ] Données MASI récupérées
- [ ] Sentiment calculé avec données réelles

---

## 8. Commandes de Test Rapides

```bash
# Test 1: Vérification rapide
python3 -c "from sentiment_calculator import MASISentimentCalculator; print('✓ OK')"

# Test 2: Générer des données
python3 -c "from data_handler import DataHandler; from datetime import date; print(DataHandler().get_historical_data(date.today())['close'])"

# Test 3: Lancer le dashboard
streamlit run Main.py

# Test 4: Test automatique complet
./test_project.sh

# Test 5: Vérifier les dépendances
pip check
```

---

## 📞 Support

Si vous rencontrez des problèmes :

1. Exécutez `./test_project.sh` pour identifier le problème
2. Vérifiez les logs dans le terminal
3. Consultez les messages d'erreur Python
4. Vérifiez que toutes les dépendances sont installées

---

**🎉 Bonne chance avec vos tests !**
