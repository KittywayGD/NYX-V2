"""
Electronics Sandbox - Simulateur de circuits électroniques interactif
Analyse de circuits, simulation temporelle, diagrammes de Bode
"""

import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ComponentType(Enum):
    """Types de composants électroniques"""
    RESISTOR = "resistor"
    CAPACITOR = "capacitor"
    INDUCTOR = "inductor"
    VOLTAGE_SOURCE = "voltage_source"
    CURRENT_SOURCE = "current_source"
    GROUND = "ground"
    WIRE = "wire"


@dataclass
class Component:
    """Représente un composant électronique"""
    id: str
    type: ComponentType
    value: float  # Résistance (Ω), Capacitance (F), Inductance (H), Tension (V), Courant (A)
    node1: str  # Nœud d'entrée
    node2: str  # Nœud de sortie
    label: str = ""
    unit: str = ""


@dataclass
class Circuit:
    """Représente un circuit électronique"""
    components: List[Component]
    nodes: List[str]
    ground_node: str = "0"


class ElectronicsSandbox:
    """Sandbox pour simulation de circuits électroniques"""

    def __init__(self):
        self.circuits = {}

    def simulate_rc_circuit(self,
                           resistance: float,
                           capacitance: float,
                           voltage: float = 5.0,
                           duration: float = None,
                           circuit_type: str = "charging",
                           **kwargs) -> Dict[str, Any]:
        """
        Simule un circuit RC (résistance-condensateur)

        Args:
            resistance: Résistance en Ohms
            capacitance: Capacité en Farads
            voltage: Tension d'alimentation (V)
            duration: Durée de simulation (s), par défaut 5*RC
            circuit_type: "charging" ou "discharging"
        """
        try:
            # Constante de temps
            tau = resistance * capacitance

            if duration is None:
                duration = 5 * tau

            # Générer les points temporels
            num_points = 500
            times = np.linspace(0, duration, num_points)

            if circuit_type == "charging":
                # Charge: V_C(t) = V_0 * (1 - e^(-t/RC))
                v_capacitor = voltage * (1 - np.exp(-times / tau))
                i_circuit = (voltage / resistance) * np.exp(-times / tau)
            else:  # discharging
                # Décharge: V_C(t) = V_0 * e^(-t/RC)
                v_capacitor = voltage * np.exp(-times / tau)
                i_circuit = -(voltage / resistance) * np.exp(-times / tau)

            # Énergie stockée dans le condensateur
            energy = 0.5 * capacitance * v_capacitor**2

            # Puissance dissipée dans la résistance
            power = i_circuit**2 * resistance

            return {
                "success": True,
                "type": "rc_circuit",
                "data": {
                    "time": times.tolist(),
                    "voltage_capacitor": v_capacitor.tolist(),
                    "current": i_circuit.tolist(),
                    "energy": energy.tolist(),
                    "power": power.tolist(),
                },
                "parameters": {
                    "resistance": resistance,
                    "capacitance": capacitance,
                    "voltage": voltage,
                    "tau": tau,
                    "circuit_type": circuit_type,
                },
                "analysis": {
                    "time_constant": tau,
                    "time_to_63_percent": tau,
                    "time_to_95_percent": 3 * tau,
                    "time_to_99_percent": 5 * tau,
                    "max_current": abs(voltage / resistance),
                    "final_voltage": voltage if circuit_type == "charging" else 0,
                },
            }

        except Exception as e:
            logger.error(f"Error in RC circuit simulation: {e}")
            return {"success": False, "error": str(e)}

    def simulate_rl_circuit(self,
                           resistance: float,
                           inductance: float,
                           voltage: float = 12.0,
                           duration: float = None,
                           **kwargs) -> Dict[str, Any]:
        """
        Simule un circuit RL (résistance-inductance)

        Args:
            resistance: Résistance en Ohms
            inductance: Inductance en Henrys
            voltage: Tension d'alimentation (V)
            duration: Durée de simulation (s)
        """
        try:
            # Constante de temps
            tau = inductance / resistance

            if duration is None:
                duration = 5 * tau

            num_points = 500
            times = np.linspace(0, duration, num_points)

            # Courant: I(t) = (V/R) * (1 - e^(-Rt/L))
            i_circuit = (voltage / resistance) * (1 - np.exp(-times / tau))

            # Tension aux bornes de l'inductance: V_L = L * dI/dt
            v_inductor = voltage * np.exp(-times / tau)

            # Tension aux bornes de la résistance
            v_resistor = i_circuit * resistance

            # Énergie stockée dans l'inductance
            energy = 0.5 * inductance * i_circuit**2

            # Puissance dissipée
            power = i_circuit**2 * resistance

            return {
                "success": True,
                "type": "rl_circuit",
                "data": {
                    "time": times.tolist(),
                    "current": i_circuit.tolist(),
                    "voltage_inductor": v_inductor.tolist(),
                    "voltage_resistor": v_resistor.tolist(),
                    "energy": energy.tolist(),
                    "power": power.tolist(),
                },
                "parameters": {
                    "resistance": resistance,
                    "inductance": inductance,
                    "voltage": voltage,
                    "tau": tau,
                },
                "analysis": {
                    "time_constant": tau,
                    "final_current": voltage / resistance,
                    "initial_di_dt": voltage / inductance,
                },
            }

        except Exception as e:
            logger.error(f"Error in RL circuit simulation: {e}")
            return {"success": False, "error": str(e)}

    def simulate_rlc_circuit(self,
                            resistance: float,
                            inductance: float,
                            capacitance: float,
                            voltage: float = 10.0,
                            duration: float = None,
                            **kwargs) -> Dict[str, Any]:
        """
        Simule un circuit RLC série

        Args:
            resistance: Résistance (Ω)
            inductance: Inductance (H)
            capacitance: Capacité (F)
            voltage: Tension d'alimentation (V)
            duration: Durée de simulation (s)
        """
        try:
            # Paramètres du circuit
            omega_0 = 1 / np.sqrt(inductance * capacitance)  # Fréquence naturelle
            zeta = (resistance / 2) * np.sqrt(capacitance / inductance)  # Coefficient d'amortissement

            # Déterminer le régime
            if zeta < 1:
                regime = "sous-amorti"
                omega_d = omega_0 * np.sqrt(1 - zeta**2)
            elif zeta == 1:
                regime = "critique"
                omega_d = 0
            else:
                regime = "sur-amorti"
                omega_d = 0

            if duration is None:
                duration = 10 / omega_0 if omega_0 > 0 else 1.0

            num_points = 1000
            times = np.linspace(0, duration, num_points)

            # Résolution de l'équation différentielle
            # d²q/dt² + (R/L)dq/dt + (1/LC)q = V/L
            # Avec conditions initiales: q(0) = 0, i(0) = 0

            if regime == "sous-amorti":
                # Oscillations amorties
                charge = (capacitance * voltage) * (1 - np.exp(-zeta * omega_0 * times) *
                        (np.cos(omega_d * times) + (zeta * omega_0 / omega_d) * np.sin(omega_d * times)))
                current = np.gradient(charge, times)

            elif regime == "critique":
                # Amortissement critique
                charge = (capacitance * voltage) * (1 - np.exp(-omega_0 * times) * (1 + omega_0 * times))
                current = (voltage / resistance) * omega_0 * times * np.exp(-omega_0 * times)

            else:  # sur-amorti
                alpha = zeta * omega_0
                beta = omega_0 * np.sqrt(zeta**2 - 1)
                s1 = -alpha + beta
                s2 = -alpha - beta

                A = voltage / (inductance * (s1 - s2))
                charge = (capacitance * voltage) * (1 + A * (s2 * np.exp(s1 * times) - s1 * np.exp(s2 * times)))
                current = A * (np.exp(s1 * times) - np.exp(s2 * times))

            # Tensions
            v_capacitor = charge / capacitance
            v_resistor = current * resistance
            v_inductor = voltage - v_capacitor - v_resistor

            # Énergie
            energy_capacitor = 0.5 * capacitance * v_capacitor**2
            energy_inductor = 0.5 * inductance * current**2
            energy_total = energy_capacitor + energy_inductor

            return {
                "success": True,
                "type": "rlc_circuit",
                "data": {
                    "time": times.tolist(),
                    "current": current.tolist(),
                    "charge": charge.tolist(),
                    "voltage_capacitor": v_capacitor.tolist(),
                    "voltage_resistor": v_resistor.tolist(),
                    "voltage_inductor": v_inductor.tolist(),
                    "energy_capacitor": energy_capacitor.tolist(),
                    "energy_inductor": energy_inductor.tolist(),
                    "energy_total": energy_total.tolist(),
                },
                "parameters": {
                    "resistance": resistance,
                    "inductance": inductance,
                    "capacitance": capacitance,
                    "voltage": voltage,
                    "omega_0": omega_0,
                    "zeta": zeta,
                    "regime": regime,
                },
                "analysis": {
                    "natural_frequency": omega_0,
                    "damping_ratio": zeta,
                    "regime": regime,
                    "resonant_frequency": omega_0 / (2 * np.pi),
                    "quality_factor": 1 / (2 * zeta) if zeta > 0 else float('inf'),
                },
            }

        except Exception as e:
            logger.error(f"Error in RLC circuit simulation: {e}")
            return {"success": False, "error": str(e)}

    def frequency_response(self,
                          resistance: float,
                          inductance: float = None,
                          capacitance: float = None,
                          freq_min: float = 1,
                          freq_max: float = 10000,
                          num_points: int = 100,
                          **kwargs) -> Dict[str, Any]:
        """
        Calcule la réponse en fréquence d'un circuit

        Args:
            resistance: Résistance (Ω)
            inductance: Inductance optionnelle (H)
            capacitance: Capacité optionnelle (F)
            freq_min, freq_max: Plage de fréquences (Hz)
            num_points: Nombre de points
        """
        try:
            frequencies = np.logspace(np.log10(freq_min), np.log10(freq_max), num_points)
            omega = 2 * np.pi * frequencies

            if inductance and capacitance:
                # Circuit RLC
                Z = resistance + 1j * (omega * inductance - 1 / (omega * capacitance))
            elif inductance:
                # Circuit RL
                Z = resistance + 1j * omega * inductance
            elif capacitance:
                # Circuit RC
                Z = resistance + 1 / (1j * omega * capacitance)
            else:
                # Résistance pure
                Z = resistance * np.ones_like(omega)

            # Impédance
            magnitude = np.abs(Z)
            phase = np.angle(Z, deg=True)

            # Gain (normalisé)
            gain_db = 20 * np.log10(magnitude / magnitude[0])

            return {
                "success": True,
                "type": "frequency_response",
                "data": {
                    "frequency": frequencies.tolist(),
                    "magnitude": magnitude.tolist(),
                    "phase": phase.tolist(),
                    "gain_db": gain_db.tolist(),
                },
                "parameters": {
                    "resistance": resistance,
                    "inductance": inductance,
                    "capacitance": capacitance,
                },
            }

        except Exception as e:
            logger.error(f"Error in frequency response: {e}")
            return {"success": False, "error": str(e)}

    def analyze_voltage_divider(self,
                                r1: float,
                                r2: float,
                                v_in: float,
                                **kwargs) -> Dict[str, Any]:
        """
        Analyse un diviseur de tension

        Args:
            r1: Résistance 1 (Ω)
            r2: Résistance 2 (Ω)
            v_in: Tension d'entrée (V)
        """
        try:
            v_out = v_in * (r2 / (r1 + r2))
            current = v_in / (r1 + r2)
            power_r1 = current**2 * r1
            power_r2 = current**2 * r2
            power_total = power_r1 + power_r2

            return {
                "success": True,
                "type": "voltage_divider",
                "data": {
                    "v_out": v_out,
                    "current": current,
                    "power_r1": power_r1,
                    "power_r2": power_r2,
                    "power_total": power_total,
                },
                "parameters": {
                    "r1": r1,
                    "r2": r2,
                    "v_in": v_in,
                },
                "analysis": {
                    "voltage_ratio": v_out / v_in,
                    "attenuation_db": 20 * np.log10(v_out / v_in),
                    "efficiency": power_r2 / power_total,
                },
            }

        except Exception as e:
            logger.error(f"Error in voltage divider analysis: {e}")
            return {"success": False, "error": str(e)}

    def create_circuit_visualization(self,
                                    components: List[Dict[str, Any]],
                                    **kwargs) -> Dict[str, Any]:
        """
        Crée les données de visualisation pour un circuit

        Args:
            components: Liste de composants avec type, valeur, connexions
        """
        try:
            # Créer une représentation JSON du circuit pour le frontend
            circuit_elements = []

            for i, comp in enumerate(components):
                element = {
                    "id": comp.get('id', f"comp_{i}"),
                    "type": comp.get('type'),
                    "value": comp.get('value'),
                    "unit": comp.get('unit', ''),
                    "from": comp.get('node1', comp.get('from')),
                    "to": comp.get('node2', comp.get('to')),
                    "position": comp.get('position', {"x": 0, "y": 0}),
                }
                circuit_elements.append(element)

            return {
                "success": True,
                "type": "circuit_diagram",
                "data": {
                    "elements": circuit_elements,
                    "nodes": self._extract_nodes(components),
                },
            }

        except Exception as e:
            logger.error(f"Error creating circuit visualization: {e}")
            return {"success": False, "error": str(e)}

    def _extract_nodes(self, components: List[Dict]) -> List[str]:
        """Extrait les nœuds uniques d'une liste de composants"""
        nodes = set()
        for comp in components:
            if 'node1' in comp:
                nodes.add(comp['node1'])
            if 'node2' in comp:
                nodes.add(comp['node2'])
            if 'from' in comp:
                nodes.add(comp['from'])
            if 'to' in comp:
                nodes.add(comp['to'])
        return sorted(list(nodes))

    def execute(self, query: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Point d'entrée général pour le sandbox électronique

        Args:
            query: Requête utilisateur
            parameters: Paramètres extraits
        """
        parameters = parameters or {}
        query_lower = query.lower()

        # Extraire les valeurs des composants
        resistance = parameters.get('resistance', 1000)
        capacitance = parameters.get('capacitance', 1e-6)
        inductance = parameters.get('inductance', 0.1)
        voltage = parameters.get('voltage', 5.0)

        if 'rc' in query_lower and 'rlc' not in query_lower:
            return self.simulate_rc_circuit(resistance, capacitance, voltage, **parameters)

        elif 'rl' in query_lower and 'rlc' not in query_lower:
            return self.simulate_rl_circuit(resistance, inductance, voltage, **parameters)

        elif 'rlc' in query_lower:
            return self.simulate_rlc_circuit(resistance, inductance, capacitance, voltage, **parameters)

        elif 'fréquence' in query_lower or 'frequency' in query_lower or 'bode' in query_lower:
            return self.frequency_response(resistance, inductance, capacitance, **parameters)

        elif 'diviseur' in query_lower or 'divider' in query_lower:
            r1 = parameters.get('r1', 1000)
            r2 = parameters.get('r2', 1000)
            return self.analyze_voltage_divider(r1, r2, voltage, **parameters)

        else:
            # Circuit RC par défaut
            return self.simulate_rc_circuit(resistance, capacitance, voltage, **parameters)
