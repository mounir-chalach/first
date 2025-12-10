#!/bin/bash

#######################################################
# Script de Test Complet - MASI Dashboard
# Teste toutes les fonctionnalités du projet
#######################################################

echo "🧪 =============================================="
echo "   MASI Dashboard - Script de Test Complet"
echo "================================================"
echo ""

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Compteurs
TESTS_PASSED=0
TESTS_FAILED=0

# Fonction pour afficher les résultats
test_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC} - $2"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC} - $2"
        ((TESTS_FAILED++))
    fi
}

echo -e "${BLUE}📋 Phase 1: Vérification de l'environnement${NC}"
echo "================================================"

# Test Python version
echo -n "Vérification de Python... "
python3 --version > /dev/null 2>&1
test_result $? "Python installé"

# Test pip
echo -n "Vérification de pip... "
python3 -m pip --version > /dev/null 2>&1
test_result $? "pip installé"

echo ""
echo -e "${BLUE}📦 Phase 2: Vérification de la structure du projet${NC}"
echo "================================================"

# Vérifier les fichiers principaux
files=("Main.py" "bl_client.py" "sentiment_calculator.py" "data_handler.py" "config.py" "requirements.txt")

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        test_result 0 "Fichier $file existe"
    else
        test_result 1 "Fichier $file manquant"
    fi
done

# Vérifier les dossiers
dirs=("components" "utils" "pages" "assets" "data")

for dir in "${dirs[@]}"; do
    if [ -d "$dir" ]; then
        test_result 0 "Dossier $dir/ existe"
    else
        test_result 1 "Dossier $dir/ manquant"
    fi
done

echo ""
echo -e "${BLUE}🔧 Phase 3: Test des imports Python${NC}"
echo "================================================"

# Test des imports
python3 << 'EOF'
import sys
sys.path.insert(0, '.')

errors = []

# Test imports principaux
try:
    import config
    print("✓ config importé")
except Exception as e:
    print(f"✗ Erreur config: {e}")
    errors.append("config")

try:
    import data_handler
    print("✓ data_handler importé")
except Exception as e:
    print(f"✗ Erreur data_handler: {e}")
    errors.append("data_handler")

try:
    import sentiment_calculator
    print("✓ sentiment_calculator importé")
except Exception as e:
    print(f"✗ Erreur sentiment_calculator: {e}")
    errors.append("sentiment_calculator")

# Test imports utils (pas de dépendances externes)
try:
    from utils.cache import cache_data, get_cached_data
    print("✓ utils.cache importé")
except Exception as e:
    print(f"✗ Erreur utils.cache: {e}")
    errors.append("utils.cache")

try:
    from utils.formatters import format_number, format_percentage
    print("✓ utils.formatters importé")
except Exception as e:
    print(f"✗ Erreur utils.formatters: {e}")
    errors.append("utils.formatters")

if errors:
    sys.exit(1)
else:
    sys.exit(0)
EOF

test_result $? "Imports Python basiques"

echo ""
echo -e "${BLUE}🧮 Phase 4: Test des fonctionnalités core${NC}"
echo "================================================"

# Test du système de cache
python3 << 'EOF'
from utils.cache import cache_data, get_cached_data, clear_cache

# Test cache set/get
cache_data("test_key", {"value": 123}, ttl=60)
result = get_cached_data("test_key")

if result and result.get("value") == 123:
    print("✓ Cache set/get fonctionne")
    exit(0)
else:
    print("✗ Cache ne fonctionne pas correctement")
    exit(1)
EOF

test_result $? "Système de cache"

# Test des formatters
python3 << 'EOF'
from utils.formatters import format_number, format_percentage, format_currency

# Test formatage nombre
result1 = format_number(1234567.89, decimals=2)
expected1 = "1,234,567.89"

# Test formatage pourcentage
result2 = format_percentage(5.234, decimals=2)
expected2 = "+5.23%"

# Test formatage devise
result3 = format_currency(1000, currency="MAD", decimals=0)
expected3 = "MAD 1,000"

if result1 == expected1 and result2 == expected2 and result3 == expected3:
    print("✓ Formatters fonctionnent correctement")
    print(f"  - Nombre: {result1}")
    print(f"  - Pourcentage: {result2}")
    print(f"  - Devise: {result3}")
    exit(0)
else:
    print("✗ Formatters ne fonctionnent pas correctement")
    exit(1)
EOF

test_result $? "Fonctions de formatage"

# Test du calculateur de sentiment
python3 << 'EOF'
from sentiment_calculator import MASISentimentCalculator
from datetime import date

calculator = MASISentimentCalculator()

