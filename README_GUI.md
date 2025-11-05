# NYX-V2 avec Interface Graphique Electron

## 🎯 Vue d'Ensemble

NYX-V2 est un assistant scientifique intelligent avec:
- **Interface Graphique Electron + React** moderne et intuitive
- **Système d'Intent Amélioré** pour comprendre vos requêtes
- **3 Bacs à Sable Interactifs:**
  - 📊 **Mathématiques**: Traçage de courbes 2D/3D, animations
  - 🎯 **Physique**: Simulations de projectiles, pendules, collisions
  - ⚡ **Électronique**: Simulation de circuits RC/RL/RLC

## 📐 Architecture

```
NYX-V2/
├── core/                      # Moteur principal
│   ├── nyx.py                # Assistant NYX
│   └── intent_system.py      # Détection d'intentions
├── modules/
│   ├── scientific/           # Modules scientifiques
│   └── sandboxes/            # Bacs à sable interactifs
│       ├── math_sandbox.py
│       ├── physics_sandbox.py
│       └── electronics_sandbox.py
├── api/                       # Backend FastAPI
│   └── main.py
└── electron-app/             # Frontend Electron + React
    ├── src/
    │   ├── main/             # Processus principal Electron
    │   ├── renderer/         # Application React
    │   └── preload/          # Bridge sécurisé
    └── package.json
```

## 🚀 Installation

### Prérequis

- **Python 3.8+**
- **Node.js 18+** et npm
- pip, git

### Étape 1: Installation Python

```bash
cd NYX-V2

# Créer un environnement virtuel (recommandé)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances Python
pip install -r requirements.txt
pip install -r api/requirements.txt
```

### Étape 2: Installation Electron

```bash
cd electron-app

# Installer les dépendances Node.js
npm install
```

## 🎮 Utilisation

### Démarrage Complet

Vous devez lancer **2 processus** en parallèle:

#### Terminal 1: Backend API

```bash
cd NYX-V2
source venv/bin/activate  # Activer l'environnement

# Lancer l'API FastAPI
cd api
python main.py
```

L'API sera disponible sur `http://localhost:8000`

#### Terminal 2: Application Electron

```bash
cd NYX-V2/electron-app

# Lancer l'application
npm start
```

Cela va:
1. Démarrer le serveur de développement Vite (React)
2. Lancer l'application Electron

### Build Production

```bash
cd electron-app

# Build pour votre plateforme
npm run build           # Détection automatique
npm run build:win       # Windows
npm run build:mac       # macOS
npm run build:linux     # Linux
```

Les installeurs seront dans `electron-app/dist/`

## 📚 Guide d'Utilisation

### Interface Principale

L'interface est divisée en 3 zones:

1. **Sidebar** (gauche): Navigation entre sections
2. **Chat** (centre): Conversation avec NYX
3. **Sandbox** (droite): Visualisations interactives

### Exemples de Commandes

#### 📊 Mathématiques

```
Tracer la fonction sin(x)*exp(-x)
```
- Ouvre le sandbox mathématique
- Affiche la courbe avec analyse (zéros, extrema)

```
Tracer x² - 4 de -5 à 5
```
- Courbe avec intervalle personnalisé

```
Animer a*sin(x) avec a de -2 à 2
```
- Crée une animation interactive

```
Résoudre x² - 4 = 0
```
- Résout l'équation et affiche les solutions

#### 🎯 Physique

```
Simuler un projectile lancé à 45° avec vitesse 20m/s
```
- Simulation de trajectoire
- Graphiques énergie, vitesse

```
Simuler un pendule de longueur 1m, angle initial 45°
```
- Animation du pendule
- Analyse énergétique

```
Simuler une collision entre deux objets
```
- Simulation avec conservation de l'énergie
- Visualisation en temps réel

#### ⚡ Électronique

```
Circuit RC avec R=1kΩ, C=1µF
```
- Simulation charge/décharge
- Graphiques temporels

```
Analyser un circuit RLC série
```
- Régime oscillatoire
- Diagramme de Bode

```
Diviseur de tension avec R1=1kΩ, R2=2kΩ
```
- Calcul et analyse

### Intent System

Le système détecte automatiquement:
- **Catégorie**: VISUALIZE, SIMULATE, SOLVE, COMPUTE, etc.
- **Domaine**: Mathematics, Physics, Electronics
- **Action**: PLOT_FUNCTION, SIMULATE_MOTION, etc.
- **Confidence**: Score de confiance

Les intents sont affichés sous les réponses de l'assistant.

## 🔧 API REST

L'API expose plusieurs endpoints:

### Endpoints Principaux

```bash
# Query NYX
POST /api/query
{
  "query": "Tracer sin(x)",
  "context": null,
  "validate": true
}

# Detect Intent
POST /api/intent/detect
{
  "query": "Simuler un pendule"
}

# Status
GET /api/status

# Modules
GET /api/modules
```

### Sandbox Endpoints

