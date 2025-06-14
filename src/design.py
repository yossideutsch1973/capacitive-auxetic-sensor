"""Design utilities for the re-entrant auxetic unit cell.

All public functions are *pure*: they depend only on their inputs and
produce deterministic outputs without side-effects.
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple

__all__ = [
    "generate_reentrant_cell",
    "calculate_poisson_ratio",
    "estimate_capacitance_change",
]


def generate_reentrant_cell(a: float, b: float, alpha: float) -> Dict[str, List[Tuple[float, float]]]:
    """Return the *topology* of a single 2-D re-entrant auxetic unit cell.

    Parameters
    ----------
    a : float
        Side length of the undeformed square cell (m).
    b : float
        Wall thickness (m).
    alpha : float
        Re-entrance angle (degrees).

    Returns
    -------
    Dict[str, List[Tuple[float, float]]]
        ``{"nodes": [...], "edges": [...]}`` where
        ``nodes`` is a list of *(x, y)* coordinates and ``edges`` a list of
        *(start_index, end_index)* pairs.

    Notes
    -----
    ASCII symbolic form::

        x_i = a * cos(alpha_rad)
        y_i = a * sin(alpha_rad)
        
    Re-entrant structure creates negative Poisson's ratio through
    geometric transformation under load.
    """
    alpha_rad = math.radians(alpha)
    
    # Calculate key geometric parameters
    # L = horizontal projection of angled strut
    L = a * math.cos(alpha_rad)
    # H = vertical projection of angled strut  
    H = a * math.sin(alpha_rad)
    
    # Define the 8 key nodes of the re-entrant cell
    # Starting from bottom-left, going counter-clockwise
    nodes: List[Tuple[float, float]] = [
        (0.0, 0.0),                    # 0: bottom-left corner
        (L, 0.0),                      # 1: bottom inner corner
        (L, H),                        # 2: bottom-right of vertical strut
        (L + b, H),                    # 3: top-right of vertical strut
        (L + b, H + b),                # 4: top-right corner
        (L, H + b),                    # 5: top inner corner
        (L, 2*H + b),                  # 6: top-left of vertical strut
        (0.0, 2*H + b),                # 7: top-left corner
    ]
    
    # Define edges connecting the nodes to form the re-entrant structure
    edges: List[Tuple[int, int]] = [
        (0, 1),  # bottom horizontal
        (1, 2),  # angled strut (bottom)
        (2, 3),  # vertical strut (bottom)
        (3, 4),  # top horizontal (right)
        (4, 5),  # top horizontal (left)
        (5, 6),  # vertical strut (top)
        (6, 7),  # angled strut (top)
        (7, 0),  # left vertical
    ]

    return {"nodes": nodes, "edges": edges}


def calculate_poisson_ratio(a: float, alpha: float, strain: float = 0.01) -> float:
    """Calculate theoretical Poisson's ratio for re-entrant auxetic structure.
    
    Parameters
    ----------
    a : float
        Side length of undeformed cell (m).
    alpha : float
        Re-entrance angle (degrees).
    strain : float, default=0.01
        Applied strain for calculation.
        
    Returns
    -------
    float
        Poisson's ratio (negative for auxetic behavior).
        
    Notes
    -----
    ASCII symbolic form::
    
        ν = -ε_transverse / ε_longitudinal
        ν ≈ -sin(α) / (1 + cos(α))  for small strains
    """
    alpha_rad = math.radians(alpha)
    
    # Theoretical Poisson's ratio for re-entrant structure
    # Negative value indicates auxetic behavior
    cos_alpha = math.cos(alpha_rad)
    sin_alpha = math.sin(alpha_rad)
    
    if abs(1 + cos_alpha) < 1e-10:
        return float('-inf')  # Degenerate case
        
    return -sin_alpha / (1 + cos_alpha)


def estimate_capacitance_change(
    initial_gap: float, 
    strain: float, 
    poisson_ratio: float,
    dielectric_constant: float = 1.0
) -> float:
    """Estimate relative capacitance change due to auxetic deformation.
    
    Parameters
    ----------
    initial_gap : float
        Initial capacitor gap distance (m).
    strain : float
        Applied longitudinal strain.
    poisson_ratio : float
        Material Poisson's ratio (negative for auxetic).
    dielectric_constant : float, default=1.0
        Relative permittivity of gap medium.
        
    Returns
    -------
    float
        Relative capacitance change ΔC/C₀.
        
    Notes
    -----
    ASCII symbolic form::
    
        C = ε₀ * ε_r * A / d
        ΔC/C₀ = ΔA/A₀ - Δd/d₀
        
    For auxetic materials: ΔA/A₀ = 2*ν*ε (area increases under tension)
    """
    # Transverse strain (width change)
    transverse_strain = -poisson_ratio * strain
    
    # Area change: ΔA/A₀ ≈ 2 * transverse_strain for small strains
    area_change_ratio = 2 * transverse_strain
    
    # Gap change (assuming gap scales with longitudinal dimension)
    gap_change_ratio = strain
    
    # Capacitance change: C ∝ A/d
    capacitance_change_ratio = area_change_ratio - gap_change_ratio
    
    return capacitance_change_ratio