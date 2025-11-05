#!/usr/bin/env python3
"""
Test rapide pour vérifier le fonctionnement de Nyx
"""

from core import Nyx

def test_module_detection():
    """Teste la détection automatique des modules"""
    print("="*70)
    print("TEST DE DÉTECTION DES MODULES")
    print("="*70)

    nyx = Nyx()

    # Test 1: Mathématiques
    print("\n1. Test Mathématiques - 'Résoudre x² - 4 = 0'")
    math_module = nyx.module_manager.find_best_module("Résoudre x² - 4 = 0")
    if math_module:
        print(f"   ✓ Module trouvé: {math_module.name}")
    else:
        print("   ✗ Aucun module trouvé")

    # Test 2: Physique
    print("\n2. Test Physique - 'Calculer l'énergie d'un photon'")
    physics_module = nyx.module_manager.find_best_module("Calculer l'énergie d'un photon")
    if physics_module:
        print(f"   ✓ Module trouvé: {physics_module.name}")
    else:
        print("   ✗ Aucun module trouvé")

    # Test 3: Électronique
    print("\n3. Test Électronique - 'Circuit RC'")
    elec_module = nyx.module_manager.find_best_module("Circuit RC")
    if elec_module:
        print(f"   ✓ Module trouvé: {elec_module.name}")
    else:
        print("   ✗ Aucun module trouvé")

    print("\n" + "="*70)

def test_simple_queries():
    """Teste des requêtes simples"""
    print("\n" + "="*70)
    print("TEST DE REQUÊTES SIMPLES")
    print("="*70)

    nyx = Nyx()

    # Test mathématiques
    print("\n1. Mathématiques: Résoudre x² - 9 = 0")
    response = nyx.ask("Résoudre x² - 9 = 0", validate=False)
    if response["success"]:
        print(f"   ✓ Succès!")
        result = response["result"]
        if "result" in result and "solutions" in result["result"]:
            print(f"   Solutions: {result['result']['solutions']}")
    else:
        print(f"   ✗ Erreur: {response.get('error')}")

    # Test physique
    print("\n2. Physique: Calculer l'énergie d'un photon")
    response = nyx.ask("Calculer l'énergie d'un photon",
                       context={"frequency": 5e14},
                       validate=False)
    if response["success"]:
        print(f"   ✓ Succès!")
        result = response["result"]
        if "result" in result:
            print(f"   Résultat: {result['result']}")
    else:
        print(f"   ✗ Erreur: {response.get('error')}")

    # Test électronique
    print("\n3. Électronique: Circuit RC")
    response = nyx.ask("Circuit RC",
                       context={"resistance": 1000, "capacitance": 1e-6},
                       validate=False)
    if response["success"]:
        print(f"   ✓ Succès!")
        result = response["result"]
        if "result" in result and "time_constant" in result["result"]:
            print(f"   Constante de temps: {result['result']['time_constant']} s")
    else:
        print(f"   ✗ Erreur: {response.get('error')}")

    print("\n" + "="*70)

    nyx.shutdown()

if __name__ == "__main__":
    print("\nNYX-V2 - Tests Rapides\n")
    test_module_detection()
    test_simple_queries()
    print("\n✓ Tests terminés!\n")