```bash
# Math Sandbox
POST /api/sandbox/math/plot
{
  "function": "x**2",
  "x_min": -10,
  "x_max": 10,
  "plot_type": "2d"
}

# Physics Sandbox
POST /api/sandbox/physics/simulate
{
  "simulation_type": "projectile",
  "parameters": {
    "initial_velocity": 20,
    "angle_degrees": 45
  }
}

# Electronics Sandbox
POST /api/sandbox/electronics/simulate
{
  "circuit_type": "rc",
  "parameters": {
    "resistance": 1000,
    "capacitance": 1e-6,
    "voltage": 5
  }
}
```

## 🧪 Tests

### Test Backend

```bash
# Tester l'API
curl http://localhost:8000/health

# Ou utiliser la doc interactive
# Ouvrir dans le navigateur: http://localhost:8000/docs
```

### Test Sandboxes

```bash
cd NYX-V2
python -c "
from modules.sandboxes import MathSandbox
sandbox = MathSandbox()
result = sandbox.plot_function_2d('x**2', -10, 10)
print(result)
"
```

## 📊 Fonctionnalités des Sandboxes

### Math Sandbox

- **Traçage 2D**: Fonctions standards, trigonométriques, exponentielles
- **Traçage 3D**: Surfaces z = f(x, y)
- **Courbes paramétriques**: x(t), y(t)
- **Coordonnées polaires**: r(θ)
- **Champs de vecteurs**: Visualisation de gradients
- **Animations**: Paramètre variable
- **Analyse automatique**:
  - Points critiques (min/max)
  - Zéros de la fonction
  - Asymptotes

### Physics Sandbox

- **Projectile**: Trajectoire avec gravité
- **Pendule simple**: Oscillations avec/sans amortissement
- **Collisions**: Élastiques/inélastiques
- **Ondes**: Propagation (sinusoïdales, carrées, triangulaires)
- **Analyse énergétique**: Cinétique, potentielle, totale
- **Graphiques temps réel**

### Electronics Sandbox

- **Circuit RC**: Charge/décharge de condensateur
- **Circuit RL**: Établissement du courant
- **Circuit RLC**: Oscillations, régimes (sous-amorti, critique, sur-amorti)
- **Diviseur de tension**: Analyse et calculs
- **Réponse en fréquence**: Diagrammes de Bode
- **Analyses**:
  - Constante de temps
  - Facteur de qualité
  - Fréquence de résonance
  - Puissance dissipée

## 🎨 Personnalisation

### Thème

Modifiez `electron-app/tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      'nyx-accent': '#3b82f6', // Votre couleur principale
      // ...
    },
  },
},
```

### Ajouter un Module

1. Créer un module dans `modules/scientific/`
2. L'enregistrer dans `core/nyx.py`
3. Ajouter les keywords dans `core/intent_system.py`

### Ajouter un Sandbox

1. Créer un sandbox dans `modules/sandboxes/`
2. Ajouter les endpoints dans `api/main.py`
3. Créer le composant React dans `electron-app/src/renderer/components/`

## 🐛 Débogage

### L'API ne démarre pas

```bash
# Vérifier les logs
cd api
python main.py

# Vérifier les dépendances
pip list | grep fastapi
```

### Electron ne se connecte pas à l'API

1. Vérifier que l'API tourne sur `http://localhost:8000`
2. Vérifier les logs dans DevTools (F12)
3. Vérifier le fichier `electron-app/src/main/main.js` ligne 8

### Les sandboxes ne s'affichent pas

1. Vérifier dans DevTools (F12) les erreurs
2. Vérifier que les modules Python sont bien installés
3. Tester l'API directement: `curl http://localhost:8000/api/status`

## 📝 Logs

### Backend

Les logs Python sont dans la console où vous avez lancé `python main.py`

### Frontend

Ouvrir les DevTools: `Ctrl+Shift+I` (Windows/Linux) ou `Cmd+Option+I` (Mac)

## 🤝 Contribution

1. Fork le projet
2. Créer une branche: `git checkout -b feature/ma-fonctionnalite`
3. Commit: `git commit -m 'Ajout de ma fonctionnalité'`
4. Push: `git push origin feature/ma-fonctionnalite`
5. Pull Request

## 📄 Licence

MIT License - Voir [LICENSE](LICENSE)

## 🎓 Crédits

- **SymPy**: Calculs symboliques
- **NumPy/SciPy**: Calculs numériques
- **FastAPI**: Backend API
- **Electron**: Framework desktop
- **React**: Interface utilisateur
- **Plotly.js**: Visualisations (à intégrer)
- **Matter.js**: Physique 2D (à intégrer)

## 🆘 Support

- Documentation API: http://localhost:8000/docs
- Issues GitHub: https://github.com/KittywayGD/NYX-V2/issues
- Architecture: Voir [ARCHITECTURE.md](ARCHITECTURE.md)
- Changelog: Voir [CHANGELOG.md](CHANGELOG.md)

---

**NYX-V2** - Assistant Scientifique Intelligent avec Interface Graphique
