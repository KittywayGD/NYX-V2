# NYX-V2 - Assistant Scientifique Intelligent 🚀

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8+-yellow)
![Node](https://img.shields.io/badge/node-18+-green)

NYX-V2 est un assistant scientifique intelligent avec interface graphique Electron, capable de résoudre des problèmes avancés en mathématiques, physique et électronique, avec des visualisations interactives en temps réel.

## 🎯 Fonctionnalités

### ✨ Interface Graphique Moderne
- **Electron + React** avec design moderne dark theme
- **Chat interactif** avec l'assistant
- **3 Sandboxes côte à côte** pour visualisations

### 📊 Mathématiques
- Traçage 2D/3D interactif avec **Plotly.js**
- Courbes paramétriques et polaires
- Champs de vecteurs
- Animations avec paramètres variables
- Analyse automatique (zéros, extrema, points critiques)
- **Export PNG/SVG/JSON**

### 🎯 Physique
- Simulations en temps réel avec **Matter.js**
- Projectiles avec analyse énergétique
- Pendule simple (amorti/non-amorti)
- Collisions élastiques/inélastiques
- Propagation d'ondes

### ⚡ Électronique
- **Dessin de circuits** interactif
- Simulation RC/RL/RLC
- Diagrammes de Bode
- Analyseur de circuits
- Visualisation temporelle et fréquentielle

### 🧩 Système de Plugins
- Ajoutez vos propres modules facilement
- Hot-reload sans redémarrage
- Template generator inclus

### 🤖 Intent System Avancé
- Détection automatique d'intentions
- Support bilingue (FR/EN)
- Routing intelligent vers les modules

## 🚀 Démarrage Rapide (Une Commande!)

### Linux / Mac
```bash
./start-nyx.sh
```

### Windows (PowerShell)
```powershell
.\start-nyx.ps1
```

**C'est tout!** Le script va:
1. ✅ Vérifier les prérequis
2. ✅ Faire `git pull origin main`
3. ✅ Installer/mettre à jour les dépendances
4. ✅ Lancer l'API backend
5. ✅ Lancer l'application Electron
6. ✅ Afficher les logs en temps réel

**Appuyez sur Ctrl+C pour tout arrêter proprement.**

## 💬 Exemples

```
Tracer la fonction sin(x)*exp(-x)
```
→ Graphique 2D interactif avec Plotly

```
Simuler un projectile lancé à 45° avec vitesse 20m/s
```
→ Simulation Matter.js + graphiques énergie

```
Circuit RC avec R=1kΩ, C=1µF
```
→ Schéma + graphiques temporels

[Plus d'exemples dans README_GUI.md](README_GUI.md)

## 📦 Installation Manuelle

### Prérequis
- Python 3.8+
- Node.js 18+
- npm 8+
- git

### Installation

```bash
# Clone
git clone https://github.com/KittywayGD/NYX-V2.git
cd NYX-V2

# Python
python -m venv venv
source venv/bin/activate  # Linux/Mac | venv\Scripts\activate (Windows)
pip install -r requirements.txt
pip install -r api/requirements.txt

# Node.js
cd electron-app
npm install
cd ..
```

### Lancement Manuel (2 terminaux)

**Terminal 1 - API:**
```bash
cd api
python main.py
```

**Terminal 2 - Electron:**
```bash
cd electron-app
npm start
```

## 📖 Documentation

- **Guide Complet**: [README_GUI.md](README_GUI.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **API Docs**: http://localhost:8000/docs (quand l'API tourne)

## 🧩 Créer un Plugin

```python
from core.plugin_system import create_plugin_template

create_plugin_template('mon_plugin')
```

## 🎨 Screenshots

### Interface Principale
![Chat + Sandbox](docs/screenshots/main-interface.png)

### Math Sandbox (Plotly.js)
![Math Plot](docs/screenshots/math-sandbox.png)

### Physics Sandbox (Matter.js)
![Physics Sim](docs/screenshots/physics-sandbox.png)

### Electronics Sandbox
![Circuit](docs/screenshots/electronics-sandbox.png)

## 🔧 Technologies

**Backend:**
- Python 3.8+
- FastAPI
- SymPy, NumPy, SciPy

**Frontend:**
- Electron 27+
- React 18+
- TypeScript
- Tailwind CSS
- Plotly.js
- Matter.js
- Zustand

## 📊 Statistiques

- **~10,000 lignes de code**
- **3 sandboxes interactifs**
- **15+ endpoints API**
- **Système de plugins complet**
- **Bilingue** (FR/EN)

## 🤝 Contribution

1. Fork le projet
2. Créer une branche: `git checkout -b feature/ma-feature`
3. Commit: `git commit -m 'Add ma-feature'`
4. Push: `git push origin feature/ma-feature`
5. Pull Request

## 📝 Changelog

### v2.0.0 (2025-01-XX)
- ✨ Interface Electron + React
- ✨ Plotly.js pour graphiques interactifs
- ✨ Matter.js pour simulations physiques
- ✨ Circuit drawing
- ✨ Système de plugins
- ✨ Export PNG/SVG/JSON
- ✨ Script de démarrage unifié

### v1.0.0
- ✅ Modules scientifiques de base
- ✅ CLI interface

## 📄 Licence

MIT License

## 🆘 Support

- **Documentation**: [README_GUI.md](README_GUI.md)
- **Issues**: [GitHub Issues](https://github.com/KittywayGD/NYX-V2/issues)
- **API Docs**: http://localhost:8000/docs

---

**NYX-V2** - L'assistant scientifique qui comprend vraiment vos questions 🚀

*Développé avec ❤️ par l'équipe NYX*
