"""
Math Sandbox - Visualisation interactive de fonctions mathématiques
Traçage de courbes 2D/3D, graphiques paramétriques, animations
"""

import numpy as np
import sympy as sp
from sympy import symbols, lambdify, sympify
from typing import Dict, Any, List, Optional, Tuple, Union
import json
import logging

logger = logging.getLogger(__name__)


class MathSandbox:
    """Sandbox pour visualisations mathématiques interactives"""

    def __init__(self):
        self.x, self.y, self.z, self.t = symbols('x y z t')
        self.default_range = (-10, 10)
        self.default_points = 500

    def plot_function_2d(self, function_str: str,
                        x_min: float = None, x_max: float = None,
                        num_points: int = None,
                        **kwargs) -> Dict[str, Any]:
        """
        Génère les données pour tracer une fonction 2D

        Args:
            function_str: Expression de la fonction (ex: "sin(x)", "x**2 + 2*x + 1")
            x_min, x_max: Intervalle de traçage
            num_points: Nombre de points à calculer
            **kwargs: Options additionnelles (color, style, etc.)

        Returns:
            Dict avec data points et metadata pour le frontend
        """
        try:
            # Parser la fonction
            func_expr = sympify(function_str)
            func = lambdify(self.x, func_expr, modules=['numpy'])

            # Paramètres par défaut
            x_min = x_min if x_min is not None else self.default_range[0]
            x_max = x_max if x_max is not None else self.default_range[1]
            num_points = num_points or self.default_points

            # Générer les points
            x_values = np.linspace(x_min, x_max, num_points)
            y_values = func(x_values)

            # Gérer les infinis et NaN
            mask = np.isfinite(y_values)
            x_clean = x_values[mask].tolist()
            y_clean = y_values[mask].tolist()

            # Trouver les points remarquables
            critical_points = self._find_critical_points(func_expr, x_min, x_max)
            zeros = self._find_zeros(func_expr, x_min, x_max)

            return {
                "success": True,
                "type": "function_2d",
                "data": {
                    "x": x_clean,
                    "y": y_clean,
                    "function": str(func_expr),
                    "x_min": x_min,
                    "x_max": x_max,
                },
                "metadata": {
                    "critical_points": critical_points,
                    "zeros": zeros,
                    "num_points": len(x_clean),
                },
                "options": kwargs,
            }

        except Exception as e:
            logger.error(f"Error plotting function: {e}")
            return {
                "success": False,
                "error": str(e),
                "function": function_str,
            }

    def plot_parametric_2d(self, x_expr: str, y_expr: str,
                          t_min: float = 0, t_max: float = 2*np.pi,
                          num_points: int = None,
                          **kwargs) -> Dict[str, Any]:
        """
        Génère les données pour une courbe paramétrique 2D

        Args:
            x_expr: Expression pour x(t)
            y_expr: Expression pour y(t)
            t_min, t_max: Intervalle du paramètre t
            num_points: Nombre de points
        """
        try:
            x_func_expr = sympify(x_expr)
            y_func_expr = sympify(y_expr)

            x_func = lambdify(self.t, x_func_expr, modules=['numpy'])
            y_func = lambdify(self.t, y_func_expr, modules=['numpy'])

            num_points = num_points or self.default_points
            t_values = np.linspace(t_min, t_max, num_points)

            x_values = x_func(t_values)
            y_values = y_func(t_values)

            return {
                "success": True,
                "type": "parametric_2d",
                "data": {
                    "x": x_values.tolist(),
                    "y": y_values.tolist(),
                    "t": t_values.tolist(),
                    "x_expr": str(x_func_expr),
                    "y_expr": str(y_func_expr),
                },
                "metadata": {
                    "t_min": t_min,
                    "t_max": t_max,
                    "num_points": num_points,
                },
                "options": kwargs,
            }

        except Exception as e:
            logger.error(f"Error plotting parametric curve: {e}")
            return {
                "success": False,
                "error": str(e),
            }

    def plot_function_3d(self, function_str: str,
                        x_min: float = None, x_max: float = None,
                        y_min: float = None, y_max: float = None,
                        num_points: int = 50,
                        **kwargs) -> Dict[str, Any]:
        """
        Génère les données pour tracer une surface 3D z = f(x, y)

        Args:
            function_str: Expression de la fonction (ex: "x**2 + y**2")
            x_min, x_max, y_min, y_max: Intervalles
            num_points: Nombre de points par dimension
        """
        try:
            func_expr = sympify(function_str)
            func = lambdify((self.x, self.y), func_expr, modules=['numpy'])

            x_min = x_min if x_min is not None else self.default_range[0]
            x_max = x_max if x_max is not None else self.default_range[1]
            y_min = y_min if y_min is not None else self.default_range[0]
            y_max = y_max if y_max is not None else self.default_range[1]

            # Créer la grille
            x_grid = np.linspace(x_min, x_max, num_points)
            y_grid = np.linspace(y_min, y_max, num_points)
            X, Y = np.meshgrid(x_grid, y_grid)

            # Calculer Z
            Z = func(X, Y)

            # Gérer les infinis
            Z = np.where(np.isfinite(Z), Z, np.nan)

            return {
                "success": True,
                "type": "function_3d",
                "data": {
                    "x": X.tolist(),
                    "y": Y.tolist(),
                    "z": Z.tolist(),
                    "function": str(func_expr),
                },
                "metadata": {
                    "x_min": x_min,
                    "x_max": x_max,
                    "y_min": y_min,
                    "y_max": y_max,
                    "num_points": num_points,
                },
                "options": kwargs,
            }

        except Exception as e:
            logger.error(f"Error plotting 3D function: {e}")
            return {
                "success": False,
                "error": str(e),
            }

    def plot_polar(self, r_expr: str,
                  theta_min: float = 0, theta_max: float = 2*np.pi,
                  num_points: int = None,
                  **kwargs) -> Dict[str, Any]:
        """
        Génère les données pour une courbe polaire r(θ)

        Args:
            r_expr: Expression pour r(theta)
            theta_min, theta_max: Intervalle de θ
            num_points: Nombre de points
        """
        try:
            theta = symbols('theta')
            r_func_expr = sympify(r_expr.replace('θ', 'theta'))
            r_func = lambdify(theta, r_func_expr, modules=['numpy'])

            num_points = num_points or self.default_points
            theta_values = np.linspace(theta_min, theta_max, num_points)
            r_values = r_func(theta_values)

            # Convertir en coordonnées cartésiennes pour le traçage
            x_values = r_values * np.cos(theta_values)
            y_values = r_values * np.sin(theta_values)

            return {
                "success": True,
                "type": "polar",
                "data": {
                    "x": x_values.tolist(),
                    "y": y_values.tolist(),
                    "r": r_values.tolist(),
                    "theta": theta_values.tolist(),
                    "r_expr": str(r_func_expr),
                },
                "metadata": {
                    "theta_min": theta_min,
                    "theta_max": theta_max,
                    "num_points": num_points,
                },
                "options": kwargs,
            }

        except Exception as e:
            logger.error(f"Error plotting polar curve: {e}")
            return {
                "success": False,
                "error": str(e),
            }

    def plot_vector_field(self, u_expr: str, v_expr: str,
                         x_min: float = None, x_max: float = None,
                         y_min: float = None, y_max: float = None,
                         num_points: int = 20,
                         **kwargs) -> Dict[str, Any]:
        """
        Génère les données pour un champ de vecteurs 2D

        Args:
            u_expr: Composante x du vecteur
            v_expr: Composante y du vecteur
            x_min, x_max, y_min, y_max: Intervalles
            num_points: Nombre de vecteurs par dimension
        """
        try:
            u_func_expr = sympify(u_expr)
            v_func_expr = sympify(v_expr)

            u_func = lambdify((self.x, self.y), u_func_expr, modules=['numpy'])
            v_func = lambdify((self.x, self.y), v_func_expr, modules=['numpy'])

            x_min = x_min if x_min is not None else self.default_range[0]
            x_max = x_max if x_max is not None else self.default_range[1]
            y_min = y_min if y_min is not None else self.default_range[0]
            y_max = y_max if y_max is not None else self.default_range[1]

            x_grid = np.linspace(x_min, x_max, num_points)
            y_grid = np.linspace(y_min, y_max, num_points)
            X, Y = np.meshgrid(x_grid, y_grid)

            U = u_func(X, Y)
            V = v_func(X, Y)

            return {
                "success": True,
                "type": "vector_field",
                "data": {
                    "x": X.tolist(),
                    "y": Y.tolist(),
                    "u": U.tolist(),
                    "v": V.tolist(),
                    "u_expr": str(u_func_expr),
                    "v_expr": str(v_func_expr),
                },
                "metadata": {
                    "x_min": x_min,
                    "x_max": x_max,
                    "y_min": y_min,
                    "y_max": y_max,
                    "num_points": num_points,
                },
                "options": kwargs,
            }

        except Exception as e:
            logger.error(f"Error plotting vector field: {e}")
            return {
                "success": False,
                "error": str(e),
            }

    def _find_critical_points(self, func_expr, x_min: float, x_max: float) -> List[Dict[str, float]]:
        """Trouve les points critiques (dérivée = 0)"""
        try:
            derivative = sp.diff(func_expr, self.x)
            critical_x = sp.solve(derivative, self.x)

            points = []
            func = lambdify(self.x, func_expr, modules=['numpy'])

            for x_val in critical_x:
                if x_val.is_real:
                    x_float = float(x_val.evalf())
                    if x_min <= x_float <= x_max:
                        y_float = float(func(x_float))
                        if np.isfinite(y_float):
                            # Déterminer le type (min, max, inflexion)
                            second_deriv = sp.diff(derivative, self.x)
                            second_deriv_val = float(second_deriv.subs(self.x, x_val).evalf())

                            point_type = "inflection"
                            if second_deriv_val > 0:
                                point_type = "minimum"
                            elif second_deriv_val < 0:
                                point_type = "maximum"

                            points.append({
                                "x": x_float,
                                "y": y_float,
                                "type": point_type
                            })

            return points[:10]  # Limiter à 10 points

        except Exception as e:
            logger.debug(f"Could not find critical points: {e}")
            return []

    def _find_zeros(self, func_expr, x_min: float, x_max: float) -> List[float]:
        """Trouve les zéros de la fonction"""
        try:
            zeros = sp.solve(func_expr, self.x)
            result = []

            for zero in zeros:
                if zero.is_real:
                    zero_float = float(zero.evalf())
                    if x_min <= zero_float <= x_max:
                        result.append(zero_float)

            return result[:10]  # Limiter à 10 zéros

        except Exception as e:
            logger.debug(f"Could not find zeros: {e}")
            return []

    def animate_function(self, function_template: str,
                        parameter_name: str = 'a',
                        param_values: List[float] = None,
                        x_min: float = None, x_max: float = None,
                        **kwargs) -> Dict[str, Any]:
        """
        Génère une animation de fonction avec paramètre variable

        Args:
            function_template: Fonction avec paramètre (ex: "a*sin(x)")
            parameter_name: Nom du paramètre à varier
            param_values: Valeurs du paramètre pour l'animation
            x_min, x_max: Intervalle de traçage
        """
        try:
            param_symbol = symbols(parameter_name)
            func_expr = sympify(function_template)

            x_min = x_min if x_min is not None else self.default_range[0]
            x_max = x_max if x_max is not None else self.default_range[1]

            if param_values is None:
                param_values = np.linspace(-5, 5, 30).tolist()

            x_values = np.linspace(x_min, x_max, self.default_points)

            # Générer les frames
            frames = []
            for param_val in param_values:
                func_with_param = func_expr.subs(param_symbol, param_val)
                func = lambdify(self.x, func_with_param, modules=['numpy'])
                y_values = func(x_values)

                # Nettoyer les infinis
                mask = np.isfinite(y_values)

                frames.append({
                    "x": x_values[mask].tolist(),
                    "y": y_values[mask].tolist(),
                    "parameter_value": param_val,
                })

            return {
                "success": True,
                "type": "animation",
                "data": {
                    "frames": frames,
                    "function_template": str(func_expr),
                    "parameter_name": parameter_name,
                },
                "metadata": {
                    "num_frames": len(frames),
                    "x_min": x_min,
                    "x_max": x_max,
                },
                "options": kwargs,
            }

        except Exception as e:
            logger.error(f"Error creating animation: {e}")
            return {
                "success": False,
                "error": str(e),
            }

    def execute(self, query: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Point d'entrée général pour le sandbox math

        Args:
            query: Requête utilisateur
            parameters: Paramètres extraits par l'intent system
        """
        parameters = parameters or {}

        # Déterminer le type de visualisation demandé
        query_lower = query.lower()

        if '3d' in query_lower or 'surface' in query_lower:
            function = parameters.get('function', 'x**2 + y**2')
            return self.plot_function_3d(function, **parameters)

        elif 'paramétrique' in query_lower or 'parametric' in query_lower:
            x_expr = parameters.get('x_expr', 'cos(t)')
            y_expr = parameters.get('y_expr', 'sin(t)')
            return self.plot_parametric_2d(x_expr, y_expr, **parameters)

        elif 'polaire' in query_lower or 'polar' in query_lower:
            r_expr = parameters.get('r_expr', parameters.get('function', '1 + cos(theta)'))
            return self.plot_polar(r_expr, **parameters)

        elif 'champ' in query_lower or 'vector' in query_lower:
            u_expr = parameters.get('u_expr', '-y')
            v_expr = parameters.get('v_expr', 'x')
            return self.plot_vector_field(u_expr, v_expr, **parameters)

        elif 'animer' in query_lower or 'animate' in query_lower:
            function = parameters.get('function', 'a*sin(x)')
            return self.animate_function(function, **parameters)

        else:
            # Par défaut: fonction 2D
            function = parameters.get('function')
            if not function:
                return {
                    "success": False,
                    "error": "No function specified",
                    "query": query,
                }

            return self.plot_function_2d(function, **parameters)
