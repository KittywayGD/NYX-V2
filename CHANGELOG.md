# Changelog - NYX-V2

Toutes les modifications importantes de NYX-V2 sont documentées ici.

## [Unreleased] - 2025-01-XX

### 🔧 Corrections Critiques

#### [df8ffef] - 2025-01-XX
**fix: Add implicit multiplication and complete mathematical accuracy fixes**
- Ajout de la multiplication implicite: 2x → 2*x, 3xy → 3*x*y
- Conversion unicode dans dérivées et intégrales (x² → x**2)
- Reconnaissance de 'e' comme constante d'Euler dans les bornes
- Simplification de l'affichage des intégrales définies
- **Impact:** Tous les calculs mathématiques retournent maintenant des résultats corrects
- **Tests:**
  - ✅ résoudre 2x - 4 = 0 → ['2']
  - ✅ x² - 4 = 0 → ['-2', '2'] (était ['4'])
  - ✅ dérivée de x² → 2*x (était 0)
  - ✅ Intégrale de x² → x**3/3 (était x*x²)
  - ✅ intégrale de 1/x de 1 à e → 1 (était log(e))

#### [583e765] - 2025-01-XX
**fix: Correct mathematical computation errors**
- Correction de la conversion unicode des exposants (x² → x**2)
- Résolution explicite pour la variable x dans solve()
- Utilisation de expand() au lieu de simplify() pour les dérivées
- Évaluation numérique automatique des intégrales définies
- **Impact:** Correction des calculs qui retournaient des résultats incorrects

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
4. Mathematical accuracy fix (583e765) - **OBLIGATOIRE**
5. Implicit multiplication fix (df8ffef) - **OBLIGATOIRE**

**Commits Actuels sur la Branche:**
- Total: 14 commits
- Feature branch: `claude/modular-recursive-jarvis-011CUoNHqjSXuL2Dt9KByZ7g`
- ⚠️ Les 5 derniers commits ne sont **PAS ENCORE** dans `main`

---

## Migration vers Main

Pour que NYX-V2 fonctionne correctement en production, les commits suivants **DOIVENT** être mergés dans `main`:

1. `8875def` - Module detection (CRITIQUE)
2. `331c44d` - JSON serialization (CRITIQUE)
3. `0c83998` - Expression extraction (CRITIQUE)
4. `583e765` - Mathematical accuracy (CRITIQUE)
5. `df8ffef` - Implicit multiplication (CRITIQUE)
6. `e34bc7d` - Documentation et tests

**Action requise:** Créer une Pull Request ou merger manuellement ces commits dans `main`.
