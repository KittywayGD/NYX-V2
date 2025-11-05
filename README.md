# NYX-V2

## Assistant Scientifique Modulaire et Récursif

**Version:** 1.0.0
**Auteur:** NYX-V2
**Licence:** MIT

---

## 📋 Description

NYX-V2 est un assistant scientifique avancé inspiré de J.A.R.V.I.S. (Just A Rather Very Intelligent System). Il est conçu pour résoudre des problèmes complexes en mathématiques, physique et électronique grâce à :

- **Architecture modulaire** : Modules indépendants et extensibles
- **Validation récursive** : Vérification automatique et correction des erreurs
- **Multi-domaines** : Mathématiques avancées, physique extrême, électronique

---

## 🚀 Fonctionnalités Principales

### Module Mathématiques Avancées
- ✅ Résolution d'équations algébriques et différentielles
- ✅ Calcul symbolique (dérivées, intégrales, limites)
- ✅ Algèbre linéaire (matrices, vecteurs, eigenvalues)
- ✅ Développements en série (Taylor, Fourier)
- ✅ Optimisation de fonctions
- ✅ Analyse numérique

### Module Physique Extrême
- ✅ Mécanique quantique (Schrödinger, Heisenberg)
- ✅ Relativité (restreinte et générale)
- ✅ Thermodynamique et statistique
- ✅ Électromagnétisme (Maxwell, ondes)
- ✅ Mécanique classique
- ✅ Physique nucléaire et des particules
- ✅ Astrophysique

### Module Électronique
- ✅ Analyse de circuits (DC/AC)
- ✅ Circuits RC, RL, RLC
- ✅ Design de filtres (passe-bas, passe-haut, passe-bande)
- ✅ Amplificateurs opérationnels
- ✅ Calculs d'impédance et résonance
- ✅ Transistors et composants actifs

### Système de Validation Récursive
- ✅ Vérification automatique des résultats
- ✅ Correction itérative des erreurs
- ✅ Validation croisée avec méthodes alternatives
- ✅ Score de confiance pour chaque résultat

---

## 📦 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
cd NYX-V2
pip install -r requirements.txt
```

### Dépendances principales
- `numpy` - Calculs numériques
- `scipy` - Fonctions scientifiques avancées
- `sympy` - Calculs symboliques
- `matplotlib` - Visualisation (optionnel)
- `pint` - Gestion des unités

---

## 🎯 Utilisation

### Lancement rapide

```bash
python main.py
```

### Utilisation en Python

```python
from core import Nyx

# Initialiser Nyx
nyx = Nyx()

# Poser une question
response = nyx.ask("Résoudre x² - 4 = 0")
print(response)

# Résoudre un problème avec paramètres
response = nyx.ask(
    "Calculer l'énergie d'un photon",
    context={"frequency": 5e14}
)

# Résoudre un problème complexe
response = nyx.solve(
    "Circuit RC",
    parameters={"resistance": 1000, "capacitance": 1e-6}
)
```

---

## 📖 Exemples d'Utilisation

### Exemple 1 : Mathématiques

```python
from core import Jarvis

jarvis = Jarvis()

# Résoudre une équation
response = nyx.ask("Résoudre 2x + 5 = 13")
# Résultat: x = 4

# Calculer une dérivée
response = nyx.ask("Dérivée de sin(x) * exp(x)")
# Résultat: exp(x)*sin(x) + exp(x)*cos(x)

# Calculer une intégrale
response = nyx.ask("Intégrale de x² de 0 à 2")
# Résultat: 8/3
```

### Exemple 2 : Physique

```python
# Calculer l'énergie d'un photon (lumière verte)
response = nyx.ask(
    "Énergie d'un photon",
    context={"frequency": 5.5e14}  # Hz
)
# E = h·ν ≈ 3.64 × 10⁻¹⁹ J

# Calculer E=mc²
response = nyx.ask(
    "mass-energy equivalence",
    context={"mass": 0.001}  # 1 gramme
)
# E = 9 × 10¹³ J (90 térajoules!)

# Principe d'incertitude de Heisenberg
response = nyx.ask("Principe d'incertitude de Heisenberg")
# Δx·Δp ≥ ℏ/2
```

### Exemple 3 : Électronique

```python
# Loi d'Ohm
response = nyx.ask(
    "Calculer le courant",
    context={"voltage": 12, "resistance": 100}
)
# I = 0.12 A (120 mA)

# Circuit RC
response = nyx.ask(
    "Circuit RC",
    context={"resistance": 10000, "capacitance": 100e-9}
)
# τ = 1 ms, f_c = 159 Hz

# Diviseur de tension
response = nyx.ask(
    "Diviseur de tension",
    context={"R1": 1000, "R2": 2000, "V_in": 12}
)
# V_out = 8V
```

### Exemple 4 : Validation Récursive

```python
# Avec validation activée (par défaut)
response = nyx.ask("Résoudre x³ - 8 = 0", validate=True)

