"""
Moteur de résolution scientifique unifié
Coordonne les modules Math, Physique et Électronique
"""

from typing import Dict, Any, Optional, List
import logging

from modules.base_module import BaseModule
from .mathematics import MathematicsModule
from .physics import PhysicsModule
from .electronics import ElectronicsModule


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScientificSolver(BaseModule):
    """
    Moteur de résolution scientifique qui coordonne
    les modules mathématiques, physiques et électroniques
    """

    def __init__(self):
        super().__init__("ScientificSolver", "1.0.0")
        self.capabilities = [
            "scientific_problem_solving",
            "multi_domain_analysis",
            "integrated_calculations"
        ]
        self.metadata = {
            "description": "Moteur unifié pour problèmes scientifiques complexes",
            "modules": ["Mathematics", "Physics", "Electronics"]
        }

        # Initialiser les sous-modules
        self.math_module = MathematicsModule()
        self.physics_module = PhysicsModule()
        self.electronics_module = ElectronicsModule()

        self.sub_modules = {
            "mathematics": self.math_module,
            "physics": self.physics_module,
            "electronics": self.electronics_module
        }

    def initialize(self) -> bool:
        """Initialise le solver et tous les sous-modules"""
        try:
            logger.info("Initialisation du ScientificSolver...")

            # Initialiser tous les sous-modules
            for name, module in self.sub_modules.items():
                if not module.initialize():
                    logger.error(f"Échec initialisation {name}")
                    return False
                logger.info(f"✓ {name} initialisé")

            logger.info("✓ ScientificSolver initialisé")
            return True

        except Exception as e:
            logger.error(f"Erreur initialisation ScientificSolver: {e}")
            return False

    def execute(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Résout un problème scientifique en utilisant les modules appropriés

        Args:
            query: Requête scientifique
            context: Contexte avec paramètres

        Returns:
            Résultats de la résolution
        """
        logger.info(f"ScientificSolver - Requête: {query}")

        try:
            # Analyser la requête pour déterminer quels modules utiliser
            analysis = self._analyze_query(query)
            logger.info(f"Analyse: domaines={analysis['domains']}, complexité={analysis['complexity']}")

            results = {
                "query": query,
                "analysis": analysis,
                "module_results": {},
                "success": True
            }

            # Si mono-domaine, utiliser directement le module approprié
            if len(analysis['domains']) == 1:
                domain = analysis['domains'][0]
                module = self.sub_modules.get(domain)

                if module:
                    result = module.execute(query, context)
                    results["module_results"][domain] = result
                    results["primary_result"] = result
                else:
                    results["success"] = False
                    results["error"] = f"Module {domain} non trouvé"

            # Si multi-domaines, coordonner plusieurs modules
            else:
                for domain in analysis['domains']:
                    module = self.sub_modules.get(domain)
                    if module:
                        try:
                            result = module.execute(query, context)
                            results["module_results"][domain] = result
                        except Exception as e:
                            logger.error(f"Erreur module {domain}: {e}")
                            results["module_results"][domain] = {"error": str(e)}

                # Fusionner les résultats
                results["integrated_result"] = self._integrate_results(
                    results["module_results"],
                    query
                )

            return results

        except Exception as e:
            logger.error(f"Erreur ScientificSolver: {e}")
            return {
                "success": False,
                "error": str(e),
                "query": query
            }

    def _analyze_query(self, query: str) -> Dict[str, Any]:
        """
        Analyse une requête pour déterminer les domaines impliqués

        Args:
            query: Requête à analyser

        Returns:
            Analyse de la requête
        """
        query_lower = query.lower()
        domains = []
        keywords = []

        # Mots-clés mathématiques
        math_keywords = [
            "solve", "résoudre", "équation", "equation", "dérivée", "derivative",
            "intégrale", "integral", "limite", "limit", "matrice", "matrix",
            "série", "series", "optimize", "optimiser"
        ]

        # Mots-clés physiques
        physics_keywords = [
            "force", "energy", "énergie", "momentum", "velocity", "vitesse",
            "temperature", "température", "quantum", "quantique", "relativité",
            "relativity", "photon", "electron", "mass", "masse", "gravity"
        ]

        # Mots-clés électroniques
        electronics_keywords = [
            "circuit", "resistance", "résistance", "voltage", "tension",
            "current", "courant", "capacitor", "condensateur", "inductor",
            "transistor", "amplifier", "filter", "filtre", "impedance"
        ]

        # Vérifier chaque domaine
        if any(keyword in query_lower for keyword in math_keywords):
            domains.append("mathematics")
            keywords.extend([kw for kw in math_keywords if kw in query_lower])

        if any(keyword in query_lower for keyword in physics_keywords):
            domains.append("physics")
            keywords.extend([kw for kw in physics_keywords if kw in query_lower])

        if any(keyword in query_lower for keyword in electronics_keywords):
            domains.append("electronics")
            keywords.extend([kw for kw in electronics_keywords if kw in query_lower])

        # Si aucun domaine détecté, essayer tous
        if not domains:
            domains = ["mathematics", "physics", "electronics"]

        # Déterminer la complexité
        complexity = "simple"
        if len(domains) > 1:
            complexity = "complex"
        elif len(query.split()) > 20:
            complexity = "moderate"

        return {
            "domains": domains,
            "keywords": keywords,
            "complexity": complexity,
            "multi_domain": len(domains) > 1
        }

    def _integrate_results(self, module_results: Dict[str, Any], query: str) -> Dict[str, Any]:
        """
        Intègre les résultats de plusieurs modules

        Args:
            module_results: Résultats de chaque module
            query: Requête originale

        Returns:
            Résultats intégrés
        """
        integrated = {
            "combined_results": {},
            "summary": [],
            "all_successful": True
        }

        for module_name, result in module_results.items():
            if isinstance(result, dict):
                if result.get("success", True):
                    integrated["combined_results"][module_name] = result.get("result", result)
                    integrated["summary"].append(f"{module_name}: OK")
                else:
                    integrated["all_successful"] = False
                    integrated["summary"].append(f"{module_name}: ERREUR")

        return integrated

    def solve_problem(
        self,
        problem_statement: str,
        parameters: Optional[Dict[str, Any]] = None,
        preferred_module: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Résout un problème scientifique complet

        Args:
            problem_statement: Énoncé du problème
            parameters: Paramètres du problème
            preferred_module: Module préféré (optionnel)

        Returns:
            Solution complète
        """
        logger.info(f"Résolution de problème: {problem_statement}")

        context = parameters or {}

        if preferred_module and preferred_module in self.sub_modules:
            # Utiliser directement le module spécifié
            module = self.sub_modules[preferred_module]
            result = module.execute(problem_statement, context)

            return {
                "problem": problem_statement,
                "solution": result,
                "module_used": preferred_module,
                "parameters": parameters
            }
        else:
            # Laisser le solver choisir
            return self.execute(problem_statement, context)

    def get_module_capabilities(self) -> Dict[str, List[str]]:
        """
        Retourne les capacités de tous les modules

        Returns:
            Dictionnaire des capacités par module
        """
        capabilities = {}

        for name, module in self.sub_modules.items():
            capabilities[name] = module.get_capabilities()

        return capabilities

    def validate_result(self, result: Any, original_query: str) -> Dict[str, Any]:
        """
        Valide un résultat du solver

        Args:
            result: Résultat à valider
            original_query: Requête originale

        Returns:
            Validation
        """
        try:
            is_valid = True
            errors = []
            confidence = 0.9

            if isinstance(result, dict):
                if not result.get("success", True):
                    is_valid = False
                    if "error" in result:
                        errors.append(result["error"])
                    confidence = 0.0
                elif "module_results" in result:
                    # Valider chaque résultat de module
                    for module_name, module_result in result.get("module_results", {}).items():
                        module = self.sub_modules.get(module_name)
                        if module:
                            validation = module.validate_result(module_result, original_query)
                            if not validation.get("is_valid", True):
                                is_valid = False
                                errors.extend(validation.get("errors", []))
                            confidence = min(confidence, validation.get("confidence", 0.5))

            return {
                "is_valid": is_valid,
                "confidence": confidence,
                "errors": errors,
                "validation_method": "multi_module"
            }

        except Exception as e:
            return {
                "is_valid": False,
                "confidence": 0.0,
                "errors": [str(e)]
            }

    def get_available_modules(self) -> List[str]:
        """Retourne la liste des modules disponibles"""
        return list(self.sub_modules.keys())

    def module_info(self, module_name: str) -> Optional[Dict[str, Any]]:
        """
        Retourne les informations sur un module spécifique

        Args:
            module_name: Nom du module

        Returns:
            Informations du module
        """
        module = self.sub_modules.get(module_name)
        if module:
            return module.get_info()
        return None
