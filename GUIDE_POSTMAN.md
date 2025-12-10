# 📮 Guide Postman - MASI Sentiment API

Guide complet pour tester l'API MASI Sentiment avec Postman.

## 📋 Table des Matières

1. [Installation et Démarrage](#1-installation-et-démarrage)
2. [Importer la Collection Postman](#2-importer-la-collection-postman)
3. [Endpoints Disponibles](#3-endpoints-disponibles)
4. [Exemples de Tests](#4-exemples-de-tests)
5. [Scénarios de Test](#5-scénarios-de-test)
6. [Dépannage](#6-dépannage)

---

## 1. Installation et Démarrage

### Étape 1.1 : Installer FastAPI et Uvicorn

```bash
# Ajouter les dépendances
pip install fastapi uvicorn pydantic

# Ou depuis requirements.txt (à ajouter)
echo "fastapi>=0.104.0" >> requirements.txt
echo "uvicorn[standard]>=0.24.0" >> requirements.txt
echo "pydantic>=2.0.0" >> requirements.txt

pip install -r requirements.txt
```

### Étape 1.2 : Lancer l'API

```bash
# Méthode 1: Python direct
python3 api.py

# Méthode 2: Uvicorn
uvicorn api:app --reload --host 0.0.0.0 --port 8000

# Méthode 3: En arrière-plan
nohup python3 api.py > api.log 2>&1 &
```

**Résultat attendu :**
```
🚀 Starting MASI Sentiment API...
📖 API Documentation: http://localhost:8000/docs
📊 Interactive Docs: http://localhost:8000/redoc

INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Étape 1.3 : Vérifier que l'API fonctionne

```bash
# Test avec curl
curl http://localhost:8000/

# Ou ouvrir dans un navigateur
# http://localhost:8000/docs
```

---

## 2. Importer la Collection Postman

### Méthode 1 : Import Direct

1. Ouvrir Postman
2. Cliquer sur **Import** (en haut à gauche)
3. Sélectionner le fichier `MASI_Sentiment_API.postman_collection.json`
4. Cliquer sur **Import**

### Méthode 2 : Import depuis URL

1. Dans Postman, cliquer sur **Import**
2. Sélectionner l'onglet **Link**
3. Coller l'URL du fichier JSON (si hébergé en ligne)
4. Cliquer sur **Continue** puis **Import**

### Méthode 3 : Copier-Coller le JSON

1. Ouvrir le fichier `MASI_Sentiment_API.postman_collection.json`
2. Copier tout le contenu
3. Dans Postman, **Import** > **Raw text**
4. Coller le JSON et importer

---

## 3. Endpoints Disponibles

### 📊 Overview des Endpoints

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Informations API |
| `/health` | GET | Health check |
| `/api/v1/sentiment` | GET | Sentiment actuel |
| `/api/v1/historical/{date}` | GET | Sentiment historique |
| `/api/v1/calculate` | POST | Calculer sentiment custom |
| `/api/v1/config` | GET | Configuration |
| `/api/v1/range` | GET | Sentiment sur période |
| `/api/v1/backtest` | POST | Backtesting |

---

## 4. Exemples de Tests

### Test 1 : Health Check

**Request:**
```http
GET http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "bloomberg_connected": false,
  "timestamp": "2024-12-10T16:30:00.000000"
}
```

**Dans Postman:**
1. Sélectionner `General` > `Health Check`
2. Cliquer sur **Send**
3. Vérifier le status code `200 OK`

---

### Test 2 : Sentiment Actuel (Synthétique)

**Request:**
```http
GET http://localhost:8000/api/v1/sentiment?use_bloomberg=false
```

**Expected Response:**
```json
{
  "overall_score": 42.5,
  "sentiment_label": "↗️ Bullish",
  "components": {
    "breadth_score": 45.2,
    "momentum_score": 38.5,
    "trend_score": 41.8,
    "volume_score": 46.1
  },
  "technical_levels": {
    "pivot_point": 13000.0,
    "resistance_r1": 13150.0,
    "resistance_r2": 13300.0,
    "support_s1": 12850.0,
    "support_s2": 12700.0,
    "ma_20": 12980.0,
    "ma_50": 12950.0,
    "ma_200": 12900.0
  },
  "confidence": 0.875,
  "timestamp": "2024-12-10T16:30:00",
  "analysis_date": "2024-12-10"
}
```

**Dans Postman:**
1. Aller dans `Sentiment Analysis` > `Get Current Sentiment (Synthetic)`
2. Cliquer sur **Send**
3. Observer le score de sentiment et les composantes

---

### Test 3 : Sentiment Historique

**Request:**
```http
GET http://localhost:8000/api/v1/historical/2024-12-01
```

**Dans Postman:**
1. Sélectionner `Sentiment Analysis` > `Get Historical Sentiment`
2. Modifier la date dans l'URL si nécessaire
3. Cliquer sur **Send**

**Variantes à tester:**
```
/api/v1/historical/2024-11-15
/api/v1/historical/2024-10-01
/api/v1/historical/2024-09-15
```

---

### Test 4 : Calculer Sentiment Custom (POST)

**Request:**
```http
POST http://localhost:8000/api/v1/calculate
Content-Type: application/json

{
  "close": 13500.0,
  "open": 13450.0,
  "high": 13600.0,
  "low": 13400.0,
  "volume": 2200.0,
  "volume_avg_20d": 2000.0,
  "advances": 500,
  "declines": 200,
  "unchanged": 50,
  "total_issues": 750,
  "new_highs": 20,
  "new_lows": 3,
  "rsi": 65.0,
  "macd": 8.0,
  "macd_signal": 5.0,
  "stochastic": 70.0,
  "ma_20": 13400.0,
  "ma_50": 13300.0,
  "ma_200": 13000.0
}
```

**Dans Postman:**
1. Aller dans `Sentiment Analysis` > `Calculate Sentiment (Custom Data)`
2. Le body JSON est déjà configuré
3. Cliquer sur **Send**
4. Tester avec différentes valeurs

---

### Test 5 : Sentiment sur Période

**Request:**
```http
GET http://localhost:8000/api/v1/range?start_date=2024-11-01&end_date=2024-11-30
```

**Expected Response:**
```json
{
  "start_date": "2024-11-01",
  "end_date": "2024-11-30",
  "count": 30,
  "data": [
    {
      "date": "2024-11-01",
      "score": 38.5,
      "label": "↗️ Bullish",
      "components": {...}
    },
    ...
  ]
}
```

**Dans Postman:**
1. Sélectionner `Sentiment Analysis` > `Get Sentiment Range`
2. Modifier les paramètres de query si nécessaire
3. Cliquer sur **Send**

---

### Test 6 : Backtesting

**Request:**
```http
POST http://localhost:8000/api/v1/backtest
Content-Type: application/json

{
  "start_date": "2024-11-01",
  "end_date": "2024-11-30",
  "entry_threshold": 30,
  "exit_threshold": -30,
  "initial_capital": 100000,
  "position_size": 1.0
}
```

**Expected Response:**
```json
{
  "parameters": {
    "start_date": "2024-11-01",
    "end_date": "2024-11-30",
    "entry_threshold": 30,
    "exit_threshold": -30,
    "initial_capital": 100000,
    "position_size": 1.0
  },
  "results": {
    "total_return": 5.23,
    "final_value": 105230.0,
    "total_trades": 8,
    "win_rate": 62.5,
    "max_drawdown": -3.2,
    "sharpe_ratio": 1.45
  },
  "trades": [...]
}
```

**Dans Postman:**
1. Aller dans `Backtesting` > `Run Backtest (30 days)`
2. Cliquer sur **Send**
3. Analyser les résultats de performance

---

## 5. Scénarios de Test

### Scénario 1 : Marché Très Bullish 🚀

**Objectif :** Tester avec un marché très haussier

**Steps:**
1. Sélectionner `Calculate Sentiment (Bullish Scenario)`
2. Vérifier les données dans le body :
   - `advances: 600`, `declines: 100` (ratio 6:1)
   - `new_highs: 50`, `new_lows: 2`
   - `rsi: 75` (zone overbought)
   - `close > open` (forte hausse)
3. Cliquer sur **Send**

**Expected Score:** > 60 (Very Bullish)

---

### Scénario 2 : Marché Très Bearish 📉

**Objectif :** Tester avec un marché très baissier

**Steps:**
1. Sélectionner `Calculate Sentiment (Bearish Scenario)`
2. Vérifier les données :
   - `advances: 150`, `declines: 550` (ratio 1:3.7)
   - `new_highs: 2`, `new_lows: 45`
   - `rsi: 25` (zone oversold)
   - `close < open` (forte baisse)
3. Cliquer sur **Send**

**Expected Score:** < -60 (Very Bearish)

---

### Scénario 3 : Test de Configuration

**Objectif :** Vérifier les poids et seuils

**Steps:**
1. Sélectionner `Configuration` > `Get Configuration`
2. Cliquer sur **Send**
3. Vérifier les valeurs :
   ```json
   {
     "sentiment_weights": {
       "breadth": 0.30,
       "momentum": 0.25,
       "trend": 0.25,
       "volume": 0.20
     },
     "thresholds": {
       "very_bullish": 60,
       "bullish": 30,
       "neutral": -30,
       "bearish": -60
     }
   }
   ```

---

### Scénario 4 : Backtesting Comparatif

**Objectif :** Comparer différentes stratégies

**Steps:**

**Test A - Stratégie Agressive:**
```json
{
  "entry_threshold": 20,
  "exit_threshold": -20,
  "position_size": 1.0
}
```

**Test B - Stratégie Conservative:**
```json
{
  "entry_threshold": 50,
  "exit_threshold": -50,
  "position_size": 0.5
}
```

**Test C - Stratégie Équilibrée:**
```json
{
  "entry_threshold": 30,
  "exit_threshold": -30,
  "position_size": 0.75
}
```

Comparer les résultats :
- Total Return
- Win Rate
- Sharpe Ratio
- Max Drawdown

---

### Scénario 5 : Test de Robustesse

**Objectif :** Tester les cas limites

**Test 1 - Date Future (doit échouer):**
```http
GET /api/v1/historical/2025-12-31
```
Expected: `400 Bad Request`

**Test 2 - Format de Date Invalide:**
```http
GET /api/v1/historical/31-12-2024
```
Expected: `400 Bad Request`

**Test 3 - Données Incomplètes:**
```json
POST /api/v1/calculate
{
  "close": 13000,
  "open": 12950
  // Champs manquants
}
```
Expected: `422 Unprocessable Entity`

---

## 6. Variables Postman

### Configuration des Variables

1. Dans Postman, aller dans la collection
2. Variables tab
3. Modifier `base_url` si nécessaire

**Variables utiles:**

| Variable | Valeur | Description |
|----------|--------|-------------|
| `base_url` | `http://localhost:8000` | URL de base |
| `api_version` | `v1` | Version de l'API |

**Utilisation dans les requêtes:**
```
{{base_url}}/api/{{api_version}}/sentiment
```

---

## 7. Tests Automatisés avec Scripts Postman

### Test Script Example

Dans l'onglet **Tests** de chaque requête :

```javascript
// Test 1: Status Code
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// Test 2: Response Time
pm.test("Response time is less than 2000ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(2000);
});

// Test 3: Sentiment Score Range
pm.test("Sentiment score is between -100 and 100", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.overall_score).to.be.within(-100, 100);
});

// Test 4: Required Fields
pm.test("Response has required fields", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('overall_score');
    pm.expect(jsonData).to.have.property('sentiment_label');
    pm.expect(jsonData).to.have.property('components');
});

// Test 5: Components Sum (optional)
pm.test("All components exist", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.components).to.have.property('breadth_score');
    pm.expect(jsonData.components).to.have.property('momentum_score');
    pm.expect(jsonData.components).to.have.property('trend_score');
    pm.expect(jsonData.components).to.have.property('volume_score');
});
```

---

## 8. Dépannage

### Problème : L'API ne démarre pas

**Solution :**
```bash
# Vérifier si le port est déjà utilisé
lsof -i :8000

# Utiliser un autre port
uvicorn api:app --port 8001

# Vérifier les dépendances
pip show fastapi uvicorn
```

### Problème : Erreur 422 lors du POST

**Solution :**
- Vérifier le Content-Type: `application/json`
- Vérifier que tous les champs requis sont présents
- Vérifier le format des nombres (pas de guillemets)

### Problème : Timeout

**Solution :**
```bash
# Augmenter le timeout dans Postman
Settings > Request timeout: 30000ms

# Ou limiter la période de backtest
```

### Problème : Bloomberg non connecté

**Solution :**
```bash
# Utiliser le mode synthétique
?use_bloomberg=false

# Ou vérifier Bloomberg Terminal
python3 -c "from bl_client import BloombergClient; print(BloombergClient().connected)"
```

---

## 9. Documentation Interactive

L'API inclut une documentation Swagger automatique :

**Swagger UI:** http://localhost:8000/docs
- Interface interactive
- Tester directement dans le navigateur
- Schémas de données

**ReDoc:** http://localhost:8000/redoc
- Documentation élégante
- Facile à lire
- Exemples inclus

---

## 10. Checklist de Test Complète

### Tests Basiques
- [ ] Health check réussi
- [ ] API Info accessible
- [ ] Configuration récupérée

### Tests de Sentiment
- [ ] Sentiment actuel (synthétique)
- [ ] Sentiment actuel (Bloomberg si disponible)
- [ ] Sentiment historique
- [ ] Calcul avec données custom
- [ ] Sentiment sur période

### Tests de Scénarios
- [ ] Scénario bullish
- [ ] Scénario bearish
- [ ] Scénario neutre

### Tests de Backtesting
- [ ] Backtest 30 jours
- [ ] Backtest 90 jours
- [ ] Stratégie conservative
- [ ] Stratégie aggressive

### Tests de Robustesse
- [ ] Date invalide
- [ ] Données incomplètes
- [ ] Format incorrect
- [ ] Période invalide

---

## 📞 Support

- Documentation interactive : http://localhost:8000/docs
- Collection Postman : `MASI_Sentiment_API.postman_collection.json`
- Guide complet : Ce fichier

---

**🎉 Vous êtes prêt à tester avec Postman !**
