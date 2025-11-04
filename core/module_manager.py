"""
Gestionnaire de modules pour Jarvis
Gère le chargement, l'activation et l'exécution des modules
"""

from typing import Dict, List, Optional, Any, Type
import importlib
import logging
from pathlib import Path
import json

from modules.base_module import BaseModule


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModuleManager:
    """Gestionnaire central pour tous les modules Jarvis"""

    def __init__(self):
        """Initialise le gestionnaire de modules"""
        self.modules: Dict[str, BaseModule] = {}
        self.module_configs: Dict[str, Dict] = {}
        self.initialization_order: List[str] = []

    def register_module(self, module: BaseModule, config: Optional[Dict] = None) -> bool:
        """
        Enregistre un nouveau module

        Args:
            module: Instance du module à enregistrer
            config: Configuration optionnelle du module

        Returns:
            True si l'enregistrement réussit
        """
        try:
            if module.name in self.modules:
                logger.warning(f"Module {module.name} déjà enregistré, remplacement...")

            # Initialiser le module
            if module.initialize():
                self.modules[module.name] = module
                self.module_configs[module.name] = config or {}
                self.initialization_order.append(module.name)
                logger.info(f"Module {module.name} v{module.version} enregistré avec succès")
                return True
            else:
                logger.error(f"Échec de l'initialisation du module {module.name}")
                return False

        except Exception as e:
            logger.error(f"Erreur lors de l'enregistrement du module {module.name}: {e}")
            return False

    def unregister_module(self, module_name: str) -> bool:
        """
        Désenregistre un module

        Args:
            module_name: Nom du module à désenregistrer

        Returns:
            True si le désenregistrement réussit
        """
        if module_name in self.modules:
            del self.modules[module_name]
            if module_name in self.module_configs:
                del self.module_configs[module_name]
            if module_name in self.initialization_order:
                self.initialization_order.remove(module_name)
            logger.info(f"Module {module_name} désenregistré")
            return True
        return False

    def get_module(self, module_name: str) -> Optional[BaseModule]:
        """
        Récupère un module par son nom

        Args:
            module_name: Nom du module

        Returns:
            Instance du module ou None
        """
        return self.modules.get(module_name)

    def get_all_modules(self) -> Dict[str, BaseModule]:
        """Retourne tous les modules enregistrés"""
        return self.modules.copy()

    def find_best_module(self, query: str) -> Optional[BaseModule]:
        """
        Trouve le meilleur module pour gérer une requête

        Args:
            query: La requête à traiter

        Returns:
            Le module le plus approprié ou None
        """
        best_module = None
        best_score = 0.0

        for module in self.modules.values():
            if not module.is_enabled():
                continue

            score = module.can_handle(query)
            if score > best_score:
                best_score = score
                best_module = module

        if best_score > 0.3:  # Seuil de confiance minimum
            logger.info(f"Module sélectionné: {best_module.name} (score: {best_score:.2f})")
            return best_module

        logger.warning(f"Aucun module approprié trouvé pour: {query}")
        return None

    def execute_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Exécute une requête en trouvant automatiquement le bon module

        Args:
            query: La requête à exécuter
            context: Contexte optionnel

        Returns:
            Dictionnaire avec les résultats
        """
        module = self.find_best_module(query)

        if module is None:
            return {
                "success": False,
                "error": "Aucun module approprié trouvé",
                "query": query
            }

        try:
            result = module.execute(query, context)
            result["module_used"] = module.name
            return result
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution sur {module.name}: {e}")
            return {
                "success": False,
                "error": str(e),
                "module_used": module.name,
                "query": query
            }

    def get_system_status(self) -> Dict[str, Any]:
        """
        Retourne le statut du système et de tous les modules

        Returns:
            Dictionnaire avec le statut complet
        """
        status = {
            "total_modules": len(self.modules),
            "enabled_modules": sum(1 for m in self.modules.values() if m.is_enabled()),
            "modules": {}
        }

        for name, module in self.modules.items():
            status["modules"][name] = module.get_info()

        return status

    def load_config(self, config_path: str) -> bool:
        """
        Charge la configuration depuis un fichier JSON

        Args:
            config_path: Chemin vers le fichier de configuration

        Returns:
            True si le chargement réussit
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # Traiter la configuration
            for module_name, module_config in config.get("modules", {}).items():
                if module_name in self.modules:
                    self.module_configs[module_name] = module_config
                    logger.info(f"Configuration chargée pour {module_name}")

            return True
        except Exception as e:
            logger.error(f"Erreur lors du chargement de la configuration: {e}")
            return False

    def get_available_capabilities(self) -> List[str]:
        """
        Retourne toutes les capacités disponibles dans le système

        Returns:
            Liste des capacités
        """
        capabilities = set()
        for module in self.modules.values():
            if module.is_enabled():
                capabilities.update(module.get_capabilities())
        return sorted(list(capabilities))
