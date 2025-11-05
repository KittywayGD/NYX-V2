#!/usr/bin/env python3
"""
Exemples d'utilisation de NYX-V2
Démonstration des capacités scientifiques
"""

from core import Nyx

def main():
    print("="*70)
    print("NYX-V2 - Exemples d'Utilisation")
    print("="*70)

    # Initialiser Nyx
    print("\n🚀 Initialisation de Nyx...")
    nyx = Nyx()
    print("✓ Nyx initialisé\n")

    # Exemple 1: Mathématiques
    print("\n" + "="*70)
    print("EXEMPLE 1: Mathématiques - Résolution d'équation")
    print("="*70)
    print("Question: Résoudre x² - 9 = 0")

    response = nyx.ask("Résoudre x² - 9 = 0")
    if response["success"]:
        result = response["result"]["result"]
        print(f"✓ Solutions: {result.get('solutions', result)}")

    # Exemple 2: Physique
    print("\n" + "="*70)
    print("EXEMPLE 2: Physique - Énergie d'un photon")
    print("="*70)
    print("Question: Calculer l'énergie d'un photon de lumière verte")
    print("Fréquence: 5.5 × 10¹⁴ Hz")

    response = nyx.ask(
        "Calculer l'énergie d'un photon",
        context={"frequency": 5.5e14}
    )
    if response["success"]:
        result = response["result"]["result"]
        print(f"✓ Énergie: {result.get('photon_energy', 'N/A')} J")
        print(f"  Longueur d'onde: {result.get('wavelength', 'N/A')} m")

    # Exemple 3: Électronique
    print("\n" + "="*70)
    print("EXEMPLE 3: Électronique - Circuit RC")
    print("="*70)
    print("Question: Analyser un circuit RC")
    print("R = 10 kΩ, C = 100 nF")

    response = nyx.ask(
        "Circuit RC",
        context={"resistance": 10000, "capacitance": 100e-9}
    )
    if response["success"]:
        result = response["result"]["result"]
        print(f"✓ Constante de temps τ: {result.get('time_constant', 'N/A')} s")
        print(f"  Fréquence de coupure: {result.get('cutoff_frequency', 'N/A')} Hz")

    # Exemple 4: Validation récursive
    print("\n" + "="*70)
    print("EXEMPLE 4: Validation Récursive")
    print("="*70)
    print("Question: Résoudre x³ - 27 = 0 (avec validation)")

    response = nyx.ask("Résoudre x³ - 27 = 0", validate=True)
    if response["success"]:
        validation = response.get("validation", {})
        print(f"✓ Statut: {validation.get('status', 'N/A')}")
        print(f"  Confiance: {validation.get('confidence', 0):.2%}")
        print(f"  Itérations: {validation.get('iterations', 0)}")

    # Statut du système
    print("\n" + "="*70)
    print("STATUT DU SYSTÈME")
    print("="*70)

    status = nyx.get_status()
    print(f"✓ Modules chargés: {status['modules']['total_modules']}")
    print(f"✓ Modules actifs: {status['modules']['enabled_modules']}")
    print(f"✓ Requêtes traitées: {status['nyx']['queries_processed']}")

    capabilities = nyx.get_capabilities()
    print(f"✓ Capacités disponibles: {len(capabilities)}")
    print(f"  Exemples: {', '.join(capabilities[:5])}...")

    # Historique
    print("\n" + "="*70)
    print("HISTORIQUE DES REQUÊTES")
    print("="*70)

    history = nyx.get_history()
    for i, entry in enumerate(history, 1):
        print(f"{i}. {entry['query'][:50]}... - Succès: {entry['success']}")

    print("\n" + "="*70)
    print("Démonstration terminée!")
    print("="*70)

    nyx.shutdown()
    print("\n👋 Nyx arrêté")


if __name__ == "__main__":
    main()
