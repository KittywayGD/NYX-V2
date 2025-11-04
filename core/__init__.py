"""
NYX-V2 Jarvis - Core System
Un système d'IA modulaire et récursif pour l'assistance scientifique avancée
"""

__version__ = "0.1.0"
__author__ = "NYX-V2"

from .jarvis import Jarvis
from .module_manager import ModuleManager
from .recursive_validator import RecursiveValidator

__all__ = ["Jarvis", "ModuleManager", "RecursiveValidator"]
