"""
Enhanced Intent Detection System for NYX-V2
Détecte l'intention de l'utilisateur et route vers le bon module/action
"""

import re
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


class IntentCategory(Enum):
    """Catégories d'intentions principales"""
    QUERY = "query"                    # Question simple
    COMPUTE = "compute"                # Calcul numérique
    SOLVE = "solve"                    # Résolution d'équation
    VISUALIZE = "visualize"            # Visualisation/graphique
    SIMULATE = "simulate"              # Simulation interactive
    EXPLAIN = "explain"                # Explication de concept
    OPTIMIZE = "optimize"              # Optimisation
    ANALYZE = "analyze"                # Analyse de données
    DERIVE = "derive"                  # Dérivation
    INTEGRATE = "integrate"            # Intégration
    UNKNOWN = "unknown"                # Intent non reconnu


class DomainType(Enum):
    """Domaines scientifiques"""
    MATHEMATICS = "mathematics"
    PHYSICS = "physics"
    ELECTRONICS = "electronics"
    GENERAL = "general"


class ActionType(Enum):
    """Actions spécifiques par domaine"""
    # Mathematics
    PLOT_FUNCTION = "plot_function"
    PLOT_PARAMETRIC = "plot_parametric"
    PLOT_3D = "plot_3d"
    SOLVE_EQUATION = "solve_equation"
    COMPUTE_DERIVATIVE = "compute_derivative"
    COMPUTE_INTEGRAL = "compute_integral"
    COMPUTE_LIMIT = "compute_limit"
    COMPUTE_SERIES = "compute_series"

    # Physics
    SIMULATE_MOTION = "simulate_motion"
    SIMULATE_COLLISION = "simulate_collision"
    SIMULATE_WAVES = "simulate_waves"
    SIMULATE_PENDULUM = "simulate_pendulum"
    CALCULATE_ENERGY = "calculate_energy"
    CALCULATE_FORCE = "calculate_force"

    # Electronics
    SIMULATE_CIRCUIT = "simulate_circuit"
    ANALYZE_CIRCUIT = "analyze_circuit"
    DESIGN_CIRCUIT = "design_circuit"
    CALCULATE_RC = "calculate_rc"
    CALCULATE_RL = "calculate_rl"
    CALCULATE_RLC = "calculate_rlc"

    # General
    EXPLAIN = "explain"
    COMPUTE = "compute"


@dataclass
class Intent:
    """Représente une intention détectée"""
    category: IntentCategory
    domain: DomainType
    action: ActionType
    confidence: float
    parameters: Dict[str, Any]
    requires_sandbox: bool
    original_query: str


