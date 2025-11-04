"""
Validateur récursif pour Jarvis
Vérifie et corrige automatiquement les résultats
"""

from typing import Dict, Any, List, Optional, Callable
import logging
import time
from dataclasses import dataclass
from enum import Enum


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ValidationStatus(Enum):
    """Statuts de validation possibles"""
    VALID = "valid"
    INVALID = "invalid"
    UNCERTAIN = "uncertain"
    CORRECTED = "corrected"
    FAILED = "failed"


@dataclass
class ValidationResult:
    """Résultat d'une validation"""
    status: ValidationStatus
    confidence: float  # 0.0 à 1.0
    original_result: Any
    corrected_result: Optional[Any] = None
    validation_details: Dict[str, Any] = None
    iterations: int = 0
    errors: List[str] = None

    def __post_init__(self):
        if self.validation_details is None:
            self.validation_details = {}
        if self.errors is None:
            self.errors = []


class RecursiveValidator:
    """
    Validateur récursif qui vérifie les résultats et corrige les erreurs
    en réexécutant avec des paramètres ajustés
    """

    def __init__(self, max_iterations: int = 3, min_confidence: float = 0.85):
        """
        Initialise le validateur récursif

        Args:
            max_iterations: Nombre maximum d'itérations de correction
            min_confidence: Confiance minimum requise (0.0 à 1.0)
        """
        self.max_iterations = max_iterations
        self.min_confidence = min_confidence
        self.validation_history: List[ValidationResult] = []

    def validate(
        self,
        result: Any,
        original_query: str,
        validator_func: Callable[[Any], Dict[str, Any]],
        corrector_func: Optional[Callable[[Any, Dict[str, Any]], Any]] = None
    ) -> ValidationResult:
        """
        Valide un résultat de manière récursive

        Args:
            result: Le résultat à valider
            original_query: La requête originale
            validator_func: Fonction qui valide le résultat
            corrector_func: Fonction optionnelle qui corrige le résultat

        Returns:
            ValidationResult avec le statut et les détails
        """
        logger.info(f"Début de validation récursive pour: {original_query}")

        current_result = result
        iteration = 0
        total_errors = []

        while iteration < self.max_iterations:
            iteration += 1
            logger.info(f"Itération de validation {iteration}/{self.max_iterations}")

            # Valider le résultat actuel
            validation_info = validator_func(current_result)

            confidence = validation_info.get("confidence", 0.0)
            is_valid = validation_info.get("is_valid", False)
            errors = validation_info.get("errors", [])
            total_errors.extend(errors)

            logger.info(f"Validation - Confiance: {confidence:.2f}, Valide: {is_valid}")

            # Si le résultat est valide et confiant, terminé
            if is_valid and confidence >= self.min_confidence:
                validation_result = ValidationResult(
                    status=ValidationStatus.VALID if iteration == 1 else ValidationStatus.CORRECTED,
                    confidence=confidence,
                    original_result=result,
                    corrected_result=current_result if iteration > 1 else None,
                    validation_details=validation_info,
                    iterations=iteration,
                    errors=total_errors
                )
                self.validation_history.append(validation_result)
                logger.info(f"✓ Validation réussie après {iteration} itération(s)")
                return validation_result

            # Si pas de fonction de correction, on arrête
            if corrector_func is None:
                break

            # Tenter de corriger
            logger.info("Tentative de correction...")
            try:
                current_result = corrector_func(current_result, validation_info)
                logger.info("Correction appliquée, nouvelle validation...")
            except Exception as e:
                logger.error(f"Erreur lors de la correction: {e}")
                total_errors.append(f"Correction error: {str(e)}")
                break

        # Maximum d'itérations atteint ou échec
        status = ValidationStatus.UNCERTAIN if iteration == 1 else ValidationStatus.FAILED
        validation_result = ValidationResult(
            status=status,
            confidence=validation_info.get("confidence", 0.0) if 'validation_info' in locals() else 0.0,
            original_result=result,
            corrected_result=current_result if current_result != result else None,
            validation_details=validation_info if 'validation_info' in locals() else {},
            iterations=iteration,
            errors=total_errors
        )

        self.validation_history.append(validation_result)
        logger.warning(f"⚠ Validation incomplète après {iteration} itération(s)")
        return validation_result

    def validate_multiple(
        self,
        results: List[Any],
        queries: List[str],
        validator_func: Callable[[Any], Dict[str, Any]],
        corrector_func: Optional[Callable[[Any, Dict[str, Any]], Any]] = None
    ) -> List[ValidationResult]:
        """
        Valide plusieurs résultats en parallèle

        Args:
            results: Liste des résultats à valider
            queries: Liste des requêtes correspondantes
            validator_func: Fonction de validation
            corrector_func: Fonction de correction optionnelle

        Returns:
            Liste des ValidationResult
        """
        validation_results = []

        for result, query in zip(results, queries):
            vr = self.validate(result, query, validator_func, corrector_func)
            validation_results.append(vr)

        return validation_results

    def cross_validate(
        self,
        result: Any,
        alternative_methods: List[Callable[[], Any]],
        comparison_func: Callable[[Any, List[Any]], Dict[str, Any]]
    ) -> ValidationResult:
        """
        Valide un résultat en le comparant avec des méthodes alternatives

        Args:
            result: Le résultat à valider
            alternative_methods: Liste de fonctions qui calculent le même résultat différemment
            comparison_func: Fonction qui compare le résultat avec les alternatives

        Returns:
            ValidationResult
        """
        logger.info("Validation croisée avec méthodes alternatives...")

        # Exécuter les méthodes alternatives
        alternative_results = []
        for i, method in enumerate(alternative_methods):
            try:
                alt_result = method()
                alternative_results.append(alt_result)
                logger.info(f"Méthode alternative {i+1} exécutée")
            except Exception as e:
                logger.error(f"Erreur méthode alternative {i+1}: {e}")
                alternative_results.append(None)

        # Comparer les résultats
        comparison = comparison_func(result, alternative_results)

        validation_result = ValidationResult(
            status=ValidationStatus.VALID if comparison.get("is_valid", False) else ValidationStatus.UNCERTAIN,
            confidence=comparison.get("confidence", 0.0),
            original_result=result,
            validation_details={
                "comparison": comparison,
                "alternative_results": alternative_results,
                "num_methods": len(alternative_methods)
            },
            iterations=1,
            errors=comparison.get("errors", [])
        )

        self.validation_history.append(validation_result)
        return validation_result

    def get_statistics(self) -> Dict[str, Any]:
        """
        Retourne les statistiques de validation

        Returns:
            Dictionnaire avec les statistiques
        """
        if not self.validation_history:
            return {"total_validations": 0}

        total = len(self.validation_history)
        status_counts = {}

        for vr in self.validation_history:
            status = vr.status.value
            status_counts[status] = status_counts.get(status, 0) + 1

        avg_iterations = sum(vr.iterations for vr in self.validation_history) / total
        avg_confidence = sum(vr.confidence for vr in self.validation_history) / total

        return {
            "total_validations": total,
            "status_distribution": status_counts,
            "average_iterations": round(avg_iterations, 2),
            "average_confidence": round(avg_confidence, 3),
            "success_rate": round(status_counts.get("valid", 0) / total, 3) if total > 0 else 0
        }

    def clear_history(self):
        """Efface l'historique de validation"""
        self.validation_history.clear()
        logger.info("Historique de validation effacé")
