"""
Classe de base pour tous les modules Nyx
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import json


class BaseModule(ABC):
    """Classe de base abstraite pour tous les modules Nyx"""

    def __init__(self, name: str, version: str = "1.0.0"):
        """
        Initialise un module

        Args:
            name: Nom du module
            version: Version du module
        """
        self.name = name
        self.version = version
        self.enabled = True
        self.capabilities: List[str] = []
        self.metadata: Dict[str, Any] = {}

    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialise le module et ses dépendances

        Returns:
            True si l'initialisation réussit, False sinon
        """
        pass

    @abstractmethod
    def execute(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Exécute une requête sur le module

        Args:
            query: La requête à exécuter
            context: Contexte optionnel pour la requête

        Returns:
            Dictionnaire contenant les résultats
        """
        pass

    @abstractmethod
    def validate_result(self, result: Any, original_query: str) -> Dict[str, Any]:
        """
        Valide un résultat produit par le module

        Args:
            result: Le résultat à valider
            original_query: La requête originale

        Returns:
            Dictionnaire avec validation status et détails
        """
        pass

    def get_capabilities(self) -> List[str]:
        """Retourne la liste des capacités du module"""
        return self.capabilities

    def get_info(self) -> Dict[str, Any]:
        """Retourne les informations sur le module"""
        return {
            "name": self.name,
            "version": self.version,
            "enabled": self.enabled,
            "capabilities": self.capabilities,
            "metadata": self.metadata
        }

    def enable(self):
        """Active le module"""
        self.enabled = True

    def disable(self):
        """Désactive le module"""
        self.enabled = False

    def is_enabled(self) -> bool:
        """Vérifie si le module est activé"""
        return self.enabled

    def can_handle(self, query: str) -> float:
        """
        Détermine si ce module peut gérer une requête

        Args:
            query: La requête à évaluer

        Returns:
            Score de confiance entre 0 et 1
        """
        # Implémentation par défaut basique
        query_lower = query.lower()
        score = 0.0

        for capability in self.capabilities:
            if capability.lower() in query_lower:
                score += 0.3

        return min(score, 1.0)