class IntentDetector:
    """Détecteur d'intentions avec patterns et règles"""

    def __init__(self):
        self.intent_patterns = self._build_intent_patterns()
        self.domain_keywords = self._build_domain_keywords()
        self.action_keywords = self._build_action_keywords()

    def _build_intent_patterns(self) -> Dict[IntentCategory, List[str]]:
        """Patterns regex pour chaque catégorie d'intent"""
        return {
            IntentCategory.VISUALIZE: [
                r'\b(trac(?:er|e)|plot|graph(?:e|ique)?|visualis(?:er|e)|dessine?r?|affiche?r?)\b',
                r'\bcourbe\b',
                r'\bdiagramme\b',
            ],
            IntentCategory.SIMULATE: [
                r'\b(simul(?:er|e|ation)|model(?:er|e)?|animer?)\b',
                r'\ben temps réel\b',
                r'\binteractif\b',
                r'\bbac à sable\b',
                r'\bsandbox\b',
            ],
            IntentCategory.SOLVE: [
                r'\b(résou(?:dre|s)|solve|trouve?r?)\b',
                r'\béquation\b',
                r'\bsolution\b',
            ],
            IntentCategory.DERIVE: [
                r'\b(dériv(?:ée?|er)|derivative|d/dx)\b',
            ],
            IntentCategory.INTEGRATE: [
                r'\b(intégr(?:ale?|er)|integral|∫)\b',
            ],
            IntentCategory.COMPUTE: [
                r'\b(calcul(?:er)?|calculate|compute|évalue?r?)\b',
            ],
            IntentCategory.EXPLAIN: [
                r'\b(expli(?:que|quer)|explain|qu\'?est[- ]ce|c\'?est quoi|comment)\b',
                r'\bpourquoi\b',
            ],
            IntentCategory.ANALYZE: [
                r'\b(analys(?:er|e)|analyze|étud(?:ier|e))\b',
            ],
            IntentCategory.OPTIMIZE: [
                r'\b(optimis(?:er|e)|optimize|minim(?:iser|um)|maxim(?:iser|um))\b',
            ],
        }

    def _build_domain_keywords(self) -> Dict[DomainType, Dict[str, float]]:
        """Keywords avec scores pour chaque domaine"""
        return {
            DomainType.MATHEMATICS: {
                'fonction': 0.9, 'function': 0.9, 'équation': 0.9, 'equation': 0.9,
                'dérivée': 0.95, 'derivative': 0.95, 'intégrale': 0.95, 'integral': 0.95,
                'courbe': 0.85, 'graphe': 0.85, 'graph': 0.85, 'plot': 0.85,
                'limite': 0.9, 'limit': 0.9, 'série': 0.9, 'series': 0.9,
                'matrice': 0.9, 'matrix': 0.9, 'algèbre': 0.85, 'algebra': 0.85,
                'sin': 0.7, 'cos': 0.7, 'tan': 0.7, 'exp': 0.7, 'log': 0.7,
                'polynôme': 0.85, 'polynomial': 0.85,
            },
            DomainType.PHYSICS: {
                'physique': 0.95, 'physics': 0.95, 'force': 0.9, 'énergie': 0.9, 'energy': 0.9,
                'vitesse': 0.85, 'velocity': 0.85, 'accélération': 0.85, 'acceleration': 0.85,
                'masse': 0.8, 'mass': 0.8, 'collision': 0.9, 'mouvement': 0.85, 'motion': 0.85,
                'pendule': 0.9, 'pendulum': 0.9, 'gravité': 0.85, 'gravity': 0.85,
                'projectile': 0.9, 'onde': 0.85, 'wave': 0.85, 'oscillation': 0.85,
                'mécanique': 0.9, 'mechanics': 0.9, 'cinétique': 0.85, 'kinetic': 0.85,
                'photon': 0.9, 'quantique': 0.95, 'quantum': 0.95,
            },
            DomainType.ELECTRONICS: {
                'circuit': 0.95, 'électrique': 0.9, 'electric': 0.9, 'électronique': 0.95,
                'résistance': 0.9, 'resistance': 0.9, 'résistor': 0.9, 'resistor': 0.9,
                'condensateur': 0.9, 'capacitor': 0.9, 'inductance': 0.9, 'inductor': 0.9,
                'voltage': 0.85, 'tension': 0.85, 'courant': 0.85, 'current': 0.85,
                'ampère': 0.8, 'ampere': 0.8, 'volt': 0.8, 'ohm': 0.85,
                'rc': 0.9, 'rl': 0.9, 'rlc': 0.95, 'transistor': 0.9,
                'diode': 0.9, 'led': 0.85, 'oscilloscope': 0.9,
            },
        }

    def _build_action_keywords(self) -> Dict[ActionType, Dict[str, float]]:
        """Keywords pour actions spécifiques"""
        return {
            # Math actions
            ActionType.PLOT_FUNCTION: {
                'tracer': 0.9, 'plot': 0.9, 'graphe': 0.9, 'courbe': 0.9,
                'dessiner': 0.85, 'visualiser': 0.85, 'afficher': 0.8,
            },
            ActionType.SOLVE_EQUATION: {
                'résoudre': 0.95, 'solve': 0.95, 'solution': 0.9, 'trouver': 0.85,
            },
            ActionType.COMPUTE_DERIVATIVE: {
                'dérivée': 0.95, 'derivative': 0.95, 'dériver': 0.9, 'd/dx': 0.95,
            },
            ActionType.COMPUTE_INTEGRAL: {
                'intégrale': 0.95, 'integral': 0.95, 'intégrer': 0.9, '∫': 0.95,
            },

            # Physics actions
            ActionType.SIMULATE_MOTION: {
                'mouvement': 0.9, 'motion': 0.9, 'déplacer': 0.85, 'move': 0.85,
            },
            ActionType.SIMULATE_COLLISION: {
                'collision': 0.95, 'choc': 0.9, 'impact': 0.85,
            },
            ActionType.SIMULATE_PENDULUM: {
                'pendule': 0.95, 'pendulum': 0.95, 'balancier': 0.9,
            },

            # Electronics actions
            ActionType.SIMULATE_CIRCUIT: {
                'circuit': 0.9, 'simuler': 0.85, 'simulate': 0.85,
            },
            ActionType.CALCULATE_RC: {
                'rc': 0.95, 'résistance-condensateur': 0.9,
            },
        }

    def detect(self, query: str, context: Optional[Dict[str, Any]] = None) -> Intent:
        """
        Détecte l'intention principale d'une requête

        Args:
            query: Requête utilisateur
            context: Contexte optionnel (historique, variables, etc.)

        Returns:
            Intent détecté avec tous les détails
        """
        query_lower = query.lower()

        # 1. Détecter la catégorie d'intent
        category, category_confidence = self._detect_category(query_lower)

        # 2. Détecter le domaine
        domain, domain_confidence = self._detect_domain(query_lower)

        # 3. Détecter l'action spécifique
        action, action_confidence = self._detect_action(query_lower, category, domain)

        # 4. Déterminer si sandbox requis
        requires_sandbox = self._requires_sandbox(category, action)

        # 5. Extraire les paramètres
        parameters = self._extract_parameters(query, category, domain, action, context)

        # Confidence globale (moyenne pondérée)
        overall_confidence = (
            category_confidence * 0.3 +
            domain_confidence * 0.4 +
            action_confidence * 0.3
        )

        intent = Intent(
            category=category,
            domain=domain,
            action=action,
            confidence=overall_confidence,
            parameters=parameters,
            requires_sandbox=requires_sandbox,
            original_query=query
        )

        logger.info(f"Intent detected: {category.value}/{domain.value}/{action.value} "
                   f"(confidence: {overall_confidence:.2f})")

        return intent

    def _detect_category(self, query: str) -> Tuple[IntentCategory, float]:
        """Détecte la catégorie d'intent"""
        best_category = IntentCategory.UNKNOWN
        best_score = 0.0

        for category, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query, re.IGNORECASE):
                    score = 0.9  # Score de base pour un match
                    if score > best_score:
                        best_score = score
                        best_category = category

        # Si pas de match, essayer de déduire depuis les mots-clés
        if best_category == IntentCategory.UNKNOWN:
            if any(word in query for word in ['calculer', 'calculate', 'compute', 'valeur']):
                return IntentCategory.COMPUTE, 0.6
            else:
                return IntentCategory.QUERY, 0.5

        return best_category, best_score

    def _detect_domain(self, query: str) -> Tuple[DomainType, float]:
        """Détecte le domaine scientifique"""
        scores = {domain: 0.0 for domain in DomainType}

        for domain, keywords in self.domain_keywords.items():
            for keyword, weight in keywords.items():
                if keyword in query:
                    scores[domain] += weight

        best_domain = max(scores, key=scores.get)
        best_score = scores[best_domain]

        # Normaliser le score
        if best_score > 0:
            best_score = min(best_score, 1.0)
        else:
            best_domain = DomainType.GENERAL
            best_score = 0.3

        return best_domain, best_score

    def _detect_action(self, query: str, category: IntentCategory,
                      domain: DomainType) -> Tuple[ActionType, float]:
        """Détecte l'action spécifique"""
        scores = {}

        for action, keywords in self.action_keywords.items():
            score = 0.0
            for keyword, weight in keywords.items():
                if keyword in query:
                    score += weight
            if score > 0:
                scores[action] = score

        if scores:
            best_action = max(scores, key=scores.get)
            best_score = min(scores[best_action], 1.0)
            return best_action, best_score

        # Actions par défaut selon catégorie + domaine
        default_actions = {
            (IntentCategory.VISUALIZE, DomainType.MATHEMATICS): ActionType.PLOT_FUNCTION,
            (IntentCategory.SOLVE, DomainType.MATHEMATICS): ActionType.SOLVE_EQUATION,
            (IntentCategory.DERIVE, DomainType.MATHEMATICS): ActionType.COMPUTE_DERIVATIVE,
            (IntentCategory.INTEGRATE, DomainType.MATHEMATICS): ActionType.COMPUTE_INTEGRAL,
            (IntentCategory.SIMULATE, DomainType.PHYSICS): ActionType.SIMULATE_MOTION,
            (IntentCategory.SIMULATE, DomainType.ELECTRONICS): ActionType.SIMULATE_CIRCUIT,
            (IntentCategory.COMPUTE, DomainType.ELECTRONICS): ActionType.CALCULATE_RC,
        }

        action = default_actions.get((category, domain), ActionType.COMPUTE)
        return action, 0.5

    def _requires_sandbox(self, category: IntentCategory, action: ActionType) -> bool:
        """Détermine si l'action requiert un sandbox interactif"""
        sandbox_categories = {
            IntentCategory.VISUALIZE,
            IntentCategory.SIMULATE,
        }

        sandbox_actions = {
            ActionType.PLOT_FUNCTION,
            ActionType.PLOT_PARAMETRIC,
            ActionType.PLOT_3D,
            ActionType.SIMULATE_MOTION,
            ActionType.SIMULATE_COLLISION,
            ActionType.SIMULATE_WAVES,
            ActionType.SIMULATE_PENDULUM,
            ActionType.SIMULATE_CIRCUIT,
            ActionType.DESIGN_CIRCUIT,
        }

        return category in sandbox_categories or action in sandbox_actions

    def _extract_parameters(self, query: str, category: IntentCategory,
                           domain: DomainType, action: ActionType,
                           context: Optional[Dict] = None) -> Dict[str, Any]:
        """Extrait les paramètres de la requête"""
        parameters = {}

        # Extraire les expressions mathématiques
        if domain == DomainType.MATHEMATICS:
            # Chercher des fonctions (f(x) = ..., y = ...)
            func_match = re.search(r'(?:f\(x\)|y)\s*=\s*(.+?)(?:\s+|$)', query, re.IGNORECASE)
            if func_match:
                parameters['function'] = func_match.group(1).strip()
            else:
                # Chercher "de <fonction>"
                func_match = re.search(r'de\s+(.+?)(?:\s+de\s+|\s+from\s+|$)', query, re.IGNORECASE)
                if func_match:
                    parameters['function'] = func_match.group(1).strip()

            # Extraire les bornes/intervalles
            bounds_match = re.search(r'(?:de|from)\s+(\S+)\s+(?:à|to)\s+(\S+)', query, re.IGNORECASE)
            if bounds_match:
                parameters['x_min'] = bounds_match.group(1)
                parameters['x_max'] = bounds_match.group(2)

            # Intervalle avec [...] ou (...)
            interval_match = re.search(r'[\[\(]([^,]+),\s*([^\]\)]+)[\]\)]', query)
            if interval_match:
                parameters['x_min'] = interval_match.group(1).strip()
                parameters['x_max'] = interval_match.group(2).strip()

        # Paramètres physiques
        if domain == DomainType.PHYSICS:
            # Masse
            mass_match = re.search(r'masse\s*(?:=|:)?\s*(\d+(?:\.\d+)?)\s*(kg|g)?', query, re.IGNORECASE)
            if mass_match:
                parameters['mass'] = float(mass_match.group(1))
                parameters['mass_unit'] = mass_match.group(2) or 'kg'

            # Vitesse
            velocity_match = re.search(r'vitesse\s*(?:=|:)?\s*(\d+(?:\.\d+)?)\s*(m/s)?', query, re.IGNORECASE)
            if velocity_match:
                parameters['velocity'] = float(velocity_match.group(1))

        # Paramètres électroniques
        if domain == DomainType.ELECTRONICS:
            # Résistance
            r_match = re.search(r'R\s*=\s*(\d+(?:\.\d+)?)\s*(Ω|ohm|k)?', query, re.IGNORECASE)
            if r_match:
                parameters['resistance'] = float(r_match.group(1))
                parameters['resistance_unit'] = r_match.group(2) or 'Ω'

            # Condensateur
            c_match = re.search(r'C\s*=\s*(\d+(?:\.\d+)?)\s*(F|µF|nF|pF)?', query, re.IGNORECASE)
            if c_match:
                parameters['capacitance'] = float(c_match.group(1))
                parameters['capacitance_unit'] = c_match.group(2) or 'F'

        # Contexte additionnel
        if context:
            parameters['context'] = context

        return parameters


