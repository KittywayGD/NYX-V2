"""
NYX-V2 - Système principal
Assistant scientifique modulaire et récursif
"""

from typing import Dict, Any, Optional, List
import logging
import json
from pathlib import Path

from .module_manager import ModuleManager
from .recursive_validator import RecursiveValidator, ValidationStatus
from modules.scientific.solver import ScientificSolver
from modules.scientific.mathematics import MathematicsModule
from modules.scientific.physics import PhysicsModule
from modules.scientific.electronics import ElectronicsModule


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Nyx:
    """
    Système Nyx - Assistant scientifique modulaire et récursif
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialise le système Nyx

        Args:
            config_path: Chemin vers le fichier de configuration (optionnel)
        """
        logger.info("=" * 60)
        logger.info("Initialisation de NYX-V2")
        logger.info("=" * 60)

        # Composants principaux
        self.module_manager = ModuleManager()
        self.validator = RecursiveValidator(max_iterations=3, min_confidence=0.85)

        # État du système
        self.initialized = False
        self.config = {}
        self.query_history: List[Dict] = []

        # Charger la configuration si fournie
        if config_path:
            self._load_config(config_path)

        # Initialiser les modules par défaut
        self._initialize_default_modules()

    def _load_config(self, config_path: str):
        """Charge la configuration depuis un fichier"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            logger.info(f"Configuration chargée depuis {config_path}")
        except Exception as e:
            logger.warning(f"Impossible de charger la configuration: {e}")
            self.config = {}

    def _initialize_default_modules(self):
        """Initialise les modules scientifiques par défaut"""
        logger.info("Chargement des modules scientifiques...")

        # Module scientifique unifié (recommandé)
        scientific_solver = ScientificSolver()
        self.module_manager.register_module(scientific_solver)

        # Modules individuels (optionnels, pour usage direct)
        math_module = MathematicsModule()
        physics_module = PhysicsModule()
        electronics_module = ElectronicsModule()

        self.module_manager.register_module(math_module)
        self.module_manager.register_module(physics_module)
        self.module_manager.register_module(electronics_module)

        self.initialized = True
        logger.info("✓ Tous les modules chargés avec succès")

    def ask(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        validate: bool = True,
        module: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Pose une question à Nyx

        Args:
            query: Question ou requête
            context: Contexte optionnel avec paramètres
            validate: Active la validation récursive (True par défaut)
            module: Force l'utilisation d'un module spécifique (optionnel)

        Returns:
            Réponse complète avec résultats et validation
        """
        if not self.initialized:
            return {
                "success": False,
                "error": "Nyx n'est pas initialisé"
            }

        logger.info(f"\n{'='*60}")
        logger.info(f"Nouvelle requête: {query}")
        logger.info(f"{'='*60}")

        try:
            # Exécuter la requête
            if module:
                # Utiliser un module spécifique
                specific_module = self.module_manager.get_module(module)
                if specific_module:
                    result = specific_module.execute(query, context)
                else:
                    return {
                        "success": False,
                        "error": f"Module '{module}' non trouvé"
                    }
            else:
                # Laisser le gestionnaire choisir le meilleur module
                result = self.module_manager.execute_query(query, context)

            response = {
                "query": query,
                "result": result,
                "context": context,
                "success": result.get("success", True)
            }

            # Validation récursive si demandée
            if validate and result.get("success", True):
                logger.info("Démarrage de la validation récursive...")

                # Fonction de validation
                def validator_func(res):
                    module_used = result.get("module_used")
                    if module_used:
                        mod = self.module_manager.get_module(module_used)
                        if mod:
                            return mod.validate_result(res, query)
                    return {"is_valid": True, "confidence": 0.7, "errors": []}

                # Exécuter la validation
                validation_result = self.validator.validate(
                    result,
                    query,
                    validator_func
                )

                response["validation"] = {
                    "status": validation_result.status.value,
                    "confidence": validation_result.confidence,
                    "iterations": validation_result.iterations,
                    "errors": validation_result.errors
                }

                logger.info(f"Validation: {validation_result.status.value} (confiance: {validation_result.confidence:.2f})")

            # Ajouter à l'historique
            self.query_history.append(response)

            return response

        except Exception as e:
            logger.error(f"Erreur lors du traitement de la requête: {e}")
            return {
                "success": False,
                "error": str(e),
                "query": query
            }

    def solve(
        self,
        problem: str,
        parameters: Optional[Dict[str, Any]] = None,
        validate: bool = True
    ) -> Dict[str, Any]:
        """
        Résout un problème scientifique complet

        Args:
            problem: Énoncé du problème
            parameters: Paramètres du problème
            validate: Active la validation récursive

        Returns:
            Solution complète
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Résolution de problème scientifique")
        logger.info(f"{'='*60}")

        # Utiliser le ScientificSolver
        solver = self.module_manager.get_module("ScientificSolver")

        if not solver:
            return {
                "success": False,
                "error": "ScientificSolver non disponible"
            }

        return self.ask(problem, parameters, validate, module="ScientificSolver")

    def get_status(self) -> Dict[str, Any]:
        """
        Retourne le statut complet du système

        Returns:
            Statut de Nyx et de tous les modules
        """
        status = {
            "nyx": {
                "initialized": self.initialized,
                "version": "1.0.0",
                "queries_processed": len(self.query_history)
            },
            "modules": self.module_manager.get_system_status(),
            "validator": self.validator.get_statistics(),
            "capabilities": self.get_capabilities()
        }

        return status

    def get_capabilities(self) -> List[str]:
        """
        Retourne toutes les capacités disponibles

        Returns:
            Liste des capacités
        """
        return self.module_manager.get_available_capabilities()

    def get_history(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Retourne l'historique des requêtes

        Args:
            limit: Nombre maximum de requêtes à retourner

        Returns:
            Historique des requêtes
        """
        if limit:
            return self.query_history[-limit:]
        return self.query_history

    def clear_history(self):
        """Efface l'historique des requêtes"""
        self.query_history.clear()
        logger.info("Historique effacé")

    def list_modules(self) -> Dict[str, Dict[str, Any]]:
        """
        Liste tous les modules disponibles

        Returns:
            Informations sur tous les modules
        """
        modules_info = {}
        all_modules = self.module_manager.get_all_modules()

        for name, module in all_modules.items():
            modules_info[name] = module.get_info()

        return modules_info

    def module_info(self, module_name: str) -> Optional[Dict[str, Any]]:
        """
        Retourne les informations détaillées sur un module

        Args:
            module_name: Nom du module

        Returns:
            Informations du module
        """
        module = self.module_manager.get_module(module_name)
        if module:
            return module.get_info()
        return None

    def help(self, topic: Optional[str] = None) -> str:
        """
        Affiche l'aide

        Args:
            topic: Sujet d'aide spécifique (optionnel)

        Returns:
            Texte d'aide
        """
        if topic is None:
            return """
NYX-V2 - Assistant Scientifique Modulaire et Récursif

UTILISATION:
    nyx.ask(query, context=None, validate=True)
        - Pose une question générale
        - validate: Active la vérification récursive des résultats

    nyx.solve(problem, parameters=None, validate=True)
        - Résout un problème scientifique complexe
        - parameters: Dictionnaire avec les valeurs numériques

MODULES DISPONIBLES:
    - Mathematics: Calculs mathématiques avancés
    - Physics: Physique extrême (quantique, relativité, etc.)
    - Electronics: Circuits et composants électroniques
    - ScientificSolver: Résolution unifiée multi-domaines

COMMANDES SYSTÈME:
    nyx.get_status()      - Statut du système
    nyx.list_modules()    - Liste des modules
    nyx.get_capabilities() - Capacités disponibles
    nyx.get_history()     - Historique des requêtes
    nyx.help(topic)       - Aide (ce message)

EXEMPLES:
    nyx.ask("Résoudre x² - 4 = 0")
    nyx.ask("Calculer l'énergie d'un photon", context={"frequency": 5e14})
    nyx.solve("Circuit RC", parameters={"resistance": 1000, "capacitance": 1e-6})
            """
        elif topic == "mathematics":
            return "Module Mathematics: équations, dérivées, intégrales, matrices, limites, séries..."
        elif topic == "physics":
            return "Module Physics: mécanique quantique, relativité, thermodynamique, électromagnétisme..."
        elif topic == "electronics":
            return "Module Electronics: loi d'Ohm, circuits RC/RL/RLC, filtres, amplificateurs..."
        else:
            return f"Aucune aide disponible pour '{topic}'"

    def shutdown(self):
        """Arrêt propre du système"""
        logger.info("Arrêt de Nyx...")
        self.initialized = False
        logger.info("✓ Nyx arrêté")

    def __repr__(self) -> str:
        """Représentation string de Nyx"""
        status = "✓ Actif" if self.initialized else "✗ Inactif"
        modules_count = len(self.module_manager.get_all_modules())
        return f"<Nyx {status} | {modules_count} modules | {len(self.query_history)} requêtes>"
