"""
FastAPI Backend pour NYX-V2
API REST pour l'interface Electron
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging
import sys
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import Nyx
from core.intent_system import IntentRouter, IntentDetector
from modules.sandboxes import MathSandbox, PhysicsSandbox, ElectronicsSandbox

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Créer l'application FastAPI
app = FastAPI(
    title="NYX-V2 API",
    description="API REST pour l'assistant scientifique NYX-V2",
    version="2.0.0"
)

# Configuration CORS pour Electron
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les origines exactes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instances globales
nyx = None
intent_detector = None
intent_router = None
math_sandbox = None
physics_sandbox = None
electronics_sandbox = None


# Models Pydantic pour validation
class QueryRequest(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = None
    validate: bool = True
    module: Optional[str] = None


class IntentRequest(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = None


class SandboxRequest(BaseModel):
    sandbox_type: str  # "math", "physics", "electronics"
    action: str
    parameters: Dict[str, Any]


class PlotRequest(BaseModel):
    function: str
    x_min: Optional[float] = -10
    x_max: Optional[float] = 10
    plot_type: Optional[str] = "2d"  # "2d", "3d", "parametric", "polar"
    parameters: Optional[Dict[str, Any]] = {}


class PhysicsSimRequest(BaseModel):
    simulation_type: str  # "projectile", "pendulum", "collision", "wave"
    parameters: Dict[str, Any]


class CircuitSimRequest(BaseModel):
    circuit_type: str  # "rc", "rl", "rlc", "divider"
    parameters: Dict[str, Any]


@app.on_event("startup")
async def startup_event():
    """Initialise les composants au démarrage"""
    global nyx, intent_detector, intent_router, math_sandbox, physics_sandbox, electronics_sandbox

    logger.info("Starting NYX-V2 API...")

    try:
        # Initialiser NYX
        nyx = Nyx()
        logger.info("✓ NYX initialized")

        # Initialiser l'intent system
        intent_detector = IntentDetector()
        intent_router = IntentRouter(nyx.module_manager)
        logger.info("✓ Intent system initialized")

        # Initialiser les sandboxes
        math_sandbox = MathSandbox()
        physics_sandbox = PhysicsSandbox()
        electronics_sandbox = ElectronicsSandbox()
        logger.info("✓ Sandboxes initialized")

        logger.info("NYX-V2 API ready!")

    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Nettoyage à l'arrêt"""
    global nyx

    logger.info("Shutting down NYX-V2 API...")

    if nyx:
        nyx.shutdown()
        logger.info("✓ NYX shut down")


# ============================================================================
# Endpoints Principaux
# ============================================================================

@app.get("/")
async def root():
    """Page d'accueil de l'API"""
    return {
        "name": "NYX-V2 API",
        "version": "2.0.0",
        "status": "running",
        "description": "API REST pour l'assistant scientifique NYX-V2",
        "docs": "/docs",
    }


@app.get("/api/status")
async def get_status():
    """Statut du système"""
    try:
        status = nyx.get_status() if nyx else {}

        return {
            "success": True,
            "status": "running",
            "nyx": status,
            "sandboxes": {
                "math": math_sandbox is not None,
                "physics": physics_sandbox is not None,
                "electronics": electronics_sandbox is not None,
            },
        }

    except Exception as e:
        logger.error(f"Error getting status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/modules")