class IntentRouter:
    """Route les intentions vers les modules appropriés"""

    def __init__(self, module_manager):
        self.module_manager = module_manager
        self.detector = IntentDetector()

    def route(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Route une requête vers le bon module et action

        Returns:
            Dict avec module, method, parameters, et metadata
        """
        # Détecter l'intent
        intent = self.detector.detect(query, context)

        # Mapper vers module
        module_name = self._get_module_name(intent.domain)

        # Mapper vers méthode
        method_name = self._get_method_name(intent.action, intent.category)

        return {
            'module': module_name,
            'method': method_name,
            'parameters': intent.parameters,
            'metadata': {
                'intent_category': intent.category.value,
                'domain': intent.domain.value,
                'action': intent.action.value,
                'confidence': intent.confidence,
                'requires_sandbox': intent.requires_sandbox,
            },
            'original_query': query,
        }

    def _get_module_name(self, domain: DomainType) -> str:
        """Mappe domaine vers nom de module"""
        mapping = {
            DomainType.MATHEMATICS: 'Mathematics',
            DomainType.PHYSICS: 'Physics',
            DomainType.ELECTRONICS: 'Electronics',
            DomainType.GENERAL: 'ScientificSolver',
        }
        return mapping.get(domain, 'ScientificSolver')

    def _get_method_name(self, action: ActionType, category: IntentCategory) -> str:
        """Mappe action vers nom de méthode"""
        # Pour l'instant, utiliser 'execute' générique
        # Les modules sandbox auront leurs propres méthodes
        return 'execute'
