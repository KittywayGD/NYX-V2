#!/usr/bin/env python3
"""
Script de test pour vérifier le routing des modules
"""

import sys
sys.path.insert(0, '.')

from modules.scientific.physics import PhysicsModule
from modules.scientific.mathematics import MathematicsModule
from modules.scientific.electronics import ElectronicsModule
from modules.scientific.solver import ScientificSolver

def test_can_handle():
    """Test des méthodes can_handle() des modules"""

    # Initialiser les modules
    physics = PhysicsModule()
    physics.initialize()

    mathematics = MathematicsModule()
    mathematics.initialize()

    electronics = ElectronicsModule()
    electronics.initialize()

    solver = ScientificSolver()
    solver.initialize()

    # Requêtes de test
    test_queries = [
        ("Simuler un pendule", "Physics"),
        ("Tracer x² - 4", "Mathematics"),
        ("Circuit RC", "Electronics"),
        ("Calculer l'énergie d'un photon", "Physics"),
        ("Résoudre 2x + 5 = 0", "Mathematics"),
        ("Analyser un filtre passe-bas", "Electronics"),
        ("Simuler une collision élastique", "Physics"),
        ("Dériver sin(x)*cos(x)", "Mathematics"),
    ]

    print("="*70)
    print("TEST DES SCORES DE ROUTING DES MODULES")
    print("="*70)
    print()

    all_passed = True

    for query, expected_module in test_queries:
        print(f"Requête: '{query}'")
        print(f"Module attendu: {expected_module}")
        print("-" * 70)

        scores = {
            "Physics": physics.can_handle(query),
            "Mathematics": mathematics.can_handle(query),
            "Electronics": electronics.can_handle(query),
        }

        # Afficher tous les scores
        for module_name, score in scores.items():
            marker = "✓" if module_name == expected_module and score > 0.3 else " "
            print(f"  {marker} {module_name:15s}: {score:.3f}")

        # Vérifier si le bon module a le meilleur score
        best_module = max(scores, key=scores.get)
        best_score = scores[best_module]

        if best_module == expected_module and best_score > 0.3:
            print(f"  ✓ PASS - {best_module} sélectionné (score: {best_score:.3f})")
        else:
            print(f"  ✗ FAIL - {best_module} sélectionné au lieu de {expected_module}")
            print(f"           Score du module attendu: {scores[expected_module]:.3f}")
            all_passed = False

        print()

    print("="*70)
    if all_passed:
        print("✓ TOUS LES TESTS PASSENT")
    else:
        print("✗ CERTAINS TESTS ONT ÉCHOUÉ")
    print("="*70)

    return all_passed


if __name__ == "__main__":
    try:
        success = test_can_handle()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"ERREUR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
