#!/usr/bin/env python3
"""
NYX-V2 Jarvis - Point d'entrée principal
Assistant scientifique modulaire et récursif
"""

import sys
import json
from pathlib import Path

# Ajouter le répertoire courant au path
sys.path.insert(0, str(Path(__file__).parent))

from core import Jarvis


def print_banner():
    """Affiche la bannière de démarrage"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║              NYX-V2 JARVIS v1.0.0                        ║
    ║     Assistant Scientifique Modulaire et Récursif         ║
    ║                                                           ║
    ║  Mathématiques Avancées | Physique Extrême | Électronique║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_result(response: dict):
    """Affiche les résultats de manière formatée"""
    print("\n" + "="*60)
    print("RÉSULTAT")
    print("="*60)

    if response.get("success"):
        result = response.get("result", {})

        # Afficher le résultat principal
        if isinstance(result, dict):
            if "result" in result:
                print(f"\n📊 Résultat: {json.dumps(result['result'], indent=2, ensure_ascii=False)}")
            else:
                print(f"\n📊 {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"\n📊 {result}")

        # Afficher la validation si présente
        if "validation" in response:
            val = response["validation"]
            status_emoji = "✓" if val["status"] == "valid" else "⚠"
            print(f"\n{status_emoji} Validation: {val['status']}")
            print(f"   Confiance: {val['confidence']:.2%}")
            print(f"   Itérations: {val['iterations']}")

            if val.get("errors"):
                print(f"   Erreurs: {', '.join(val['errors'])}")
    else:
        print(f"\n❌ Erreur: {response.get('error', 'Erreur inconnue')}")

    print("="*60 + "\n")


def demo_mathematics(jarvis: Jarvis):
    """Démonstration du module mathématiques"""
    print("\n" + "="*60)
    print("DÉMONSTRATION: Module Mathématiques")
    print("="*60 + "\n")

    examples = [
        {
            "query": "Résoudre x² - 4 = 0",
            "context": None
        },
        {
            "query": "Calculer la dérivée de sin(x) * exp(x)",
            "context": None
        },
        {
            "query": "Intégrale de 1/x de 1 à e",
            "context": None
        }
    ]

    for example in examples:
        print(f"📝 Question: {example['query']}")
        response = jarvis.ask(example["query"], example["context"])
        print_result(response)
        input("Appuyez sur Entrée pour continuer...")


def demo_physics(jarvis: Jarvis):
    """Démonstration du module physique"""
    print("\n" + "="*60)
    print("DÉMONSTRATION: Module Physique")
    print("="*60 + "\n")

    examples = [
        {
            "query": "Calculer l'énergie d'un photon",
            "context": {"frequency": 5e14}  # 500 THz (lumière verte)
        },
        {
            "query": "E=mc² pour 1 kg",
            "context": {"mass": 1.0}
        },
        {
            "query": "Principe d'incertitude de Heisenberg",
            "context": None
        }
    ]

    for example in examples:
        print(f"📝 Question: {example['query']}")
        if example["context"]:
            print(f"   Paramètres: {example['context']}")
        response = jarvis.ask(example["query"], example["context"])
        print_result(response)
        input("Appuyez sur Entrée pour continuer...")


def demo_electronics(jarvis: Jarvis):
    """Démonstration du module électronique"""
    print("\n" + "="*60)
    print("DÉMONSTRATION: Module Électronique")
    print("="*60 + "\n")

    examples = [
        {
            "query": "Loi d'Ohm avec V=12V et R=100Ω",
            "context": {"voltage": 12, "resistance": 100}
        },
        {
            "query": "Circuit RC avec R=1kΩ et C=1µF",
            "context": {"resistance": 1000, "capacitance": 1e-6}
        },
        {
            "query": "Calculer la puissance",
            "context": {"voltage": 12, "current": 0.5}
        }
    ]

    for example in examples:
        print(f"📝 Question: {example['query']}")
        if example["context"]:
            print(f"   Paramètres: {example['context']}")
        response = jarvis.ask(example["query"], example["context"])
        print_result(response)
        input("Appuyez sur Entrée pour continuer...")


def interactive_mode(jarvis: Jarvis):
    """Mode interactif"""
    print("\n" + "="*60)
    print("MODE INTERACTIF")
    print("="*60)
    print("\nCommandes spéciales:")
    print("  /status  - Afficher le statut du système")
    print("  /modules - Lister les modules")
    print("  /history - Afficher l'historique")
    print("  /help    - Afficher l'aide")
    print("  /quit    - Quitter")
    print("\nPosez vos questions scientifiques ci-dessous:")
    print("="*60 + "\n")

    while True:
        try:
            query = input("Jarvis> ").strip()

            if not query:
                continue

            # Commandes spéciales
            if query == "/quit":
                print("Au revoir!")
                break
            elif query == "/status":
                status = jarvis.get_status()
                print(json.dumps(status, indent=2, ensure_ascii=False))
                continue
            elif query == "/modules":
                modules = jarvis.list_modules()
                for name, info in modules.items():
                    print(f"\n{name} v{info['version']}")
                    print(f"  Capacités: {', '.join(info['capabilities'][:5])}...")
                continue
            elif query == "/history":
                history = jarvis.get_history(limit=5)
                for i, entry in enumerate(history, 1):
                    print(f"\n{i}. {entry['query']}")
                    print(f"   Succès: {entry['success']}")
                continue
            elif query == "/help":
                print(jarvis.help())
                continue

            # Requête normale
            response = jarvis.ask(query, validate=True)
            print_result(response)

        except KeyboardInterrupt:
            print("\n\nInterruption détectée. Utilisez /quit pour quitter proprement.")
        except Exception as e:
            print(f"\n❌ Erreur: {e}")


def main():
    """Fonction principale"""
    print_banner()

    # Initialiser Jarvis
    print("🚀 Initialisation de Jarvis...\n")
    jarvis = Jarvis()

    # Afficher le statut
    status = jarvis.get_status()
    print(f"✓ Jarvis initialisé")
    print(f"✓ {status['modules']['total_modules']} modules chargés")
    print(f"✓ {len(jarvis.get_capabilities())} capacités disponibles\n")

    # Menu principal
    while True:
        print("\n" + "="*60)
        print("MENU PRINCIPAL")
        print("="*60)
        print("\n1. Démonstration - Mathématiques")
        print("2. Démonstration - Physique")
        print("3. Démonstration - Électronique")
        print("4. Mode interactif")
        print("5. Test rapide")
        print("6. Statut du système")
        print("7. Quitter")
        print("\n" + "="*60)

        choice = input("\nChoisissez une option (1-7): ").strip()

        if choice == "1":
            demo_mathematics(jarvis)
        elif choice == "2":
            demo_physics(jarvis)
        elif choice == "3":
            demo_electronics(jarvis)
        elif choice == "4":
            interactive_mode(jarvis)
        elif choice == "5":
            print("\n🧪 Test rapide...")
            response = jarvis.ask("Résoudre 2x + 5 = 13")
            print_result(response)
        elif choice == "6":
            status = jarvis.get_status()
            print("\n" + json.dumps(status, indent=2, ensure_ascii=False))
        elif choice == "7":
            jarvis.shutdown()
            print("\n👋 Au revoir!")
            break
        else:
            print("\n❌ Option invalide")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Arrêt de Jarvis...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        sys.exit(1)
