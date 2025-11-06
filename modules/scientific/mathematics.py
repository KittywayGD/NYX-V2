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


def _clean_sympy_objects(obj):
    """Convertit récursivement les objets SymPy en strings pour la sérialisation JSON"""
    if isinstance(obj, dict):
        return {k: _clean_sympy_objects(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_clean_sympy_objects(item) for item in obj]
    elif hasattr(obj, '__module__') and 'sympy' in obj.__module__:
        return str(obj)
    else:
        return obj


def _add_implicit_multiplication(expr_str: str) -> str:
    """Ajoute la multiplication implicite (ex: 2x → 2*x, 3xy → 3*x*y)"""
    # Pattern pour nombre suivi d'une lettre sans opérateur entre eux
    expr_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr_str)
    # Pattern pour lettre suivie d'une autre lettre (xy → x*y)
    # ATTENTION: Ne pas casser les fonctions comme sin, cos, exp, log
    expr_str = re.sub(r'([a-zA-Z])([a-zA-Z])', lambda m: f"{m.group(1)}*{m.group(2)}"
                      if m.group(0) not in ['sin', 'cos', 'tan', 'exp', 'log', 'ln'] else m.group(0), expr_str)
    return expr_str


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

    def can_handle(self, query: str) -> float:
        """Détermine si ce module peut gérer une requête mathématique"""
        query_lower = query.lower()
        score = 0.0

        # Mots-clés français et anglais
        math_keywords = {
            # Termes généraux
            'mathématique': 0.95, 'mathematics': 0.95, 'math': 0.9,

            # Visualisation - IMPORTANT pour "Tracer x² - 4"
            'tracer': 0.9, 'plot': 0.9, 'dessiner': 0.85, 'draw': 0.85,
            'graphe': 0.9, 'graph': 0.9, 'courbe': 0.9, 'curve': 0.9,
            'visualiser': 0.85, 'visualize': 0.85, 'afficher': 0.8, 'display': 0.8,
            'fonction': 0.85, 'function': 0.85,

            # Résolution
            'résoudre': 0.9, 'solve': 0.9, 'équation': 0.9, 'equation': 0.9,
            'solution': 0.85, 'trouver': 0.7, 'find': 0.7,

            # Calcul différentiel/intégral
            'dérivée': 0.9, 'derivative': 0.9, 'dériver': 0.9, 'differentiate': 0.9,
            'intégrale': 0.9, 'integral': 0.9, 'intégrer': 0.9, 'integrate': 0.9,
            'd/dx': 0.95, '∫': 0.95,

            # Limites et séries
            'limite': 0.9, 'limit': 0.9, 'lim': 0.9,
            'série': 0.8, 'series': 0.8, 'taylor': 0.9, 'fourier': 0.9,

            # Algèbre linéaire
            'matrice': 0.9, 'matrix': 0.9, 'déterminant': 0.8, 'determinant': 0.8,
            'vecteur': 0.85, 'vector': 0.85, 'eigenvalue': 0.9, 'valeur propre': 0.9,

            # Optimisation
            'optimiser': 0.8, 'optimize': 0.8, 'minimum': 0.7, 'maximum': 0.7,
            'minimiser': 0.8, 'minimize': 0.8, 'maximiser': 0.8, 'maximize': 0.8,

            # Calcul de base
            'calculer': 0.6, 'calculate': 0.6, 'compute': 0.6,
            'simplifier': 0.7, 'simplify': 0.7, 'développer': 0.7, 'expand': 0.7,

            # Algèbre
            'polynôme': 0.85, 'polynomial': 0.85, 'factoriser': 0.8, 'factor': 0.8,
        }

        # Vérifier les mots-clés
        for keyword, weight in math_keywords.items():
            if keyword in query_lower:
                score = max(score, weight)

        # Symboles mathématiques
        math_symbols = ['=', '²', '³', '^', 'x', 'sin', 'cos', 'exp', 'log']
        symbol_count = sum(1 for s in math_symbols if s in query_lower)
        if symbol_count >= 2:
            score = max(score, 0.7)

        return min(score, 1.0)

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

            # Nettoyer les objets SymPy pour la sérialisation JSON
            result = _clean_sympy_objects(result)

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
        # Extraire l'équation en retirant les mots-clés courants
        equation_str = query

        # Retirer les mots-clés français et anglais
        keywords_to_remove = [
            r'résoudre\s+', r'solve\s+', r'résous\s+',
            r'équation\s*:?\s*', r'equation\s*:?\s*',
            r'calculer\s+', r'calculate\s+', r'compute\s+',
            r"l'équation\s+", r'the\s+equation\s+'
        ]

        for keyword in keywords_to_remove:
            equation_str = re.sub(keyword, '', equation_str, flags=re.IGNORECASE)

        equation_str = equation_str.strip()

        # Convertir les exposants unicode en notation Python
        unicode_superscripts = {
            '²': '**2', '³': '**3', '⁴': '**4', '⁵': '**5',
            '⁶': '**6', '⁷': '**7', '⁸': '**8', '⁹': '**9'
        }
        for unicode_exp, python_exp in unicode_superscripts.items():
            equation_str = equation_str.replace(unicode_exp, python_exp)

        # Ajouter la multiplication implicite (2x → 2*x)
        equation_str = _add_implicit_multiplication(equation_str)

        # Définir les symboles
        x, y, z, t = symbols('x y z t')
        a, b, c, n = symbols('a b c n')

        try:
            # Parser l'équation
            if '=' in equation_str:
                lhs, rhs = equation_str.split('=', 1)
                equation = sp.sympify(lhs.strip()) - sp.sympify(rhs.strip())
            else:
                equation = sp.sympify(equation_str)

            # Résoudre
            solutions = solve(equation, x)

            return {
                "equation": str(equation),
                "solutions": [str(sol) for sol in solutions] if isinstance(solutions, list) else [str(solutions)],
                "method": "symbolic"
            }
        except Exception as e:
            return {"error": str(e), "equation_input": equation_str}

    def _compute_derivative(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Calcule des dérivées"""
        x = symbols('x')

        # Extraire la fonction - chercher après "of" ou "de"
        func_match = re.search(r'(?:of|de)\s+(.+)', query, re.IGNORECASE)
        if func_match:
            func_str = func_match.group(1).strip()
        else:
            # Retirer les mots-clés courants
            func_str = query
            keywords = [
                r'calculer\s+(?:la\s+)?dérivée\s+', r'calculate\s+(?:the\s+)?derivative\s+',
                r'dérivée\s+', r'derivative\s+', r'dériver\s+', r'differentiate\s+',
                r'd/dx\s+', r"d'?\s*"
            ]
            for kw in keywords:
                func_str = re.sub(kw, '', func_str, flags=re.IGNORECASE)
            func_str = func_str.strip()

        # Convertir les exposants unicode en notation Python
        unicode_superscripts = {
            '²': '**2', '³': '**3', '⁴': '**4', '⁵': '**5',
            '⁶': '**6', '⁷': '**7', '⁸': '**8', '⁹': '**9'
        }
        for unicode_exp, python_exp in unicode_superscripts.items():
            func_str = func_str.replace(unicode_exp, python_exp)

        try:
            function = sp.sympify(func_str)
            derivative = diff(function, x)
            # Ne pas simplifier automatiquement - garder la forme développée
            derivative_expanded = sp.expand(derivative)

            return {
                "function": str(function),
                "derivative": str(derivative_expanded)
            }
        except Exception as e:
            return {"error": str(e), "function_input": func_str}

    def _compute_integral(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Calcule des intégrales"""
        x = symbols('x')

        # Extraire la fonction - chercher après "of" ou "de"
        func_match = re.search(r'(?:of|de)\s+(.+?)(?:\s+from|\s+de\s+|$)', query, re.IGNORECASE)
        if func_match:
            func_str = func_match.group(1).strip()
        else:
            # Retirer les mots-clés courants
            func_str = query
            keywords = [
                r'calculer\s+(?:l\')?intégrale\s+', r'calculate\s+(?:the\s+)?integral\s+',
                r'intégrale\s+', r'integral\s+', r'intégrer\s+', r'integrate\s+',
                r'∫\s*'
            ]
            for kw in keywords:
                func_str = re.sub(kw, '', func_str, flags=re.IGNORECASE)

            # Retirer les bornes si présentes
            func_str = re.sub(r'\s+(?:from|de)\s+.+', '', func_str, flags=re.IGNORECASE)
            func_str = func_str.strip()

        # Convertir les exposants unicode en notation Python
        unicode_superscripts = {
            '²': '**2', '³': '**3', '⁴': '**4', '⁵': '**5',
            '⁶': '**6', '⁷': '**7', '⁸': '**8', '⁹': '**9'
        }
        for unicode_exp, python_exp in unicode_superscripts.items():
            func_str = func_str.replace(unicode_exp, python_exp)

        # Chercher des bornes (from X to Y, de X à Y)
        bounds_match = re.search(r'(?:from|de)\s+(\S+)\s+(?:to|à)\s+(\S+)', query, re.IGNORECASE)

        try:
            function = sp.sympify(func_str)

            if bounds_match:
                # Parser les bornes en reconnaissant 'e' comme la constante E
                lower_str = bounds_match.group(1)
                upper_str = bounds_match.group(2)

                # Remplacer 'e' par la constante E de SymPy
                lower = E if lower_str.lower() == 'e' else sp.sympify(lower_str)
                upper = E if upper_str.lower() == 'e' else sp.sympify(upper_str)

                integral_result = integrate(function, (x, lower, upper))
                integral_type = "definite"

                # Pour les intégrales définies, essayer d'évaluer numériquement
                try:
                    # Simplifier d'abord
                    integral_result = sp.simplify(integral_result)
                    # Essayer d'évaluer numériquement si possible
                    if integral_result.is_number:
                        numerical_value = float(integral_result.evalf())
                        integral_str = str(integral_result)
                        # Si c'est un entier simple, afficher aussi la valeur
                        if abs(numerical_value - round(numerical_value)) < 1e-10:
                            integral_str = f"{int(round(numerical_value))}"
                        else:
                            integral_str = f"{integral_result} ≈ {numerical_value:.6f}"
                    else:
                        integral_str = str(integral_result)
                except:
                    integral_str = str(integral_result)
            else:
                integral_result = integrate(function, x)
                integral_type = "indefinite"
                integral_str = str(integral_result)

            return {
                "function": str(function),
                "integral": integral_str,
                "type": integral_type
            }
        except Exception as e:
            return {"error": str(e), "function_input": func_str}

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