print(response["validation"])
# {
#   "status": "valid",
#   "confidence": 0.95,
#   "iterations": 2,
#   "errors": []
# }
```

---

## 🏗️ Architecture

```
NYX-V2/
├── core/
│   ├── __init__.py
│   ├── nyx.py                 # Système principal
│   ├── module_manager.py      # Gestionnaire de modules
│   └── recursive_validator.py # Validation récursive
│
├── modules/
│   ├── base_module.py         # Classe de base
│   └── scientific/
│       ├── mathematics.py     # Module maths
│       ├── physics.py         # Module physique
│       ├── electronics.py     # Module électronique
│       └── solver.py          # Solver unifié
│
├── config/
│   └── modules.json           # Configuration
│
├── tests/
│   └── test_scientific.py     # Tests unitaires
│
├── main.py                    # Point d'entrée
├── requirements.txt           # Dépendances
└── README.md                  # Documentation
```

---

## 🧪 Tests

### Exécuter les tests

```bash
python tests/test_scientific.py
```

### Tests disponibles
- ✅ Module Mathématiques (équations, dérivées, intégrales)
- ✅ Module Physique (constantes, formules, calculs)
- ✅ Module Électronique (circuits, composants)
- ✅ Validation récursive
- ✅ Solver scientifique unifié

---

## 🔧 Configuration

Le fichier `config/modules.json` permet de configurer :

- Activation/désactivation des modules
- Paramètres de validation récursive
- Niveau de logging
- Précision numérique
- Timeouts

```json
{
  "recursive_validation": {
    "enabled": true,
    "max_iterations": 3,
    "min_confidence": 0.85
  }
}
```

---

## 📊 API Reference

### Classe Nyx

#### `nyx.ask(query, context=None, validate=True, module=None)`
Pose une question à Nyx.

**Paramètres:**
- `query` (str): La question ou requête
- `context` (dict, optionnel): Contexte avec paramètres
- `validate` (bool): Active la validation récursive
- `module` (str, optionnel): Force l'utilisation d'un module spécifique

**Retour:** Dictionnaire avec les résultats

#### `nyx.solve(problem, parameters=None, validate=True)`
Résout un problème scientifique complexe.

#### `nyx.get_status()`
Retourne le statut du système.

#### `nyx.list_modules()`
Liste tous les modules disponibles.

#### `nyx.get_capabilities()`
Retourne toutes les capacités disponibles.

---

## 🎓 Capacités Scientifiques Détaillées

### Mathématiques
- Algèbre: équations polynomiales, systèmes d'équations
- Analyse: dérivées, intégrales (définies et indéfinies), limites
- Équations différentielles: ordinaires et partielles
- Algèbre linéaire: matrices, déterminants, vecteurs propres
- Optimisation: recherche de minima/maxima
- Séries: Taylor, Maclaurin, Fourier
- Analyse numérique: approximations, interpolations

### Physique
- **Quantique**: équation de Schrödinger, principe d'Heisenberg, longueur d'onde de De Broglie
- **Relativité**: E=mc², dilatation du temps, contraction des longueurs, trous noirs
- **Thermodynamique**: lois des gaz parfaits, entropie, rayonnement du corps noir
- **Électromagnétisme**: loi de Coulomb, champs électriques/magnétiques, loi d'Ampère
- **Mécanique**: énergie cinétique/potentielle, forces, momentum
- **Ondes**: fréquence, longueur d'onde, effet Doppler

### Électronique
- **Circuits DC**: loi d'Ohm, lois de Kirchhoff, diviseurs de tension
- **Circuits AC**: impédance, réactance, déphasage
- **Filtres**: passe-bas, passe-haut, passe-bande, résonance
- **Composants**: résistances, condensateurs, inductances
- **Amplificateurs**: op-amp inverseurs/non-inverseurs
- **Analyse fréquentielle**: diagrammes de Bode, fonction de transfert

---

## 🚧 Limitations Actuelles

- Pas de support pour la biologie/chimie (comme demandé)
- Pas d'interface graphique (CLI uniquement)
- Pas de visualisation graphique automatique
- Parsing limité des équations en langage naturel français

---

## 🔮 Développements Futurs

- [ ] Interface graphique (GUI)
- [ ] Visualisation graphique des résultats
- [ ] Export des résultats (PDF, LaTeX)
- [ ] Base de données de problèmes résolus
- [ ] Module d'apprentissage automatique
- [ ] Support multilingue amélioré
- [ ] API REST pour intégration externe
- [ ] Module de chimie (optionnel)

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

---

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## 🙏 Remerciements

- **SymPy** - Moteur de calcul symbolique
- **SciPy** - Constantes et fonctions scientifiques
- **NumPy** - Calculs numériques performants
- **Inspiration**: J.A.R.V.I.S. de Marvel/Iron Man

---

## 📧 Contact

Pour toute question ou suggestion :
- Ouvrir une issue sur GitHub
- Contribuer au projet

---

## 🎯 Citation

Si vous utilisez NYX-V2 dans vos travaux, merci de citer :

```
NYX-V2 - Assistant Scientifique Modulaire et Récursif
Version 1.0.0
https://github.com/KittywayGD/NYX-V2
```

---

**Fait avec ❤️ pour la science et l'ingénierie**