#!/bin/bash

###########################################
# NYX-V2 Startup Script (Linux/Mac)
# Lance tout le système d'une seule commande
###########################################

# Couleurs pour output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════╗"
echo "║          NYX-V2 Startup               ║"
echo "║  Assistant Scientifique Intelligent   ║"
echo "╚═══════════════════════════════════════╝"
echo -e "${NC}"

# Fonction pour vérifier si une commande existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Fonction pour nettoyer à la sortie
cleanup() {
    echo -e "\n${YELLOW}🛑 Arrêt de NYX-V2...${NC}"

    # Kill API process
    if [ ! -z "$API_PID" ]; then
        echo -e "${YELLOW}   Arrêt de l'API (PID: $API_PID)${NC}"
        kill $API_PID 2>/dev/null
    fi

    # Kill Electron process
    if [ ! -z "$ELECTRON_PID" ]; then
        echo -e "${YELLOW}   Arrêt d'Electron (PID: $ELECTRON_PID)${NC}"
        kill $ELECTRON_PID 2>/dev/null
    fi

    echo -e "${GREEN}✓ NYX-V2 arrêté proprement${NC}"
    exit 0
}

# Trap Ctrl+C
trap cleanup SIGINT SIGTERM

# Étape 1: Vérifications
echo -e "${BLUE}🔍 Vérification des prérequis...${NC}"

if ! command_exists python3; then
    echo -e "${RED}✗ Python 3 n'est pas installé!${NC}"
    exit 1
fi

if ! command_exists node; then
    echo -e "${RED}✗ Node.js n'est pas installé!${NC}"
    exit 1
fi

if ! command_exists git; then
    echo -e "${RED}✗ Git n'est pas installé!${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Tous les prérequis sont présents${NC}\n"

# Étape 2: Git pull
echo -e "${BLUE}📥 Mise à jour depuis GitHub...${NC}"

# Check if we're in a git repository
if [ -d ".git" ]; then
    # Save current branch
    CURRENT_BRANCH=$(git branch --show-current)
    echo -e "${YELLOW}   Branche actuelle: $CURRENT_BRANCH${NC}"

    # Stash local changes if any
    if [[ -n $(git status -s) ]]; then
        echo -e "${YELLOW}   Sauvegarde des modifications locales...${NC}"
        git stash push -m "Auto-stash before pull at $(date)"
    fi

    # Pull from main
    echo -e "${YELLOW}   git pull origin main${NC}"
    git pull origin main --no-edit

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Mise à jour réussie${NC}\n"
    else
        echo -e "${YELLOW}⚠ Mise à jour échouée (peut-être pas de connexion?)${NC}\n"
    fi

    # Return to original branch if different
    if [ "$CURRENT_BRANCH" != "main" ]; then
        git checkout "$CURRENT_BRANCH" 2>/dev/null
    fi
else
    echo -e "${YELLOW}⚠ Pas un repository git, skip pull${NC}\n"
fi

# Étape 3: Installer/Mettre à jour les dépendances Python
echo -e "${BLUE}📦 Vérification des dépendances Python...${NC}"

# Activate venv if it exists
if [ -d "venv" ]; then
    echo -e "${YELLOW}   Activation de l'environnement virtuel...${NC}"
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Check if pip packages need update
if [ -f "requirements.txt" ]; then
    echo -e "${YELLOW}   Installation des dépendances...${NC}"
    pip install -q -r requirements.txt
    pip install -q -r api/requirements.txt
    echo -e "${GREEN}✓ Dépendances Python à jour${NC}\n"
fi

# Étape 4: Installer/Mettre à jour les dépendances Node.js
echo -e "${BLUE}📦 Vérification des dépendances Node.js...${NC}"

cd electron-app

if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}   Installation des dépendances Node.js (première fois)...${NC}"
    npm install
else
    echo -e "${YELLOW}   Mise à jour des dépendances...${NC}"
    npm install --silent
fi

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dépendances Node.js à jour${NC}\n"
else
    echo -e "${RED}✗ Erreur lors de l'installation des dépendances Node.js${NC}"
    cd ..
    exit 1
fi

cd ..

# Créer le dossier logs s'il n'existe pas
mkdir -p logs

# Étape 5: Lancer l'API Python
echo -e "${BLUE}🚀 Lancement de l'API Backend...${NC}"

cd api
python3 main.py > ../logs/api.log 2>&1 &
API_PID=$!
cd ..

echo -e "${GREEN}✓ API démarrée (PID: $API_PID)${NC}"
echo -e "${YELLOW}   URL: http://localhost:8000${NC}"
echo -e "${YELLOW}   Docs: http://localhost:8000/docs${NC}\n"

# Attendre que l'API soit prête
echo -e "${BLUE}⏳ Attente du démarrage de l'API...${NC}"
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ API prête!${NC}\n"
        break
    fi
    sleep 1
    echo -n "."
done
echo ""

# Étape 6: Lancer l'application Electron
echo -e "${BLUE}🚀 Lancement de l'application Electron...${NC}"

cd electron-app
npm start > ../logs/electron.log 2>&1 &
ELECTRON_PID=$!
cd ..

echo -e "${GREEN}✓ Electron démarré (PID: $ELECTRON_PID)${NC}\n"

# Étape 7: Monitoring
echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║              NYX-V2 EST MAINTENANT ACTIF!              ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${BLUE}📊 Informations:${NC}"
echo -e "   API PID: $API_PID"
echo -e "   Electron PID: $ELECTRON_PID"
echo -e "   API URL: http://localhost:8000"
echo -e "   Logs: ./logs/"
echo ""
echo -e "${YELLOW}💡 Appuyez sur Ctrl+C pour arrêter NYX-V2${NC}"
echo ""

# Afficher les logs en temps réel
echo -e "${BLUE}📋 Logs (tail -f logs/api.log):${NC}"
echo -e "${YELLOW}────────────────────────────────────────────────────────${NC}"

# Tail les logs
tail -f logs/api.log 2>/dev/null &
TAIL_PID=$!

# Attendre que l'utilisateur arrête
wait $API_PID

# Cleanup sera appelé par le trap
cleanup
