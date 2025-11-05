#!/usr/bin/env python3
"""Test rapide de la sérialisation JSON"""

import json
from core import Nyx

print("Test de sérialisation JSON...")

nyx = Nyx()

# Test dérivée (qui causait l'erreur)
print("\n1. Test dérivée: sin(x) * exp(x)")
response = nyx.ask("Calculer la dérivée de sin(x) * exp(x)", validate=False)

if response["success"]:
    print("   ✓ Succès!")
    # Tester la sérialisation JSON
    try:
        json_str = json.dumps(response, indent=2)
        print("   ✓ Sérialisation JSON réussie")
        print(f"   Résultat: {response['result']['result']['derivative']}")
    except Exception as e:
        print(f"   ✗ Erreur JSON: {e}")
else:
    print(f"   ✗ Erreur: {response.get('error')}")

# Test équation
print("\n2. Test équation: x² - 9 = 0")
response = nyx.ask("Résoudre x² - 9 = 0", validate=False)

if response["success"]:
    print("   ✓ Succès!")
    try:
        json_str = json.dumps(response, indent=2)
        print("   ✓ Sérialisation JSON réussie")
        print(f"   Solutions: {response['result']['result']['solutions']}")
    except Exception as e:
        print(f"   ✗ Erreur JSON: {e}")
else:
    print(f"   ✗ Erreur: {response.get('error')}")

# Test intégrale
print("\n3. Test intégrale: x²")
response = nyx.ask("Intégrale de x²", validate=False)

if response["success"]:
    print("   ✓ Succès!")
    try:
        json_str = json.dumps(response, indent=2)
        print("   ✓ Sérialisation JSON réussie")
        print(f"   Résultat: {response['result']['result']['integral']}")
    except Exception as e:
        print(f"   ✗ Erreur JSON: {e}")
else:
    print(f"   ✗ Erreur: {response.get('error')}")

nyx.shutdown()
print("\n✓ Tests terminés!")
