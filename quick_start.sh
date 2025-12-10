#!/bin/bash

#######################################################
# Quick Start Script - MASI Dashboard
# Lance le dashboard avec vérifications automatiques
#######################################################

echo "🚀 MASI Dashboard - Quick Start"
echo "================================"
echo ""

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Fonction pour afficher avec couleur
success() { echo -e "${GREEN}✓${NC} $1"; }
warning() { echo -e "${YELLOW}⚠${NC} $1"; }
error() { echo -e "${RED}✗${NC} $1"; }
info() { echo -e "${BLUE}ℹ${NC} $1"; }

# Étape 1: Vérifier Python
echo "📋 Vérification de l'environnement..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    success "Python $PYTHON_VERSION détecté"
else
    error "Python 3 non trouvé"
    echo "  → Installez Python 3.8 ou supérieur"
    exit 1
fi

# Étape 2: Vérifier l'environnement virtuel
if [ -d "venv" ]; then
    success "Environnement virtuel détecté"

    # Vérifier si activé
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        success "Environnement virtuel actif"
    else
        warning "Environnement virtuel non activé"
        echo ""
        echo "Pour activer l'environnement virtuel:"
        echo "  Linux/Mac: source venv/bin/activate"
        echo "  Windows:   venv\\Scripts\\activate"
        echo ""
        read -p "Voulez-vous que je l'active maintenant? (o/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[OoYy]$ ]]; then
            source venv/bin/activate
            success "Environnement activé"
        fi
    fi
else
    warning "Environnement virtuel non trouvé"
    read -p "Voulez-vous en créer un maintenant? (o/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[OoYy]$ ]]; then
        info "Création de l'environnement virtuel..."
        python3 -m venv venv
        success "Environnement virtuel créé"

        info "Activation..."
        source venv/bin/activate
        success "Environnement activé"
    else
        warning "Continuons sans environnement virtuel..."
    fi
fi

echo ""

# Étape 3: Vérifier les dépendances
echo "📦 Vérification des dépendances..."

MISSING_DEPS=0

# Vérifier streamlit
if python3 -c "import streamlit" 2>/dev/null; then
    success "streamlit installé"
else
    error "streamlit manquant"
    ((MISSING_DEPS++))
fi

# Vérifier pandas
if python3 -c "import pandas" 2>/dev/null; then
    success "pandas installé"
else
    error "pandas manquant"
    ((MISSING_DEPS++))
fi

# Vérifier numpy
if python3 -c "import numpy" 2>/dev/null; then
    success "numpy installé"
else
    error "numpy manquant"
    ((MISSING_DEPS++))
fi

# Vérifier plotly
if python3 -c "import plotly" 2>/dev/null; then
    success "plotly installé"
else
    error "plotly manquant"
    ((MISSING_DEPS++))
fi

if [ $MISSING_DEPS -gt 0 ]; then
    echo ""
    warning "$MISSING_DEPS dépendance(s) manquante(s)"
    read -p "Voulez-vous les installer maintenant? (o/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[OoYy]$ ]]; then
        info "Installation des dépendances..."
        pip install -r requirements.txt
        if [ $? -eq 0 ]; then
            success "Dépendances installées"
        else
            error "Échec de l'installation"
            exit 1
        fi
    else
        error "Impossible de continuer sans les dépendances"
        exit 1
    fi
fi

echo ""

# Étape 4: Vérifier la structure du projet
echo "🔍 Vérification de la structure..."

REQUIRED_FILES=("Main.py" "config.py" "sentiment_calculator.py" "data_handler.py")
REQUIRED_DIRS=("components" "utils" "pages" "data")

ALL_OK=1

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        error "Fichier manquant: $file"
        ALL_OK=0
    fi
done

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        error "Dossier manquant: $dir"
        ALL_OK=0
    fi
done

if [ $ALL_OK -eq 1 ]; then
    success "Structure du projet OK"
else
    error "Structure du projet incomplète"
    exit 1
fi

echo ""

# Étape 5: Tester une importation rapide
echo "🧪 Test rapide des imports..."
python3 -c "
from utils.cache import cache_data
from utils.formatters import format_number
print('✓ Imports OK')
" 2>/dev/null

if [ $? -eq 0 ]; then
    success "Tests d'import réussis"
else
    error "Échec des tests d'import"
    exit 1
fi

echo ""

# Étape 6: Vérifier Bloomberg (optionnel)
echo "🔌 Vérification Bloomberg (optionnel)..."
python3 -c "
try:
    import blpapi
    print('✓ Bloomberg API (blpapi) installé')
except:
    print('⚠ Bloomberg API non installé (optionnel)')
" 2>/dev/null

echo ""

# Étape 7: Options de lancement
echo "================================"
echo "✅ Tout est prêt!"
echo "================================"
echo ""
echo "Comment voulez-vous lancer le dashboard?"
echo ""
echo "1) Mode normal (avec navigateur)"
echo "2) Mode headless (sans navigateur)"
echo "3) Mode debug (avec logs détaillés)"
echo "4) Spécifier un port personnalisé"
echo "5) Lancer le script de test complet"
echo "6) Quitter"
echo ""

read -p "Votre choix (1-6): " choice

case $choice in
    1)
        info "Lancement du dashboard en mode normal..."
        echo ""
        success "Le dashboard va s'ouvrir dans votre navigateur"
        echo "URL: http://localhost:8501"
        echo ""
        echo "Pour arrêter: Ctrl+C"
        echo ""
        streamlit run Main.py
        ;;
    2)
        info "Lancement en mode headless..."
        echo ""
        echo "Accédez manuellement à: http://localhost:8501"
        echo ""
        streamlit run Main.py --server.headless=true
        ;;
    3)
        info "Lancement en mode debug..."
        echo ""
        streamlit run Main.py --logger.level=debug
        ;;
    4)
        read -p "Port à utiliser (ex: 8502): " port
        info "Lancement sur le port $port..."
        echo ""
        echo "URL: http://localhost:$port"
        echo ""
        streamlit run Main.py --server.port=$port
        ;;
    5)
        info "Lancement du script de test..."
        echo ""
        ./test_project.sh
        ;;
    6)
        info "Au revoir!"
        exit 0
        ;;
    *)
        error "Choix invalide"
        exit 1
        ;;
esac
