#!/bin/bash

# Script d'installation complète pour NYX-V2
# Installe toutes les dépendances et configure l'environnement

set -e  # Arrêter en cas d'erreur

echo "╔════════════════════════════════════════════════════════════╗"
echo "║          Installation NYX-V2 - Configuration Complète     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Couleurs pour le terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction d'affichage
print_step() {
    echo -e "${BLUE}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Vérification du répertoire
if [ ! -f "requirements.txt" ]; then
    print_error "Ce script doit être exécuté depuis le répertoire racine de NYX-V2"
    exit 1
fi

echo ""
print_step "Étape 1/4: Installation des dépendances Python"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Vérifier si Python 3 est installé
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 n'est pas installé"
    exit 1
fi

print_success "Python 3 trouvé: $(python3 --version)"

# Installer les dépendances Python principales
print_step "Installation des dépendances scientifiques..."
pip3 install --user -r requirements.txt 2>&1 | grep -E "(Successfully|already satisfied)" || true
print_success "Dépendances Python principales installées"

# Installer les dépendances API
print_step "Installation des dépendances API..."
pip3 install --user -r api/requirements.txt 2>&1 | grep -E "(Successfully|already satisfied)" || true
print_success "Dépendances API installées"

echo ""
print_step "Étape 2/4: Vérification de l'installation Python"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Tester les imports principaux
python3 << 'PYEOF'
import sys
try:
    import numpy
    print("✓ NumPy OK")
    import scipy
    print("✓ SciPy OK")
    import sympy
    print("✓ SymPy OK")
    import fastapi
    print("✓ FastAPI OK")
    import uvicorn
    print("✓ Uvicorn OK")
    import pint
    print("✓ Pint OK")
    import matplotlib
    print("✓ Matplotlib OK")
except ImportError as e:
    print(f"✗ Erreur d'import: {e}", file=sys.stderr)
    sys.exit(1)
PYEOF

if [ $? -eq 0 ]; then
    print_success "Tous les modules Python sont correctement installés"
else
    print_error "Certains modules Python ne sont pas installés correctement"
    exit 1
fi

echo ""
print_step "Étape 3/4: Installation des dépendances Node.js"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Vérifier si Node.js est installé
if ! command -v node &> /dev/null; then
    print_error "Node.js n'est pas installé"
    print_warning "Installez Node.js depuis https://nodejs.org/"
    exit 1
fi

print_success "Node.js trouvé: $(node --version)"
print_success "npm trouvé: $(npm --version)"

# Installer les dépendances du frontend
cd electron-app

print_step "Installation des dépendances Electron/React..."
npm install 2>&1 | tail -n 5

if [ -d "node_modules" ]; then
    print_success "Dépendances Node.js installées"
else
    print_error "Échec de l'installation des dépendances Node.js"
    exit 1
fi

cd ..

echo ""
print_step "Étape 4/4: Vérification de la configuration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Vérifier les fichiers de configuration
if [ -f "config/modules.json" ]; then
    print_success "Configuration des modules trouvée"
else
    print_warning "Configuration des modules manquante"
fi

if [ -f "electron-app/vite.config.js" ]; then
    print_success "Configuration Vite trouvée"
fi

if [ -f "electron-app/tailwind.config.js" ]; then
    print_success "Configuration Tailwind trouvée"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                  ✓ INSTALLATION TERMINÉE                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}NYX-V2 est prêt à être utilisé !${NC}"
echo ""
echo "Pour démarrer l'application:"
echo ""
echo "  ${BLUE}Option 1 - Application complète (recommandé):${NC}"
echo "    ./start-nyx.sh"
echo ""
echo "  ${BLUE}Option 2 - Backend seul:${NC}"
echo "    cd api && python3 main.py"
echo ""
echo "  ${BLUE}Option 3 - Frontend seul (backend doit tourner):${NC}"
echo "    cd electron-app && npm start"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
