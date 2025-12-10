# 🚀 Quickstart Postman - 5 Minutes

Guide ultra-rapide pour tester l'API MASI avec Postman.

## ⚡ En 3 Étapes

### 1️⃣ Installer FastAPI (30 secondes)

```bash
pip install fastapi uvicorn pydantic
```

### 2️⃣ Lancer l'API (10 secondes)

```bash
python3 api.py
```

Résultat :
```
🚀 Starting MASI Sentiment API...
📖 API Documentation: http://localhost:8000/docs
```

### 3️⃣ Importer la Collection dans Postman (30 secondes)

1. Ouvrir Postman
2. **Import** → Sélectionner `MASI_Sentiment_API.postman_collection.json`
3. **Import**

✅ **C'est tout ! Vous pouvez maintenant tester !**

---

## 📊 Tests Rapides

### Test 1 : Health Check
```
GET http://localhost:8000/health
```
→ Postman : `General` > `Health Check` > **Send**

### Test 2 : Sentiment Actuel
```
GET http://localhost:8000/api/v1/sentiment
```
→ Postman : `Sentiment Analysis` > `Get Current Sentiment` > **Send**

### Test 3 : Calculer avec vos Données
```
POST http://localhost:8000/api/v1/calculate
```
→ Postman : `Sentiment Analysis` > `Calculate Sentiment` > **Send**

---

## 🎯 Endpoints Principaux

| Endpoint | Action | Description |
|----------|--------|-------------|
| `GET /health` | Health Check | Vérifier que l'API fonctionne |
| `GET /api/v1/sentiment` | Sentiment du jour | Score de sentiment actuel |
| `POST /api/v1/calculate` | Calcul custom | Avec vos propres données |
| `GET /api/v1/historical/{date}` | Historique | Sentiment pour une date |
| `POST /api/v1/backtest` | Backtesting | Tester une stratégie |

---

## 📝 Exemples de Body (POST)

### Calculer le Sentiment

```json
{
  "close": 13500.0,
  "open": 13450.0,
  "high": 13600.0,
  "low": 13400.0,
  "volume": 2200.0,
  "advances": 500,
  "declines": 200,
  "total_issues": 750,
  "rsi": 65.0
}
```

### Backtest

```json
{
  "start_date": "2024-11-01",
  "end_date": "2024-11-30",
  "entry_threshold": 30,
  "exit_threshold": -30,
  "initial_capital": 100000,
  "position_size": 1.0
}
```

---

## 🔥 Scénarios de Test Prêts à l'Emploi

Dans Postman, vous avez **15 requêtes pré-configurées** :

### 📊 Sentiment
- Sentiment actuel (synthétique)
- Sentiment actuel (Bloomberg)
- Sentiment historique
- Calcul custom
- Scénario bullish
- Scénario bearish
- Période de dates

### 🧪 Backtesting
- 30 jours
- 90 jours aggressive
- Stratégie conservative

### ⚙️ Configuration
- Voir les poids
- Voir les seuils

---

## 🌐 Documentation Interactive

Accédez à la doc Swagger :
```
http://localhost:8000/docs
```

Vous pouvez **tester directement dans le navigateur** !

---

## 🎓 Résultats Attendus

### Health Check
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "bloomberg_connected": false,
  "timestamp": "2024-12-10T..."
}
```

### Sentiment
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
  "confidence": 0.875
}
```

### Backtest
```json
{
  "results": {
    "total_return": 5.23,
    "final_value": 105230.0,
    "total_trades": 8,
    "win_rate": 62.5,
    "sharpe_ratio": 1.45
  }
}
```

---

## ❓ Problèmes Courants

### API ne démarre pas
```bash
# Vérifier les dépendances
pip install fastapi uvicorn pydantic

# Utiliser un autre port si 8000 occupé
uvicorn api:app --port 8001
```

### Postman : Erreur 422
- Vérifier `Content-Type: application/json`
- Vérifier que tous les champs requis sont présents

### Timeout
- Augmenter le timeout dans Postman
- Réduire la période de test

---

## 📚 Documentation Complète

Pour plus de détails, consultez :
- **GUIDE_POSTMAN.md** : Guide complet avec tous les scénarios
- **http://localhost:8000/docs** : Documentation Swagger interactive

---

## ✅ Checklist Rapide

- [ ] FastAPI installé
- [ ] API lancée (`python3 api.py`)
- [ ] Collection importée dans Postman
- [ ] Health check fonctionne
- [ ] Sentiment actuel testé
- [ ] Calcul custom testé

---

**🎉 Vous êtes prêt à tester avec Postman en 5 minutes !**

---

## 🚀 Pour Aller Plus Loin

```bash
# Lancer en production
uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4

# Avec auto-reload (développement)
uvicorn api:app --reload

# En arrière-plan
nohup python3 api.py > api.log 2>&1 &
```

---

*Dernière mise à jour : Décembre 2024*
