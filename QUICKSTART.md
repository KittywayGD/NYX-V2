# NYX-V2 - Guide de Démarrage Rapide

## ⚡ Installation Rapide

```bash
# 1. Installer les dépendances Python
pip install -r requirements.txt

# OU avec conda/mamba
conda install numpy scipy sympy matplotlib pandas
pip install pint uncertainties jsonschema pytest
```

## 🚀 Lancer Nyx

### Option 1: Application Interactive
```bash
python main.py
```

### Option 2: Exemples
```bash
python examples.py
```

### Option 3: Tests Rapides
```bash
python test_quick.py
```

### Option 4: Tests Complets
```bash
python tests/test_scientific.py
```

## 📝 Utilisation en Python

```python
from core import Nyx

# Initialiser
nyx = Nyx()

# Poser des questions
nyx.ask("Résoudre x² - 4 = 0")
nyx.ask("Calculer l'énergie d'un photon", context={"frequency": 5e14})
nyx.ask("Circuit RC", context={"resistance": 1000, "capacitance": 1e-6})
```

## ✅ Vérifier l'Installation

```bash
# Tester rapidement
python test_quick.py

# Ou tester l'import
python -c "from core import Nyx; print('✓ Nyx est prêt!')"
```

## 🐛 Résolution de Problèmes

### Erreur: ModuleNotFoundError
```bash
# Installer les dépendances manquantes
pip install -r requirements.txt
```

### Erreur: ImportError hbar from sympy
✅ Déjà corrigé dans la dernière version (commit 8875def)

### Les modules ne détectent pas les requêtes françaises
✅ Déjà corrigé dans la dernière version (commit 8875def)

## 📚 Documentation Complète

Voir [README.md](README.md) pour la documentation complète.
