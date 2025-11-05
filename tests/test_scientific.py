"""
Tests pour les modules scientifiques de Nyx
"""

import sys
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import Nyx
import json


def test_mathematics():
    """Test du module mathématiques"""
    print("\n" + "="*60)
    print("TEST: Module Mathématiques")
    print("="*60)

    nyx = Nyx()

    tests = [
        {
            "name": "Résolution d'équation simple",
            "query": "solve x² - 4 = 0",
            "expected_solutions": 2
        },
        {
            "name": "Dérivée",
            "query": "derivative of x²",
            "check": lambda r: "2*x" in str(r) or "2x" in str(r)
        },
        {
            "name": "Intégrale",
            "query": "integral of x",
            "check": lambda r: "x**2" in str(r) or "x²" in str(r)
        }
    ]

    passed = 0
    failed = 0

    for test in tests:
        print(f"\n📝 Test: {test['name']}")
        print(f"   Requête: {test['query']}")

        response = nyx.ask(test["query"], validate=False)

        if response.get("success"):
            print("   ✓ Succès")
            passed += 1
        else:
            print(f"   ✗ Échec: {response.get('error')}")
            failed += 1

        print(f"   Résultat: {json.dumps(response.get('result'), indent=6, ensure_ascii=False)}")

    print(f"\n{'='*60}")
    print(f"Tests réussis: {passed}/{passed+failed}")
    print(f"{'='*60}")

    return passed, failed


def test_physics():
    """Test du module physique"""
    print("\n" + "="*60)
    print("TEST: Module Physique")
    print("="*60)

    nyx = Nyx()

    tests = [
        {
            "name": "Énergie d'un photon",
            "query": "photon energy",
            "context": {"frequency": 5e14},
            "check": lambda r: "photon_energy" in str(r)
        },
        {
            "name": "E=mc²",
            "query": "mass-energy equivalence",
            "context": {"mass": 1.0},
            "check": lambda r: "energy" in str(r)
        },
        {
            "name": "Loi des gaz parfaits",
            "query": "ideal gas law",
            "context": {"pressure": 101325, "volume": 0.0224, "n": 1},
            "check": lambda r: "temperature" in str(r)
        }
    ]

    passed = 0
    failed = 0

    for test in tests:
        print(f"\n📝 Test: {test['name']}")
        print(f"   Requête: {test['query']}")
        if test.get("context"):
            print(f"   Context: {test['context']}")

        response = nyx.ask(test["query"], context=test.get("context"), validate=False)

        if response.get("success"):
            result_str = str(response.get("result"))
            if test.get("check") and test["check"](result_str):
                print("   ✓ Succès")
                passed += 1
            elif not test.get("check"):
                print("   ✓ Succès (pas de vérification)")
                passed += 1
            else:
                print("   ✗ Échec: résultat incorrect")
                failed += 1
        else:
            print(f"   ✗ Échec: {response.get('error')}")
            failed += 1

        print(f"   Résultat: {json.dumps(response.get('result'), indent=6, ensure_ascii=False)}")

    print(f"\n{'='*60}")
    print(f"Tests réussis: {passed}/{passed+failed}")
    print(f"{'='*60}")

    return passed, failed


def test_electronics():
    """Test du module électronique"""
    print("\n" + "="*60)
    print("TEST: Module Électronique")
    print("="*60)

    nyx = Nyx()

    tests = [
        {
            "name": "Loi d'Ohm",
            "query": "calculate current",
            "context": {"voltage": 12, "resistance": 100},
            "check": lambda r: "current" in str(r)
        },
        {
            "name": "Circuit RC",
            "query": "rc circuit time constant",
            "context": {"resistance": 1000, "capacitance": 1e-6},
            "check": lambda r: "time_constant" in str(r)
        },
        {
            "name": "Puissance électrique",
            "query": "power calculation",
            "context": {"voltage": 12, "current": 2},
            "check": lambda r: "power" in str(r) and "24" in str(r)
        }
    ]

    passed = 0
    failed = 0

    for test in tests:
        print(f"\n📝 Test: {test['name']}")
        print(f"   Requête: {test['query']}")
        print(f"   Context: {test['context']}")

        response = nyx.ask(test["query"], context=test["context"], validate=False)

        if response.get("success"):
            result_str = str(response.get("result"))
            if test["check"](result_str):
                print("   ✓ Succès")
                passed += 1
            else:
                print("   ✗ Échec: résultat incorrect")
                failed += 1
        else:
            print(f"   ✗ Échec: {response.get('error')}")
            failed += 1

        print(f"   Résultat: {json.dumps(response.get('result'), indent=6, ensure_ascii=False)}")

    print(f"\n{'='*60}")
    print(f"Tests réussis: {passed}/{passed+failed}")
    print(f"{'='*60}")

    return passed, failed


def test_recursive_validation():
    """Test du système de validation récursive"""
    print("\n" + "="*60)
    print("TEST: Validation Récursive")
    print("="*60)

    nyx = Nyx()

    # Test avec validation activée
    print("\n📝 Test avec validation récursive")
    response = jarvis.ask("solve x² - 9 = 0", validate=True)

    if "validation" in response:
        val = response["validation"]
        print(f"   Statut: {val['status']}")
        print(f"   Confiance: {val['confidence']:.2%}")
        print(f"   Itérations: {val['iterations']}")
        print("   ✓ Validation fonctionnelle")
        return 1, 0
    else:
        print("   ✗ Pas de validation dans la réponse")
        return 0, 1


def test_scientific_solver():
    """Test du solver scientifique unifié"""
    print("\n" + "="*60)
    print("TEST: Scientific Solver")
    print("="*60)

    nyx = Nyx()

    # Test de problème complexe
    print("\n📝 Test résolution de problème complexe")
    response = jarvis.solve(
        "Calculer l'énergie et la fréquence",
        parameters={"frequency": 1e15}
    )

    if response.get("success"):
        print("   ✓ Solver fonctionne")
        print(f"   Résultat: {json.dumps(response.get('result'), indent=6, ensure_ascii=False)}")
        return 1, 0
    else:
        print(f"   ✗ Échec: {response.get('error')}")
        return 0, 1


def run_all_tests():
    """Exécute tous les tests"""
    print("\n" + "="*60)
    print("NYX-V2 - SUITE DE TESTS")
    print("="*60)

    total_passed = 0
    total_failed = 0

    # Tests mathématiques
    passed, failed = test_mathematics()
    total_passed += passed
    total_failed += failed

    # Tests physique
    passed, failed = test_physics()
    total_passed += passed
    total_failed += failed

    # Tests électronique
    passed, failed = test_electronics()
    total_passed += passed
    total_failed += failed

    # Test validation récursive
    passed, failed = test_recursive_validation()
    total_passed += passed
    total_failed += failed

    # Test solver
    passed, failed = test_scientific_solver()
    total_passed += passed
    total_failed += failed

    # Résumé final
    print("\n" + "="*60)
    print("RÉSUMÉ FINAL")
    print("="*60)
    print(f"\n✓ Tests réussis: {total_passed}")
    print(f"✗ Tests échoués: {total_failed}")
    print(f"📊 Taux de réussite: {total_passed/(total_passed+total_failed)*100:.1f}%")
    print("\n" + "="*60)

    return total_passed, total_failed


if __name__ == "__main__":
    try:
        run_all_tests()
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()
