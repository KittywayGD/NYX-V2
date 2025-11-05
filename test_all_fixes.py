#!/usr/bin/env python3
"""Test complet de toutes les corrections mathématiques"""

from core import Nyx
import json

print("="*70)
print("TEST COMPLET DES CORRECTIONS MATHÉMATIQUES NYX-V2")
print("="*70)

nyx = Nyx()

# Tests des corrections
tests = [
    {
        "name": "Implicit Multiplication",
        "query": "résoudre 2x - 4 = 0",
        "expected": "['2']",
        "fix": "df8ffef"
    },
    {
        "name": "Unicode in Equations",
        "query": "Résoudre x² - 4 = 0",
        "expected": "['-2', '2']",
        "fix": "583e765 + df8ffef"
    },
    {
        "name": "Unicode in Derivatives",
        "query": "dérivée de x²",
        "expected": "2*x",
        "fix": "df8ffef"
    },
    {
        "name": "Unicode in Integrals",
        "query": "Intégrale de x²",
        "expected": "x**3/3",
        "fix": "df8ffef"
    },
    {
        "name": "Constant 'e' Recognition",
        "query": "intégrale de 1/x de 1 à e",
        "expected": "1",
        "fix": "df8ffef"
    },
    {
        "name": "Derivative Expansion",
        "query": "Calculer la dérivée de sin(x) * exp(x)",
        "expected": "exp(x)*sin(x) + exp(x)*cos(x)",
        "fix": "583e765"
    },
    {
        "name": "Numerical Integration",
        "query": "integral of x from 0 to 2",
        "expected": "2",
        "fix": "583e765"
    },
]

print("\n" + "="*70)
print("RÉSULTATS DES TESTS")
print("="*70)

passed = 0
failed = 0

for test in tests:
    print(f"\n📝 Test: {test['name']}")
    print(f"   Query: {test['query']}")
    print(f"   Expected: {test['expected']}")
    print(f"   Fix commit: {test['fix']}")

    response = nyx.ask(test['query'], validate=False)

    if response["success"]:
        result = response["result"]["result"]

        # Extract the actual result
        actual = None
        if "solutions" in result:
            actual = str(result["solutions"])
        elif "derivative" in result:
            actual = result["derivative"]
        elif "integral" in result:
            actual = result["integral"]

        if actual and test["expected"] in str(actual):
            print(f"   ✅ PASSED: {actual}")
            passed += 1
        else:
            print(f"   ❌ FAILED: Got {actual}")
            failed += 1
    else:
        print(f"   ❌ FAILED: {response.get('error')}")
        failed += 1

print("\n" + "="*70)
print(f"RÉSUMÉ: {passed}/{len(tests)} tests passés")
if failed == 0:
    print("🎉 TOUS LES TESTS SONT PASSÉS!")
else:
    print(f"⚠️  {failed} test(s) échoué(s)")
print("="*70)

nyx.shutdown()
