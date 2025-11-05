# Architecture NYX-V2 avec Interface Graphique et Bacs à Sable

## Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────┐
│                    ELECTRON APP (Frontend)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Chat UI    │  │  Sandbox UI  │  │  Settings    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────┬────────────────────────────────────┘
                         │ IPC / HTTP
┌────────────────────────▼────────────────────────────────────┐
│                    REST API (Backend)                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Enhanced Intent System                   │   │
│  │  - Intent Classifier                                  │   │
│  │  - Context Manager                                    │   │
│  │  - Action Router                                      │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                      NYX-V2 CORE                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Mathematics  │  │   Physics    │  │ Electronics  │      │
│  │   Module     │  │   Module     │  │   Module     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                  │                  │              │
│  ┌──────▼──────┐  ┌────────▼────────┐  ┌─────▼──────┐      │
│  │   Math      │  │    Physics      │  │  Circuit   │      │
│  │  Sandbox    │  │    Sandbox      │  │  Sandbox   │      │
│  │  (Plotter)  │  │  (Simulator)    │  │(Simulator) │      │
│  └─────────────┘  └─────────────────┘  └────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## Composants Principaux

### 1. Frontend Electron + React

**Structure:**
```
electron-app/
├── src/
│   ├── main/           # Electron main process
│   ├── renderer/       # React app
│   │   ├── components/
│   │   │   ├── Chat/
│   │   │   ├── Sandbox/
│   │   │   │   ├── MathPlotter.tsx
│   │   │   │   ├── PhysicsSimulator.tsx
│   │   │   │   └── CircuitSimulator.tsx
│   │   │   └── Settings/
│   │   ├── hooks/
│   │   └── services/
│   └── preload/
├── package.json
└── electron-builder.yml
```

**Technologies:**
- Electron
- React + TypeScript
- Tailwind CSS
- Plotly.js (graphiques mathématiques)
- Matter.js (physique)
- Canvas API (circuits électroniques)

### 2. Backend API

**Structure:**
```
api/
├── main.py              # FastAPI application
├── routes/
│   ├── query.py         # Endpoints pour requêtes
│   ├── sandbox.py       # Endpoints pour sandboxes
│   └── intent.py        # Endpoints pour intent system
├── middleware/
│   └── cors.py
└── requirements.txt
```

**Endpoints:**
- `POST /api/query` - Soumettre une requête
- `POST /api/intent/detect` - Détecter l'intent
- `POST /api/sandbox/math/plot` - Tracer une fonction
- `POST /api/sandbox/physics/simulate` - Simuler physique
- `POST /api/sandbox/electronics/simulate` - Simuler circuit
- `GET /api/modules` - Liste des modules disponibles
- `GET /api/status` - Statut du système

### 3. Enhanced Intent System

**Intent Categories:**
```python
class IntentCategory(Enum):
    QUERY = "query"                    # Question simple
    COMPUTE = "compute"                # Calcul
    SOLVE = "solve"                    # Résolution
    VISUALIZE = "visualize"            # Visualisation
    SIMULATE = "simulate"              # Simulation
    EXPLAIN = "explain"                # Explication
    OPTIMIZE = "optimize"              # Optimisation
```

**Intent Detection Pipeline:**
1. **Preprocessing** - Nettoyage, normalisation
2. **Feature Extraction** - Keywords, patterns, entities
3. **Classification** - Intent + Confidence score
4. **Context Enrichment** - Historique, variables
5. **Action Routing** - Module + Method + Parameters

### 4. Sandboxes Interactifs

#### Math Sandbox
- **Traçage de fonctions** 2D/3D
- **Graphiques interactifs** (zoom, pan)
- **Animations** (paramètres variables)
- **Export** (PNG, SVG, données)

#### Physics Sandbox
- **Simulation 2D** (Matter.js)
- **Forces, collisions, gravité**
- **Objets personnalisés**
- **Contrôles temps réel**

#### Electronics Sandbox
- **Circuit builder** (drag & drop)
- **Composants:** résistances, condensateurs, inductances, sources
- **Simulation SPICE-like**
- **Oscilloscope virtuel**

## Technologies

### Backend
- Python 3.8+
- FastAPI
- SymPy, NumPy, SciPy
- Matplotlib (backend headless)
- PySpice (circuits)

### Frontend
- Electron 27+
- React 18+
- TypeScript
- Plotly.js
- Matter.js
- Tailwind CSS
- Zustand (state management)

## Flux de Données

### Requête Simple:
```
User Input → Intent Detection → Module Selection →
Execution → Response → UI Display
```

### Sandbox Workflow:
```
User Input → Intent Detection → Sandbox Mode →
Parameters Extraction → Sandbox Execution →
Interactive Display → User Interaction Loop
```

## Sécurité

- Sandboxing des exécutions Python
- Rate limiting
- Input validation
- CORS configuré
- Process isolation (Electron)

## Performance

- Caching des résultats
- Lazy loading des modules
- Web workers pour calculs lourds
- Virtual scrolling pour données
- Debouncing pour interactions

## Extensibilité

- Plugin system pour nouveaux modules
- Custom intent handlers
- Sandbox templates
- Theme system
