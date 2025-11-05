# Changelog - NYX-V2

Toutes les modifications importantes de NYX-V2 sont documentées ici.

## [Unreleased] - 2025-01-XX

### 🔧 Corrections Critiques

#### [0c83998] - 2025-01-XX
**fix: Improve mathematical expression extraction from queries**
- Résout le problème de parsing des requêtes en langage naturel
- Les expressions comme "résoudre 2x - 4 = 0" fonctionnent maintenant
- Suppression intelligente des mots-clés (résoudre, solve, calculer, etc.)
- Support bilingue français/anglais pour les bornes d'intégration
- **Impact:** Les utilisateurs peuvent maintenant poser des questions en langage naturel

#### [331c44d] - 2025-01-XX
**fix: Resolve JSON serialization error for SymPy objects**
- Résout l'erreur "Object of type Mul is not JSON serializable"
- Ajout de la fonction `_clean_sympy_objects()` pour convertir automatiquement les objets SymPy en strings
- **Impact:** Toutes les opérations mathématiques retournent maintenant des résultats valides

#### [8875def] - 2025-01-XX
**fix: Improve module detection with French/English keyword support**
- Ajout de méthodes `can_handle()` intelligentes dans chaque module
- Support bilingue complet (français et anglais)
- Détection basée sur les mots-clés ET symboles mathématiques
- **Impact:** ⚠️ CRITIQUE - Sans ce fix, aucune requête française ne fonctionne!

### 📚 Documentation

#### [e34bc7d] - 2025-01-XX
**docs: Add quick test script and quickstart guide**
- Ajout de `test_quick.py` pour tester rapidement le système
- Ajout de `QUICKSTART.md` avec instructions d'installation
- Ajout de `test_parsing.py` pour tester l'extraction d'expressions

### 🎨 Améliorations

#### [efaed5d] - 2025-01-XX
**fix: Correct import error and rename Jarvis to Nyx**
- Correction de l'ImportError: `hbar` n'est pas disponible dans sympy
- Renommage complet Jarvis → Nyx dans tout le code
- **Impact:** Le système démarre correctement maintenant

#### [1a6c528] - 2025-01-XX
**feat: Add comprehensive examples file**
- Ajout de `examples.py` avec des exemples concrets
- Démonstrations de mathématiques, physique, électronique

## [Initial] - 2025-01-XX

#### [c6802aa] - 2025-01-XX
**feat: Implement NYX-V2 - Initial implementation**
- Architecture modulaire complète
- Système de validation récursive
- Modules scientifiques (Mathematics, Physics, Electronics)
- Interface CLI interactive

---

## Notes de Version

### Version Actuelle: Développement

**Fonctionnalités Principales:**
- ✅ Module Mathématiques: équations, dérivées, intégrales, matrices
- ✅ Module Physique: mécanique quantique, relativité, thermodynamique
- ✅ Module Électronique: circuits RC/RL/RLC, filtres, amplificateurs
- ✅ Validation récursive avec correction automatique
- ✅ Support bilingue français/anglais
- ✅ Détection automatique des modules

**Corrections Critiques Nécessaires pour l'Utilisation:**
1. Module detection fix (8875def) - **OBLIGATOIRE**
2. JSON serialization fix (331c44d) - **OBLIGATOIRE**
3. Expression extraction fix (0c83998) - **OBLIGATOIRE**

**Commits Actuels sur la Branche:**
- Total: 10 commits
- Feature branch: `claude/modular-recursive-jarvis-011CUoNHqjSXuL2Dt9KByZ7g`
- ⚠️ Les 3 derniers commits (8875def, 331c44d, 0c83998) ne sont **PAS ENCORE** dans `main`

---

## Migration vers Main

Pour que NYX-V2 fonctionne correctement en production, les commits suivants **DOIVENT** être mergés dans `main`:

1. `8875def` - Module detection (CRITIQUE)
2. `331c44d` - JSON serialization
3. `0c83998` - Expression extraction
4. `e34bc7d` - Documentation et tests

**Action requise:** Créer une Pull Request ou merger manuellement ces commits dans `main`.
