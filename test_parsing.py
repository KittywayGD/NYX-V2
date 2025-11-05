#!/usr/bin/env python3
"""Test de l'extraction des expressions mathématiques"""

from core import Nyx

print("="*70)
print("TEST D'EXTRACTION DES EXPRESSIONS MATHÉMATIQUES")
print("="*70)

nyx = Nyx()

tests = [
    # Équations
    ("résoudre 2x - 4 = 0", "equation"),
    ("Résoudre x² - 9 = 0", "equation"),
    ("solve x + 5 = 10", "equation"),

    # Dérivées
    ("Calculer la dérivée de sin(x) * exp(x)", "derivative"),
    ("dérivée de x²", "derivative"),
    ("derivative of cos(x)", "derivative"),

    # Intégrales
    ("Intégrale de x²", "integral"),
    ("intégrale de 1/x de 1 à e", "integral"),
    ("integral of x from 0 to 2", "integral"),
]

for query, expected_type in tests:
    print(f"\n{'='*70}")
    print(f"Test: {query}")
    print(f"Type attendu: {expected_type}")

    response = nyx.ask(query, validate=False)

    if response["success"]:
        result = response["result"]["result"]
        if "error" in result:
            print(f"❌ Erreur: {result['error'][:80]}...")
        else:
            print(f"✓ Succès!")
            if "solutions" in result:
                print(f"   Solutions: {result['solutions']}")
            elif "derivative" in result:
                print(f"   Dérivée: {result['derivative']}")
            elif "integral" in result:
                print(f"   Intégrale: {result['integral']}")
    else:
        print(f"❌ Échec global: {response.get('error')}")

nyx.shutdown()
print(f"\n{'='*70}")
print("Tests terminés!")
print("="*70)