async def get_modules():
    """Liste des modules disponibles"""
    try:
        if not nyx:
            raise HTTPException(status_code=503, detail="NYX not initialized")

        modules_info = []
        for name, module in nyx.module_manager.modules.items():
            modules_info.append({
                "name": name,
                "version": module.version,
                "capabilities": module.capabilities,
                "metadata": module.metadata,
            })

        return {
            "success": True,
            "modules": modules_info,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting modules: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/query")
async def process_query(request: QueryRequest):
    """
    Traite une requête utilisateur

    Cette endpoint est le point d'entrée principal pour toutes les requêtes.
    Elle détecte automatiquement l'intent et route vers le bon module.
    """
    try:
        if not nyx:
            raise HTTPException(status_code=503, detail="NYX not initialized")

        logger.info(f"Processing query: {request.query}")

        # Traiter avec NYX
        response = nyx.ask(
            query=request.query,
            context=request.context,
            validate=request.validate,
            module=request.module
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Intent Detection
# ============================================================================

@app.post("/api/intent/detect")
async def detect_intent(request: IntentRequest):
    """
    Détecte l'intention d'une requête sans l'exécuter

    Utile pour le frontend qui veut afficher l'intent avant exécution
    """
    try:
        if not intent_detector:
            raise HTTPException(status_code=503, detail="Intent detector not initialized")

        intent = intent_detector.detect(request.query, request.context)

        return {
            "success": True,
            "intent": {
                "category": intent.category.value,
                "domain": intent.domain.value,
                "action": intent.action.value,
                "confidence": intent.confidence,
                "requires_sandbox": intent.requires_sandbox,
                "parameters": intent.parameters,
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error detecting intent: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/intent/route")
async def route_intent(request: IntentRequest):
    """
    Route une requête vers le bon module et méthode

    Retourne le routing sans exécuter
    """
    try:
        if not intent_router:
            raise HTTPException(status_code=503, detail="Intent router not initialized")

        routing = intent_router.route(request.query, request.context)

        return {
            "success": True,
            "routing": routing,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error routing intent: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Math Sandbox
# ============================================================================

@app.post("/api/sandbox/math/plot")
async def math_plot(request: PlotRequest):
    """
    Génère les données pour tracer une fonction mathématique

    Types supportés: "2d", "3d", "parametric", "polar", "vector_field"
    """
    try:
        if not math_sandbox:
            raise HTTPException(status_code=503, detail="Math sandbox not initialized")

        plot_type = request.plot_type.lower()

        if plot_type == "2d" or plot_type == "function_2d":
            result = math_sandbox.plot_function_2d(
                request.function,
                request.x_min,
                request.x_max,
                **request.parameters
            )
        elif plot_type == "3d" or plot_type == "function_3d":
            result = math_sandbox.plot_function_3d(
                request.function,
                **request.parameters
            )
        elif plot_type == "parametric":
            x_expr = request.parameters.get('x_expr', 'cos(t)')
            y_expr = request.parameters.get('y_expr', 'sin(t)')
            result = math_sandbox.plot_parametric_2d(x_expr, y_expr, **request.parameters)
        elif plot_type == "polar":
            result = math_sandbox.plot_polar(request.function, **request.parameters)
        elif plot_type == "vector_field":
            u_expr = request.parameters.get('u_expr', '-y')
            v_expr = request.parameters.get('v_expr', 'x')
            result = math_sandbox.plot_vector_field(u_expr, v_expr, **request.parameters)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown plot type: {plot_type}")

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in math plot: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/sandbox/math/animate")
async def math_animate(request: Dict[str, Any]):
    """Génère une animation de fonction"""
    try:
        if not math_sandbox:
            raise HTTPException(status_code=503, detail="Math sandbox not initialized")

        function_template = request.get('function')
        if not function_template:
            raise HTTPException(status_code=400, detail="Function template required")

        result = math_sandbox.animate_function(
            function_template,
            **request.get('parameters', {})
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in math animation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Physics Sandbox
# ============================================================================

@app.post("/api/sandbox/physics/simulate")
async def physics_simulate(request: PhysicsSimRequest):
    """
    Lance une simulation physique

    Types: "projectile", "pendulum", "collision", "wave"
    """
    try:
        if not physics_sandbox:
            raise HTTPException(status_code=503, detail="Physics sandbox not initialized")

        sim_type = request.simulation_type.lower()

        if sim_type == "projectile":
            result = physics_sandbox.create_projectile_simulation(**request.parameters)
        elif sim_type == "pendulum":
            result = physics_sandbox.create_pendulum_simulation(**request.parameters)
        elif sim_type == "collision":
            result = physics_sandbox.create_collision_simulation(**request.parameters)
        elif sim_type == "wave":
            result = physics_sandbox.create_wave_simulation(**request.parameters)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown simulation type: {sim_type}")

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in physics simulation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Electronics Sandbox
# ============================================================================

@app.post("/api/sandbox/electronics/simulate")
async def electronics_simulate(request: CircuitSimRequest):
    """
    Simule un circuit électronique

    Types: "rc", "rl", "rlc", "divider", "frequency_response"
    """
    try:
        if not electronics_sandbox:
            raise HTTPException(status_code=503, detail="Electronics sandbox not initialized")

        circuit_type = request.circuit_type.lower()

        if circuit_type == "rc":
            result = electronics_sandbox.simulate_rc_circuit(**request.parameters)
        elif circuit_type == "rl":
            result = electronics_sandbox.simulate_rl_circuit(**request.parameters)
        elif circuit_type == "rlc":
            result = electronics_sandbox.simulate_rlc_circuit(**request.parameters)
        elif circuit_type == "divider":
            result = electronics_sandbox.analyze_voltage_divider(**request.parameters)
        elif circuit_type == "frequency_response":
            result = electronics_sandbox.frequency_response(**request.parameters)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown circuit type: {circuit_type}")

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in circuit simulation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Sandbox Général
# ============================================================================

@app.post("/api/sandbox/execute")
async def sandbox_execute(request: SandboxRequest):
    """
    Exécute une action dans un sandbox

    Point d'entrée unifié pour tous les sandboxes
    """
    try:
        sandbox_type = request.sandbox_type.lower()

        if sandbox_type == "math":
            if not math_sandbox:
                raise HTTPException(status_code=503, detail="Math sandbox not initialized")
            query = request.parameters.get('query', '')
            result = math_sandbox.execute(query, request.parameters)

        elif sandbox_type == "physics":
            if not physics_sandbox:
                raise HTTPException(status_code=503, detail="Physics sandbox not initialized")
            query = request.parameters.get('query', '')
            result = physics_sandbox.execute(query, request.parameters)

        elif sandbox_type == "electronics":
            if not electronics_sandbox:
                raise HTTPException(status_code=503, detail="Electronics sandbox not initialized")
            query = request.parameters.get('query', '')
            result = electronics_sandbox.execute(query, request.parameters)

        else:
            raise HTTPException(status_code=400, detail=f"Unknown sandbox type: {sandbox_type}")

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error executing sandbox: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Health Check
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "components": {
            "nyx": nyx is not None,
            "intent_system": intent_detector is not None and intent_router is not None,
            "sandboxes": {
                "math": math_sandbox is not None,
                "physics": physics_sandbox is not None,
                "electronics": electronics_sandbox is not None,
            },
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