# Données de test
test_data = {
    'close': 13000,
    'open': 12950,
    'high': 13100,
    'low': 12900,
    'volume': 2000,
    'volume_avg_20d': 1800,
    'advances': 450,
    'declines': 250,
    'unchanged': 50,
    'total_issues': 750,
    'new_highs': 15,
    'new_lows': 5,
    'change_pct': 0.4,
    'rsi': 55,
    'macd': 5,
    'macd_signal': 3,
    'stochastic': 60,
    'ma_20': 12980,
    'ma_50': 12950,
    'ma_200': 12900
}

# Calculer le sentiment
result = calculator.calculate_sentiment(test_data, date.today())

if result and 'overall_score' in result:
    score = result['overall_score']
    label = result['sentiment_label']
    print(f"✓ Calcul de sentiment réussi")
    print(f"  - Score: {score:.1f}")
    print(f"  - Label: {label}")
    print(f"  - Breadth: {result['components']['breadth_score']:.1f}")
    print(f"  - Momentum: {result['components']['momentum_score']:.1f}")
    print(f"  - Trend: {result['components']['trend_score']:.1f}")
    print(f"  - Volume: {result['components']['volume_score']:.1f}")
    exit(0)
else:
    print("✗ Échec du calcul de sentiment")
    exit(1)
EOF

test_result $? "Calculateur de sentiment"

# Test du data handler
python3 << 'EOF'
from data_handler import DataHandler
from datetime import date

handler = DataHandler()

# Test génération de données synthétiques
test_date = date.today()
data = handler.get_historical_data(test_date)

if data and 'close' in data and 'sentiment' not in str(data):
    print("✓ Génération de données synthétiques")
    print(f"  - Date: {data.get('date')}")
    print(f"  - Close: {data.get('close', 0):.2f}")
    print(f"  - Volume: {data.get('volume', 0):.0f}")
    print(f"  - Advances: {data.get('advances', 0)}")
    print(f"  - Declines: {data.get('declines', 0)}")
    exit(0)
else:
    print("✗ Échec génération de données")
    exit(1)
EOF

test_result $? "Gestionnaire de données"

echo ""
echo -e "${BLUE}📊 Phase 5: Test de scénario complet${NC}"
echo "================================================"

# Test du workflow complet
python3 << 'EOF'
from datetime import date
from data_handler import DataHandler
from sentiment_calculator import MASISentimentCalculator
from utils.cache import cache_data, get_cached_data

# 1. Récupérer des données
handler = DataHandler()
test_date = date.today()
market_data = handler.get_historical_data(test_date)

if not market_data:
    print("✗ Échec récupération données")
    exit(1)

# 2. Calculer le sentiment
calculator = MASISentimentCalculator()
sentiment = calculator.calculate_sentiment(market_data, test_date)

if not sentiment or 'overall_score' not in sentiment:
    print("✗ Échec calcul sentiment")
    exit(1)

# 3. Mettre en cache
cache_key = f"test_sentiment_{test_date}"
cache_data(cache_key, sentiment, ttl=3600)

# 4. Récupérer du cache
cached = get_cached_data(cache_key)

if not cached or cached['overall_score'] != sentiment['overall_score']:
    print("✗ Échec cache du sentiment")
    exit(1)

print("✓ Workflow complet réussi")
print(f"  1. ✓ Données récupérées: MASI {market_data['close']:.2f}")
print(f"  2. ✓ Sentiment calculé: {sentiment['overall_score']:.1f} ({sentiment['sentiment_label']})")
print(f"  3. ✓ Données mises en cache")
print(f"  4. ✓ Données récupérées du cache")
exit(0)
EOF

test_result $? "Workflow complet (données → sentiment → cache)"

echo ""
echo "================================================"
echo -e "${BLUE}📈 RÉSUMÉ DES TESTS${NC}"
echo "================================================"
echo -e "${GREEN}Tests réussis: $TESTS_PASSED${NC}"
echo -e "${RED}Tests échoués: $TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓✓✓ TOUS LES TESTS SONT PASSÉS ✓✓✓${NC}"
    echo ""
    echo "🚀 Le projet est prêt à être utilisé!"
    echo ""
    echo "Pour lancer le dashboard:"
    echo "  1. Installer les dépendances: pip install -r requirements.txt"
    echo "  2. Lancer l'application: streamlit run Main.py"
    echo ""
    exit 0
else
    echo -e "${RED}✗✗✗ CERTAINS TESTS ONT ÉCHOUÉ ✗✗✗${NC}"
    echo ""
    echo "Veuillez corriger les erreurs ci-dessus."
    exit 1
fi
