"""
Physics Sandbox - Simulations physiques interactives
Mécanique, collisions, oscillations, projectiles, ondes
"""

import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class PhysicsObject:
    """Représente un objet physique dans la simulation"""
    id: str
    type: str  # "circle", "rectangle", "polygon"
    x: float
    y: float
    vx: float = 0.0  # Vitesse x
    vy: float = 0.0  # Vitesse y
    mass: float = 1.0
    radius: float = None  # Pour cercles
    width: float = None  # Pour rectangles
    height: float = None
    angle: float = 0.0
    angular_velocity: float = 0.0
    restitution: float = 0.8  # Coefficient de restitution
    friction: float = 0.1
    is_static: bool = False
    color: str = "#3498db"


@dataclass
class SimulationConfig:
    """Configuration de la simulation"""
    gravity: float = 9.81
    dt: float = 0.016  # Time step (60 FPS)
    width: float = 800
    height: float = 600
    air_resistance: float = 0.0
    enable_collisions: bool = True


class PhysicsSandbox:
    """Sandbox pour simulations physiques 2D"""

    def __init__(self):
        self.objects: List[PhysicsObject] = []
        self.config = SimulationConfig()
        self.time = 0.0

    def create_projectile_simulation(self,
                                    initial_velocity: float,
                                    angle_degrees: float,
                                    height: float = 0.0,
                                    mass: float = 1.0,
                                    duration: float = 10.0,
                                    **kwargs) -> Dict[str, Any]:
        """
        Simule le mouvement d'un projectile

        Args:
            initial_velocity: Vitesse initiale (m/s)
            angle_degrees: Angle de lancement (degrés)
            height: Hauteur initiale (m)
            mass: Masse du projectile (kg)
            duration: Durée de simulation (s)
        """
        try:
            angle_rad = np.radians(angle_degrees)
            g = kwargs.get('gravity', 9.81)
            dt = 0.01  # Time step pour la simulation

            # Composantes de vitesse initiale
            vx0 = initial_velocity * np.cos(angle_rad)
            vy0 = initial_velocity * np.sin(angle_rad)

            # Calculer la trajectoire
            times = []
            x_positions = []
            y_positions = []
            velocities = []
            energies = []

            t = 0
            x, y = 0, height
            vx, vy = vx0, vy0

            while t <= duration and y >= 0:
                times.append(t)
                x_positions.append(x)
                y_positions.append(y)

                # Vitesse et énergie
                v = np.sqrt(vx**2 + vy**2)
                velocities.append(v)

                kinetic = 0.5 * mass * v**2
                potential = mass * g * y
                total = kinetic + potential
                energies.append({
                    "kinetic": kinetic,
                    "potential": potential,
                    "total": total,
                })

                # Mise à jour (Euler)
                x += vx * dt
                y += vy * dt
                vy -= g * dt  # Accélération gravitationnelle

                t += dt

            # Calculer les valeurs remarquables
            max_height = max(y_positions)
            max_height_time = times[y_positions.index(max_height)]
            range_distance = x_positions[-1] if y_positions[-1] <= 0 else None
            flight_time = times[-1] if y_positions[-1] <= 0 else None

            return {
                "success": True,
                "type": "projectile",
                "data": {
                    "time": times,
                    "x": x_positions,
                    "y": y_positions,
                    "velocity": velocities,
                    "energy": energies,
                },
                "parameters": {
                    "initial_velocity": initial_velocity,
                    "angle": angle_degrees,
                    "height": height,
                    "mass": mass,
                    "gravity": g,
                },
                "analysis": {
                    "max_height": max_height,
                    "max_height_time": max_height_time,
                    "range": range_distance,
                    "flight_time": flight_time,
                },
            }

        except Exception as e:
            logger.error(f"Error in projectile simulation: {e}")
            return {"success": False, "error": str(e)}

    def create_pendulum_simulation(self,
                                  length: float = 1.0,
                                  angle0_degrees: float = 45.0,
                                  mass: float = 1.0,
                                  damping: float = 0.0,
                                  duration: float = 10.0,
                                  **kwargs) -> Dict[str, Any]:
        """
        Simule un pendule simple

        Args:
            length: Longueur du pendule (m)
            angle0_degrees: Angle initial (degrés)
            mass: Masse (kg)
            damping: Coefficient d'amortissement
            duration: Durée de simulation (s)
        """
        try:
            g = kwargs.get('gravity', 9.81)
            dt = 0.01

            # Angle initial en radians
            theta = np.radians(angle0_degrees)
            omega = 0.0  # Vitesse angulaire initiale

            times = []
            angles = []
            angular_velocities = []
            x_positions = []
            y_positions = []
            energies = []

            t = 0
            while t <= duration:
                times.append(t)
                angles.append(np.degrees(theta))
                angular_velocities.append(omega)

                # Position cartésienne
                x = length * np.sin(theta)
                y = -length * np.cos(theta)
                x_positions.append(x)
                y_positions.append(y)

                # Énergie
                v = length * abs(omega)
                kinetic = 0.5 * mass * v**2
                potential = mass * g * length * (1 - np.cos(theta))
                total = kinetic + potential
                energies.append({
                    "kinetic": kinetic,
                    "potential": potential,
                    "total": total,
                })

                # Mise à jour (méthode d'Euler)
                alpha = -(g / length) * np.sin(theta) - damping * omega
                omega += alpha * dt
                theta += omega * dt

                t += dt

            # Période approximative
            if damping == 0:
                # Approximation petits angles
                theoretical_period = 2 * np.pi * np.sqrt(length / g)
            else:
                theoretical_period = None

            return {
                "success": True,
                "type": "pendulum",
                "data": {
                    "time": times,
                    "angle": angles,
                    "angular_velocity": angular_velocities,
                    "x": x_positions,
                    "y": y_positions,
                    "energy": energies,
                },
                "parameters": {
                    "length": length,
                    "initial_angle": angle0_degrees,
                    "mass": mass,
                    "damping": damping,
                    "gravity": g,
                },
                "analysis": {
                    "theoretical_period": theoretical_period,
                    "max_angle": max(angles),
                    "min_angle": min(angles),
                },
            }

        except Exception as e:
            logger.error(f"Error in pendulum simulation: {e}")
            return {"success": False, "error": str(e)}

    def create_collision_simulation(self,
                                   objects: List[Dict[str, Any]],
                                   duration: float = 5.0,
                                   **kwargs) -> Dict[str, Any]:
        """
        Simule des collisions entre objets

        Args:
            objects: Liste d'objets avec propriétés (position, vitesse, masse)
            duration: Durée de simulation (s)
        """
        try:
            dt = 0.016  # 60 FPS
            g = kwargs.get('gravity', 9.81)

            # Initialiser les objets
            physics_objects = []
            for i, obj_data in enumerate(objects):
                obj = PhysicsObject(
                    id=f"obj_{i}",
                    type=obj_data.get('type', 'circle'),
                    x=obj_data.get('x', 0),
                    y=obj_data.get('y', 0),
                    vx=obj_data.get('vx', 0),
                    vy=obj_data.get('vy', 0),
                    mass=obj_data.get('mass', 1.0),
                    radius=obj_data.get('radius', 0.5),
                    restitution=obj_data.get('restitution', 0.8),
                    is_static=obj_data.get('is_static', False),
                )
                physics_objects.append(obj)

            # Simuler
            frames = []
            t = 0

            while t <= duration:
                frame_objects = []

                for obj in physics_objects:
                    if not obj.is_static:
                        # Appliquer la gravité
                        obj.vy -= g * dt

                        # Mettre à jour la position
                        obj.x += obj.vx * dt
                        obj.y += obj.vy * dt

                        # Collision avec le sol
                        if obj.y - obj.radius <= 0:
                            obj.y = obj.radius
                            obj.vy = -obj.vy * obj.restitution

                        # Collision avec les murs
                        if obj.x - obj.radius <= 0 or obj.x + obj.radius >= 10:
                            obj.vx = -obj.vx * obj.restitution

                    frame_objects.append({
                        "id": obj.id,
                        "x": obj.x,
                        "y": obj.y,
                        "vx": obj.vx,
                        "vy": obj.vy,
                        "radius": obj.radius,
                    })

                # Détecter collisions entre objets
                for i, obj1 in enumerate(physics_objects):
                    for j, obj2 in enumerate(physics_objects[i+1:], i+1):
                        if self._detect_collision(obj1, obj2):
                            self._resolve_collision(obj1, obj2)

                frames.append({
                    "time": t,
                    "objects": frame_objects,
                })

                t += dt

            return {
                "success": True,
                "type": "collision",
                "data": {
                    "frames": frames,
                    "num_objects": len(objects),
                },
                "parameters": {
                    "duration": duration,
                    "gravity": g,
                    "dt": dt,
                },
            }

        except Exception as e:
            logger.error(f"Error in collision simulation: {e}")
            return {"success": False, "error": str(e)}

    def create_wave_simulation(self,
                              wave_type: str = "sine",
                              frequency: float = 1.0,
                              amplitude: float = 1.0,
                              wavelength: float = 2.0,
                              duration: float = 5.0,
                              **kwargs) -> Dict[str, Any]:
        """
        Simule une onde se propageant

        Args:
            wave_type: Type d'onde ("sine", "square", "sawtooth")
            frequency: Fréquence (Hz)
            amplitude: Amplitude
            wavelength: Longueur d'onde
            duration: Durée de simulation (s)
        """
        try:
            dt = 0.05
            x_points = np.linspace(0, 10, 100)

            frames = []
            t = 0

            while t <= duration:
                if wave_type == "sine":
                    y_values = amplitude * np.sin(2 * np.pi * (x_points / wavelength - frequency * t))
                elif wave_type == "square":
                    y_values = amplitude * np.sign(np.sin(2 * np.pi * (x_points / wavelength - frequency * t)))
                elif wave_type == "sawtooth":
                    phase = 2 * np.pi * (x_points / wavelength - frequency * t)
                    y_values = amplitude * (2 * (phase / (2 * np.pi) - np.floor(phase / (2 * np.pi) + 0.5)))
                else:
                    y_values = np.zeros_like(x_points)

                frames.append({
                    "time": t,
                    "x": x_points.tolist(),
                    "y": y_values.tolist(),
                })

                t += dt

            return {
                "success": True,
                "type": "wave",
                "data": {
                    "frames": frames,
                },
                "parameters": {
                    "wave_type": wave_type,
                    "frequency": frequency,
                    "amplitude": amplitude,
                    "wavelength": wavelength,
                    "speed": frequency * wavelength,
                },
            }

        except Exception as e:
            logger.error(f"Error in wave simulation: {e}")
            return {"success": False, "error": str(e)}

    def _detect_collision(self, obj1: PhysicsObject, obj2: PhysicsObject) -> bool:
        """Détecte une collision entre deux objets circulaires"""
        if obj1.type == "circle" and obj2.type == "circle":
            dx = obj2.x - obj1.x
            dy = obj2.y - obj1.y
            distance = np.sqrt(dx**2 + dy**2)
            return distance < (obj1.radius + obj2.radius)
        return False

    def _resolve_collision(self, obj1: PhysicsObject, obj2: PhysicsObject):
        """Résout une collision élastique entre deux objets"""
        if obj1.is_static and obj2.is_static:
            return

        # Vecteur de collision
        dx = obj2.x - obj1.x
        dy = obj2.y - obj1.y
        distance = np.sqrt(dx**2 + dy**2)

        if distance == 0:
            return

        # Normale de collision
        nx = dx / distance
        ny = dy / distance

        # Vitesse relative
        dvx = obj2.vx - obj1.vx
        dvy = obj2.vy - obj1.vy

        # Vitesse relative selon la normale
        dvn = dvx * nx + dvy * ny

        # Ne rien faire si les objets s'éloignent
        if dvn >= 0:
            return

        # Coefficient de restitution moyen
        e = (obj1.restitution + obj2.restitution) / 2

        # Impulsion
        if obj1.is_static:
            obj2.vx -= (1 + e) * dvn * nx
            obj2.vy -= (1 + e) * dvn * ny
        elif obj2.is_static:
            obj1.vx += (1 + e) * dvn * nx
            obj1.vy += (1 + e) * dvn * ny
        else:
            j = -(1 + e) * dvn / (1/obj1.mass + 1/obj2.mass)

            obj1.vx -= j * nx / obj1.mass
            obj1.vy -= j * ny / obj1.mass
            obj2.vx += j * nx / obj2.mass
            obj2.vy += j * ny / obj2.mass

        # Séparer les objets
        overlap = (obj1.radius + obj2.radius) - distance
        if overlap > 0:
            if obj1.is_static:
                obj2.x += nx * overlap
                obj2.y += ny * overlap
            elif obj2.is_static:
                obj1.x -= nx * overlap
                obj1.y -= ny * overlap
            else:
                obj1.x -= nx * overlap / 2
                obj1.y -= ny * overlap / 2
                obj2.x += nx * overlap / 2
                obj2.y += ny * overlap / 2

    def execute(self, query: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Point d'entrée général pour le sandbox physique

        Args:
            query: Requête utilisateur
            parameters: Paramètres extraits
        """
        parameters = parameters or {}
        query_lower = query.lower()

        if 'projectile' in query_lower or 'lancer' in query_lower:
            velocity = parameters.get('velocity', 20.0)
            angle = parameters.get('angle', 45.0)
            return self.create_projectile_simulation(velocity, angle, **parameters)

        elif 'pendule' in query_lower or 'pendulum' in query_lower:
            length = parameters.get('length', 1.0)
            angle = parameters.get('angle', 45.0)
            return self.create_pendulum_simulation(length, angle, **parameters)

        elif 'collision' in query_lower:
            objects = parameters.get('objects', [
                {"x": 2, "y": 5, "vx": 2, "vy": 0, "mass": 1.0, "radius": 0.5},
                {"x": 8, "y": 5, "vx": -2, "vy": 0, "mass": 1.0, "radius": 0.5},
            ])
            return self.create_collision_simulation(objects, **parameters)

        elif 'onde' in query_lower or 'wave' in query_lower:
            wave_type = parameters.get('wave_type', 'sine')
            frequency = parameters.get('frequency', 1.0)
            return self.create_wave_simulation(wave_type, frequency, **parameters)

        else:
            return {
                "success": False,
                "error": "Unknown physics simulation type",
                "query": query,
            }
