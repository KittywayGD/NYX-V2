#!/usr/bin/env python3
"""
Script de vérification des mots-clés dans les modules
Sans dépendances externes
"""

import re

# Extraire les mots-clés de chaque fichier
def extract_keywords_from_file(filepath, keyword_dict_name):
    """Extrait les mots-clés d'un dictionnaire dans un fichier Python"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Trouver le dictionnaire
    pattern = rf"{keyword_dict_name}\s*=\s*\{{([^}}]+)\}}"
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        return []

    dict_content = match.group(1)

    # Extraire les clés (mots-clés)
    keywords = re.findall(r"'([^']+)':\s*[\d.]+", dict_content)

    return keywords


def test_keyword_coverage():
    """Vérifie que les mots-clés importants sont présents"""

    print("="*70)
    print("VÉRIFICATION DES MOTS-CLÉS DANS LES MODULES")
    print("="*70)
    print()

    # Test queries et leurs mots-clés attendus
    test_cases = [
        ("Simuler un pendule", "physics", ["pendule", "simuler"]),
        ("Tracer x² - 4", "mathematics", ["tracer"]),
        ("Circuit RC", "electronics", ["circuit", "rc"]),
    ]

    # Chemins des fichiers
    files = {
        "physics": "modules/scientific/physics.py",
        "mathematics": "modules/scientific/mathematics.py",
        "electronics": "modules/scientific/electronics.py",
    }

    all_passed = True

    for query, module_name, required_keywords in test_cases:
        filepath = files[module_name]

        print(f"Requête: '{query}'")
        print(f"Module: {module_name}")
        print(f"Mots-clés requis: {required_keywords}")

        # Extraire les mots-clés du module
        keywords = extract_keywords_from_file(filepath, f"{module_name}_keywords")

        # Vérifier chaque mot-clé
        missing = []
        found = []
        for keyword in required_keywords:
            if keyword in keywords:
                found.append(keyword)
            else:
                missing.append(keyword)

        if missing:
            print(f"  ✗ FAIL - Mots-clés manquants: {missing}")
            all_passed = False
        else:
            print(f"  ✓ PASS - Tous les mots-clés présents")

        print(f"  Trouvés: {found}")
        print()

    # Vérifier aussi le ScientificSolver
    print("Vérification du ScientificSolver...")
    solver_file = "modules/scientific/solver.py"

    with open(solver_file, 'r', encoding='utf-8') as f:
        solver_content = f.read()

    # Extraire physics_keywords du solver
    physics_pattern = r"physics_keywords\s*=\s*\[([^\]]+)\]"
    match = re.search(physics_pattern, solver_content, re.DOTALL)

    if match:
        physics_keywords_str = match.group(1)
        if "pendule" in physics_keywords_str and "simuler" in physics_keywords_str:
            print("  ✓ PASS - ScientificSolver contient 'pendule' et 'simuler'")
        else:
            print("  ✗ FAIL - ScientificSolver manque des mots-clés")
            all_passed = False
    else:
        print("  ✗ FAIL - Impossible de trouver physics_keywords dans ScientificSolver")
        all_passed = False

    print()
    print("="*70)
    if all_passed:
        print("✓ TOUS LES TESTS PASSENT")
        print("Les mots-clés sont correctement configurés !")
    else:
        print("✗ CERTAINS TESTS ONT ÉCHOUÉ")
    print("="*70)

    return all_passed


if __name__ == "__main__":
    import sys
    try:
        success = test_keyword_coverage()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"ERREUR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
