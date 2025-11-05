"""
Module d'électronique pour Nyx
Circuits, composants, analyse de signaux, filtres, etc.
"""

import numpy as np
import sympy as sp
from sympy import symbols, sqrt, pi, I, exp, sin, cos, atan, log
from typing import Dict, Any, Optional, List, Union
import logging

from modules.base_module import BaseModule


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ElectronicsModule(BaseModule):
    """Module d'électronique avancée"""

    def __init__(self):
        super().__init__("Electronics", "1.0.0")
        self.capabilities = [
            "ohms_law", "circuit_analysis", "filters", "amplifiers",
            "transistors", "operational_amplifiers", "digital_logic",
            "signal_processing", "impedance", "resonance", "power_electronics",
            "ac_dc_analysis", "frequency_response", "bode_plots"
        ]
        self.metadata = {
            "description": "Module d'électronique avec analyse de circuits et composants",
            "supported_components": ["resistor", "capacitor", "inductor", "diode", "transistor", "op-amp"]
        }

    def initialize(self) -> bool:
        """Initialise le module"""
        try:
            logger.info("Initialisation du module Electronics...")
            logger.info("✓ Module Electronics initialisé")
            return True
        except Exception as e:
            logger.error(f"Erreur initialisation Electronics: {e}")
            return False

    def can_handle(self, query: str) -> float:
        """Détermine si ce module peut gérer une requête électronique"""
        query_lower = query.lower()
        score = 0.0

        # Mots-clés français et anglais pour l'électronique
        electronics_keywords = {
            'circuit': 0.9, 'résistance': 0.9, 'resistance': 0.9,
            'voltage': 0.9, 'tension': 0.9, 'volt': 0.9,
            'courant': 0.9, 'current': 0.9, 'ampere': 0.9, 'ampère': 0.9,
            'ohm': 0.9, 'condensateur': 0.9, 'capacitor': 0.9, 'capacitance': 0.9,
            'inducteur': 0.9, 'inductor': 0.9, 'inductance': 0.9,
            'transistor': 0.95, 'diode': 0.95,
            'amplificateur': 0.9, 'amplifier': 0.9, 'op-amp': 0.95,
            'filtre': 0.9, 'filter': 0.9,
            'impédance': 0.9, 'impedance': 0.9,
            'résonance': 0.9, 'resonance': 0.9,
            'puissance': 0.7, 'power': 0.7, 'watt': 0.8,
            'fréquence': 0.7, 'frequency': 0.7,
        }

        # Vérifier les mots-clés
        for keyword, weight in electronics_keywords.items():
            if keyword in query_lower:
                score = max(score, weight)

        # Composants électroniques spécifiques
        components = ['rc', 'rl', 'rlc', 'bjt', 'fet', 'mosfet']
        for comp in components:
            if comp in query_lower:
                score = max(score, 0.9)

        return min(score, 1.0)

    def execute(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Exécute une requête électronique

        Args:
            query: Requête électronique
            context: Contexte avec paramètres de circuit

        Returns:
            Résultats du calcul
        """
        logger.info(f"Exécution requête électronique: {query}")

        try:
            # Déterminer le type de calcul
            calc_type = self._detect_calculation_type(query)
            logger.info(f"Type de calcul détecté: {calc_type}")

            # Router vers la bonne méthode
            if calc_type == "ohms_law":
                result = self._ohms_law(query, context)
            elif calc_type == "power":
                result = self._power_calculation(query, context)
            elif calc_type == "rc_circuit":
                result = self._rc_circuit(query, context)
            elif calc_type == "rl_circuit":
                result = self._rl_circuit(query, context)
            elif calc_type == "rlc_circuit":
                result = self._rlc_circuit(query, context)
            elif calc_type == "filter":
                result = self._filter_design(query, context)
            elif calc_type == "impedance":
                result = self._impedance_calculation(query, context)
            elif calc_type == "op_amp":
                result = self._op_amp_circuit(query, context)
            elif calc_type == "divider":
                result = self._voltage_divider(query, context)
            elif calc_type == "resonance":
                result = self._resonance_calculation(query, context)
            elif calc_type == "transistor":
                result = self._transistor_analysis(query, context)
            else:
                result = self._general_electronics(query, context)

            return {
                "success": True,
                "result": result,
                "calculation_type": calc_type,
                "query": query
            }

        except Exception as e:
            logger.error(f"Erreur lors de l'exécution électronique: {e}")
            return {
                "success": False,
                "error": str(e),
                "query": query
            }

    def _detect_calculation_type(self, query: str) -> str:
        """Détecte le type de calcul électronique"""
        query_lower = query.lower()

        if any(word in query_lower for word in ["ohm", "resistance", "résistance", "voltage", "current"]):
            if "divider" in query_lower or "diviseur" in query_lower:
                return "divider"
            return "ohms_law"
        elif any(word in query_lower for word in ["power", "puissance", "watt"]):
            return "power"
        elif "rc" in query_lower and "circuit" in query_lower:
            return "rc_circuit"
        elif "rl" in query_lower and "circuit" in query_lower:
            return "rl_circuit"
        elif "rlc" in query_lower or "resonance" in query_lower or "résonance" in query_lower:
            return "rlc_circuit"
        elif any(word in query_lower for word in ["filter", "filtre", "low pass", "high pass", "band pass"]):
            return "filter"
        elif any(word in query_lower for word in ["impedance", "impédance", "reactance"]):
            return "impedance"
        elif any(word in query_lower for word in ["op-amp", "op amp", "operational amplifier", "amplificateur"]):
            return "op_amp"
        elif "resonance" in query_lower or "résonance" in query_lower:
            return "resonance"
        elif any(word in query_lower for word in ["transistor", "bjt", "fet", "mosfet"]):
            return "transistor"
        else:
            return "general"

    def _ohms_law(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Calculs de la loi d'Ohm: V = IR"""
        if not context:
            return {"formula": "V = I × R", "description": "Loi d'Ohm"}

        # V = IR, donc on peut calculer n'importe quelle variable
        if "voltage" in context and "current" in context:
            V = context["voltage"]
            I = context["current"]
            R = V / I

            return {
                "resistance": R,
                "voltage": V,
                "current": I,
                "formula": "R = V/I",
                "units": {"R": "Ohms", "V": "Volts", "I": "Amperes"}
            }
        elif "voltage" in context and "resistance" in context:
            V = context["voltage"]
            R = context["resistance"]
            I = V / R

            return {
                "current": I,
                "voltage": V,
                "resistance": R,
                "formula": "I = V/R",
                "units": {"I": "Amperes", "V": "Volts", "R": "Ohms"}
            }
        elif "current" in context and "resistance" in context:
            I = context["current"]
            R = context["resistance"]
            V = I * R

            return {
                "voltage": V,
                "current": I,
                "resistance": R,
                "formula": "V = I × R",
                "units": {"V": "Volts", "I": "Amperes", "R": "Ohms"}
            }

        return {"error": "Insufficient parameters for Ohm's law"}

    def _power_calculation(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Calculs de puissance électrique"""
        if not context:
            return {
                "formulas": ["P = V × I", "P = I² × R", "P = V²/R"],
                "description": "Calculs de puissance électrique"
            }

        # P = VI = I²R = V²/R
        if "voltage" in context and "current" in context:
            V = context["voltage"]
            I = context["current"]
            P = V * I

            return {
                "power": P,
                "voltage": V,
                "current": I,
                "formula": "P = V × I",
                "units": "Watts"
            }
        elif "current" in context and "resistance" in context:
            I = context["current"]
            R = context["resistance"]
            P = I**2 * R

            return {
                "power": P,
                "current": I,
                "resistance": R,
                "formula": "P = I² × R",
                "units": "Watts"
            }
        elif "voltage" in context and "resistance" in context:
            V = context["voltage"]
            R = context["resistance"]
            P = V**2 / R

            return {
                "power": P,
                "voltage": V,
                "resistance": R,
                "formula": "P = V²/R",
                "units": "Watts"
            }

        return {"error": "Insufficient parameters for power calculation"}

    def _rc_circuit(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Analyse de circuits RC"""
        if not context or not all(k in context for k in ['resistance', 'capacitance']):
            return {"error": "Need resistance and capacitance values"}

        R = context['resistance']
        C = context['capacitance']

        # Constante de temps
        tau = R * C

        # Fréquence de coupure
        f_c = 1 / (2 * np.pi * tau)

        # Pulsation de coupure
        omega_c = 1 / tau

        return {
            "time_constant": tau,
            "cutoff_frequency": f_c,
            "angular_frequency": omega_c,
            "resistance": R,
            "capacitance": C,
            "formulas": {
                "tau": "τ = R × C",
                "f_c": "f_c = 1/(2π × τ)"
            },
            "units": {
                "tau": "seconds",
                "f_c": "Hertz",
                "omega_c": "rad/s"
            }
        }

    def _rl_circuit(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Analyse de circuits RL"""
        if not context or not all(k in context for k in ['resistance', 'inductance']):
            return {"error": "Need resistance and inductance values"}

        R = context['resistance']
        L = context['inductance']

        # Constante de temps
        tau = L / R

        # Fréquence de coupure
        f_c = R / (2 * np.pi * L)

        return {
            "time_constant": tau,
            "cutoff_frequency": f_c,
            "resistance": R,
            "inductance": L,
            "formulas": {
                "tau": "τ = L/R",
                "f_c": "f_c = R/(2πL)"
            },
            "units": {
                "tau": "seconds",
                "f_c": "Hertz"
            }
        }

    def _rlc_circuit(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Analyse de circuits RLC"""
        if not context or not all(k in context for k in ['resistance', 'inductance', 'capacitance']):
            return {"error": "Need R, L, and C values"}

        R = context['resistance']
        L = context['inductance']
        C = context['capacitance']

        # Fréquence de résonance
        f_0 = 1 / (2 * np.pi * np.sqrt(L * C))
        omega_0 = 1 / np.sqrt(L * C)

        # Facteur de qualité
        Q = omega_0 * L / R

        # Coefficient d'amortissement
        zeta = R / (2 * np.sqrt(L / C))

        # Type d'amortissement
        if zeta < 1:
            damping_type = "sous-amorti (oscillant)"
        elif zeta == 1:
            damping_type = "critique"
        else:
            damping_type = "sur-amorti"

        return {
            "resonance_frequency": f_0,
            "angular_frequency": omega_0,
            "quality_factor": Q,
            "damping_ratio": zeta,
            "damping_type": damping_type,
            "resistance": R,
            "inductance": L,
            "capacitance": C,
            "formulas": {
                "f_0": "f₀ = 1/(2π√(LC))",
                "Q": "Q = ω₀L/R",
                "ζ": "ζ = R/(2√(L/C))"
            }
        }

    def _filter_design(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Design de filtres"""
        query_lower = query.lower()

        if "low pass" in query_lower or "passe-bas" in query_lower:
            filter_type = "low_pass"
        elif "high pass" in query_lower or "passe-haut" in query_lower:
            filter_type = "high_pass"
        elif "band pass" in query_lower or "passe-bande" in query_lower:
            filter_type = "band_pass"
        else:
            filter_type = "unknown"

        if not context or "cutoff_frequency" not in context:
            return {
                "filter_type": filter_type,
                "description": "Besoin de la fréquence de coupure"
            }

        f_c = context["cutoff_frequency"]

        if filter_type == "low_pass":
            # Filtre RC passe-bas simple
            if "resistance" in context:
                R = context["resistance"]
                C = 1 / (2 * np.pi * f_c * R)

                return {
                    "filter_type": "RC Low-Pass",
                    "cutoff_frequency": f_c,
                    "resistance": R,
                    "capacitance": C,
                    "formula": "C = 1/(2πf_cR)",
                    "transfer_function": "H(jω) = 1/(1 + jωRC)"
                }

        elif filter_type == "high_pass":
            # Filtre RC passe-haut simple
            if "resistance" in context:
                R = context["resistance"]
                C = 1 / (2 * np.pi * f_c * R)

                return {
                    "filter_type": "RC High-Pass",
                    "cutoff_frequency": f_c,
                    "resistance": R,
                    "capacitance": C,
                    "formula": "C = 1/(2πf_cR)",
                    "transfer_function": "H(jω) = jωRC/(1 + jωRC)"
                }

        return {"filter_type": filter_type, "cutoff_frequency": f_c}

    def _impedance_calculation(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Calculs d'impédance"""
        if not context or "frequency" not in context:
            return {"error": "Need frequency for impedance calculation"}

        f = context["frequency"]
        omega = 2 * np.pi * f

        results = {
            "frequency": f,
            "angular_frequency": omega,
            "impedances": {}
        }

        # Résistance
        if "resistance" in context:
            R = context["resistance"]
            results["impedances"]["resistor"] = {
                "value": R,
                "impedance": R,
                "formula": "Z_R = R"
            }

        # Capacitance
        if "capacitance" in context:
            C = context["capacitance"]
            X_C = 1 / (omega * C)
            results["impedances"]["capacitor"] = {
                "value": C,
                "reactance": X_C,
                "impedance": f"-j{X_C}",
                "formula": "Z_C = -j/(ωC)"
            }

        # Inductance
        if "inductance" in context:
            L = context["inductance"]
            X_L = omega * L
            results["impedances"]["inductor"] = {
                "value": L,
                "reactance": X_L,
                "impedance": f"j{X_L}",
                "formula": "Z_L = jωL"
            }

        return results

    def _op_amp_circuit(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Analyse de circuits à amplificateur opérationnel"""
        query_lower = query.lower()

        if "inverting" in query_lower or "inverseur" in query_lower:
            if context and all(k in context for k in ['R1', 'R2']):
                R1 = context['R1']
                R2 = context['R2']
                gain = -R2 / R1

                return {
                    "amplifier_type": "Inverting",
                    "gain": gain,
                    "R1": R1,
                    "R2": R2,
                    "formula": "A_v = -R2/R1",
                    "output": "V_out = -V_in × (R2/R1)"
                }

        elif "non-inverting" in query_lower or "non inverseur" in query_lower:
            if context and all(k in context for k in ['R1', 'R2']):
                R1 = context['R1']
                R2 = context['R2']
                gain = 1 + (R2 / R1)

                return {
                    "amplifier_type": "Non-Inverting",
                    "gain": gain,
                    "R1": R1,
                    "R2": R2,
                    "formula": "A_v = 1 + R2/R1",
                    "output": "V_out = V_in × (1 + R2/R1)"
                }

        return {"description": "Op-amp circuit", "types": ["inverting", "non-inverting", "summing", "integrator"]}

    def _voltage_divider(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Calcul du diviseur de tension"""
        if not context or not all(k in context for k in ['R1', 'R2', 'V_in']):
            return {"error": "Need R1, R2, and V_in"}

        R1 = context['R1']
        R2 = context['R2']
        V_in = context['V_in']

        V_out = V_in * R2 / (R1 + R2)

        return {
            "V_out": V_out,
            "V_in": V_in,
            "R1": R1,
            "R2": R2,
            "formula": "V_out = V_in × R2/(R1 + R2)",
            "ratio": R2 / (R1 + R2)
        }

    def _resonance_calculation(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Calculs de résonance"""
        if not context or not all(k in context for k in ['inductance', 'capacitance']):
            return {"error": "Need L and C values"}

        L = context['inductance']
        C = context['capacitance']

        f_0 = 1 / (2 * np.pi * np.sqrt(L * C))
        omega_0 = 1 / np.sqrt(L * C)

        return {
            "resonance_frequency": f_0,
            "angular_frequency": omega_0,
            "inductance": L,
            "capacitance": C,
            "formula": "f₀ = 1/(2π√(LC))"
        }

    def _transistor_analysis(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Analyse de transistors"""
        return {
            "description": "Transistor analysis",
            "types": ["BJT", "FET", "MOSFET"],
            "parameters": ["beta", "V_BE", "I_C", "V_CE"]
        }

    def _general_electronics(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Requêtes électroniques générales"""
        return {
            "info": "General electronics query",
            "capabilities": self.capabilities
        }

    def validate_result(self, result: Any, original_query: str) -> Dict[str, Any]:
        """Valide un résultat électronique"""
        try:
            is_valid = True
            errors = []
            confidence = 0.9

            if isinstance(result, dict):
                if "error" in result:
                    is_valid = False
                    errors.append(result["error"])
                    confidence = 0.0
                elif any(k in result for k in ['voltage', 'current', 'power', 'impedance', 'frequency']):
                    is_valid = True
                    confidence = 0.95

            return {
                "is_valid": is_valid,
                "confidence": confidence,
                "errors": errors,
                "validation_method": "electronics_structural"
            }

        except Exception as e:
            return {
                "is_valid": False,
                "confidence": 0.0,
                "errors": [str(e)]
            }
