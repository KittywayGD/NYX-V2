"""
Module de mathématiques avancées pour Nyx
Calculs symboliques, équations différentielles, algèbre, analyse, etc.
"""

import numpy as np
import sympy as sp
from sympy import symbols, solve, diff, integrate, limit, series, Matrix, simplify
from sympy import cos, sin, tan, exp, log, sqrt, pi, E, I, oo
from scipy import optimize, integrate as scipy_integrate, linalg
from typing import Dict, Any, Optional, List, Union
import logging
import re

from modules.base_module import BaseModule


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MathematicsModule(BaseModule):
    """Module de mathématiques avancées"""

    def __init__(self):
        super().__init__("Mathematics", "1.0.0")
        self.capabilities = [
            "algebra", "calculus", "differential_equations",
            "linear_algebra", "complex_analysis", "numerical_analysis",
            "optimization", "series", "limits", "integrals", "derivatives",
            "matrices", "eigenvalues", "fourier", "laplace"
        ]
        self.metadata = {
            "description": "Module de mathématiques avancées avec calculs symboliques et numériques",
            "engines": ["SymPy", "NumPy", "SciPy"]
        }

    def initialize(self) -> bool:
        """Initialise le module"""
        try:
            logger.info("Initialisation du module Mathematics...")
            # Test des imports
            _ = sp.Symbol('x')
            _ = np.array([1, 2, 3])
            logger.info("✓ Module Mathematics initialisé")
            return True
        except Exception as e:
            logger.error(f"Erreur initialisation Mathematics: {e}")
            return False

    def execute(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Exécute une requête mathématique

        Args:
            query: Requête mathématique (équation, calcul, etc.)
            context: Contexte avec variables ou paramètres

        Returns:
            Résultats du calcul
        """
        logger.info(f"Exécution requête mathématique: {query}")

        try:
            # Déterminer le type d'opération
            operation_type = self._detect_operation_type(query)
            logger.info(f"Type d'opération détecté: {operation_type}")

            # Router vers la bonne méthode
            if operation_type == "solve_equation":
                result = self._solve_equation(query, context)
            elif operation_type == "derivative":
                result = self._compute_derivative(query, context)
            elif operation_type == "integral":
                result = self._compute_integral(query, context)
            elif operation_type == "differential_equation":
                result = self._solve_differential_equation(query, context)
            elif operation_type == "matrix":
                result = self._matrix_operations(query, context)
            elif operation_type == "limit":
                result = self._compute_limit(query, context)
            elif operation_type == "series":
                result = self._compute_series(query, context)
            elif operation_type == "optimization":
                result = self._optimize_function(query, context)
            elif operation_type == "numerical":
                result = self._numerical_computation(query, context)
            else:
                result = self._symbolic_computation(query, context)

            return {
                "success": True,
                "result": result,
                "operation_type": operation_type,
                "query": query
            }

        except Exception as e:
            logger.error(f"Erreur lors de l'exécution: {e}")
            return {
                "success": False,
                "error": str(e),
                "query": query
            }

    def _detect_operation_type(self, query: str) -> str:
        """Détecte le type d'opération mathématique"""
        query_lower = query.lower()

        if any(word in query_lower for word in ["solve", "résoudre", "equation", "équation", "="]):
            if "diff" in query_lower or "dérivée" in query_lower or "d/dx" in query_lower:
                return "differential_equation"
            return "solve_equation"
        elif any(word in query_lower for word in ["derivative", "dérivée", "dériver", "d/dx", "diff"]):
            return "derivative"
        elif any(word in query_lower for word in ["integral", "intégrale", "intégrer", "∫"]):
            return "integral"
        elif any(word in query_lower for word in ["matrix", "matrice", "eigen", "determinant"]):
            return "matrix"
        elif any(word in query_lower for word in ["limit", "limite", "lim"]):
            return "limit"
        elif any(word in query_lower for word in ["series", "série", "taylor", "maclaurin"]):
            return "series"
        elif any(word in query_lower for word in ["optimize", "optimiser", "minimize", "maximize", "min", "max"]):
            return "optimization"
        elif any(word in query_lower for word in ["numerical", "numérique", "approximate"]):
            return "numerical"
        else:
            return "symbolic"

    def _solve_equation(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Résout des équations algébriques"""
        # Extraire l'équation
        equation_match = re.search(r'[^:]+$', query)
        if equation_match:
            equation_str = equation_match.group(0).strip()
        else:
            equation_str = query

        # Définir les symboles
        x, y, z, t = symbols('x y z t')
        a, b, c, n = symbols('a b c n')

        try:
            # Parser l'équation
            if '=' in equation_str:
                lhs, rhs = equation_str.split('=')
                equation = sp.sympify(lhs.strip()) - sp.sympify(rhs.strip())
            else:
                equation = sp.sympify(equation_str)

            # Résoudre
            solutions = solve(equation)

            return {
                "equation": str(equation),
                "solutions": [str(sol) for sol in solutions] if isinstance(solutions, list) else str(solutions),
                "symbolic_solutions": solutions,
                "method": "symbolic"
            }
        except Exception as e:
            return {"error": str(e), "equation": equation_str}

    def _compute_derivative(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Calcule des dérivées"""
        x = symbols('x')

        # Extraire la fonction
        func_match = re.search(r'of\s+(.+)|de\s+(.+)', query, re.IGNORECASE)
        if func_match:
            func_str = func_match.group(1) or func_match.group(2)
            func_str = func_str.strip()
        else:
            # Prendre tout après les mots-clés
            func_str = query.split()[-1]

        try:
            function = sp.sympify(func_str)
            derivative = diff(function, x)
            derivative_simplified = simplify(derivative)

            return {
                "function": str(function),
                "derivative": str(derivative_simplified),
                "symbolic": derivative_simplified
            }
        except Exception as e:
            return {"error": str(e), "function": func_str}

    def _compute_integral(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Calcule des intégrales"""
        x = symbols('x')

        # Extraire la fonction et les bornes
        func_match = re.search(r'of\s+(.+)|de\s+(.+)', query, re.IGNORECASE)
        if func_match:
            func_str = func_match.group(1) or func_match.group(2)
        else:
            func_str = query.split()[-1]

        # Chercher des bornes
        bounds_match = re.search(r'from\s+(\S+)\s+to\s+(\S+)', query, re.IGNORECASE)

        try:
            function = sp.sympify(func_str)

            if bounds_match:
                lower = sp.sympify(bounds_match.group(1))
                upper = sp.sympify(bounds_match.group(2))
                integral_result = integrate(function, (x, lower, upper))
                integral_type = "definite"
            else:
                integral_result = integrate(function, x)
                integral_type = "indefinite"

            return {
                "function": str(function),
                "integral": str(integral_result),
                "type": integral_type,
                "symbolic": integral_result
            }
        except Exception as e:
            return {"error": str(e), "function": func_str}

    def _solve_differential_equation(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Résout des équations différentielles"""
        x = symbols('x')
        y = sp.Function('y')

        try:
            # Pour l'instant, un exemple simple
            # Dans une vraie implémentation, parser l'équation différentielle
            eq = sp.Eq(y(x).diff(x), y(x))
            solution = sp.dsolve(eq, y(x))

            return {
                "equation": str(eq),
                "solution": str(solution),
                "symbolic": solution
            }
        except Exception as e:
            return {"error": str(e)}

    def _matrix_operations(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Opérations sur les matrices"""
        try:
            # Si contexte contient une matrice
            if context and "matrix" in context:
                mat_data = context["matrix"]
                matrix = Matrix(mat_data)

                results = {
                    "matrix": str(matrix),
                    "determinant": str(matrix.det()),
                    "trace": str(matrix.trace()),
                }

                # Eigenvalues si matrice carrée
                if matrix.rows == matrix.cols:
                    eigenvals = matrix.eigenvals()
                    results["eigenvalues"] = {str(k): v for k, v in eigenvals.items()}

                return results
            else:
                return {"error": "No matrix provided in context"}

        except Exception as e:
            return {"error": str(e)}

    def _compute_limit(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Calcule des limites"""
        x = symbols('x')

        try:
            # Parser la fonction et le point
            func_match = re.search(r'of\s+(.+?)\s+as|de\s+(.+?)\s+quand', query, re.IGNORECASE)
            if func_match:
                func_str = func_match.group(1) or func_match.group(2)
            else:
                func_str = "x"

            function = sp.sympify(func_str)

            # Extraire le point limite
            point_match = re.search(r'x\s*→\s*(\S+)|x\s+tends?\s+to\s+(\S+)', query)
            if point_match:
                point_str = point_match.group(1) or point_match.group(2)
                point = sp.sympify(point_str) if point_str != "inf" else oo
            else:
                point = 0

            limit_result = limit(function, x, point)

            return {
                "function": str(function),
                "point": str(point),
                "limit": str(limit_result),
                "symbolic": limit_result
            }
        except Exception as e:
            return {"error": str(e)}

    def _compute_series(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Calcule des développements en série"""
        x = symbols('x')

        try:
            # Extraire fonction et ordre
            order = 6  # Par défaut
            order_match = re.search(r'order\s+(\d+)|ordre\s+(\d+)', query)
            if order_match:
                order = int(order_match.group(1) or order_match.group(2))

            func_match = re.search(r'of\s+(.+?)(?:\s+order|$)', query, re.IGNORECASE)
            if func_match:
                func_str = func_match.group(1).strip()
            else:
                func_str = "exp(x)"

            function = sp.sympify(func_str)
            series_expansion = series(function, x, 0, order)

            return {
                "function": str(function),
                "series": str(series_expansion),
                "order": order,
                "symbolic": series_expansion
            }
        except Exception as e:
            return {"error": str(e)}

    def _optimize_function(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Optimise une fonction"""
        x = symbols('x')

        try:
            # Extraire la fonction
            func_match = re.search(r'function\s+(.+)|fonction\s+(.+)', query, re.IGNORECASE)
            if func_match:
                func_str = func_match.group(1) or func_match.group(2)
            else:
                return {"error": "No function specified"}

            function = sp.sympify(func_str)

            # Trouver les points critiques
            derivative = diff(function, x)
            critical_points = solve(derivative, x)

            # Évaluer aux points critiques
            results = []
            for point in critical_points:
                value = function.subs(x, point)
                second_deriv = diff(derivative, x).subs(x, point)

                point_type = "unknown"
                if second_deriv > 0:
                    point_type = "minimum"
                elif second_deriv < 0:
                    point_type = "maximum"
                else:
                    point_type = "inflection"

                results.append({
                    "point": str(point),
                    "value": str(value),
                    "type": point_type
                })

            return {
                "function": str(function),
                "critical_points": results,
                "derivative": str(derivative)
            }
        except Exception as e:
            return {"error": str(e)}

    def _numerical_computation(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Calculs numériques"""
        try:
            # Évaluer numériquement une expression
            expr_match = re.search(r'compute\s+(.+)|calculate\s+(.+)|calculer\s+(.+)', query, re.IGNORECASE)
            if expr_match:
                expr_str = expr_match.group(1) or expr_match.group(2) or expr_match.group(3)
            else:
                expr_str = query

            expr = sp.sympify(expr_str)
            numerical_result = float(expr.evalf())

            return {
                "expression": str(expr),
                "result": numerical_result,
                "method": "numerical"
            }
        except Exception as e:
            return {"error": str(e)}

    def _symbolic_computation(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Calculs symboliques généraux"""
        try:
            # Simplifier ou manipuler une expression
            expr = sp.sympify(query)
            simplified = simplify(expr)

            return {
                "expression": str(expr),
                "simplified": str(simplified),
                "symbolic": simplified
            }
        except Exception as e:
            return {"error": str(e)}

    def validate_result(self, result: Any, original_query: str) -> Dict[str, Any]:
        """Valide un résultat mathématique"""
        try:
            # Vérifications basiques
            is_valid = True
            errors = []
            confidence = 0.9

            if isinstance(result, dict):
                if "error" in result:
                    is_valid = False
                    errors.append(result["error"])
                    confidence = 0.0
                elif "result" in result or "solutions" in result:
                    # Résultat semble valide
                    is_valid = True
                    confidence = 0.95

            return {
                "is_valid": is_valid,
                "confidence": confidence,
                "errors": errors,
                "validation_method": "structural"
            }

        except Exception as e:
            return {
                "is_valid": False,
                "confidence": 0.0,
                "errors": [str(e)]
            }
