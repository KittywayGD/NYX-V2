"""
Sandboxes Interactifs pour NYX-V2
Modules de visualisation et simulation pour chaque domaine
"""

from .math_sandbox import MathSandbox
from .physics_sandbox import PhysicsSandbox
from .electronics_sandbox import ElectronicsSandbox

__all__ = ['MathSandbox', 'PhysicsSandbox', 'ElectronicsSandbox']
