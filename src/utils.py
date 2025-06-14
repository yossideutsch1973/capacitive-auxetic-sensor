"""Utility helpers used across the project.

All listed helpers are pure functions (no side-effects).
"""

from __future__ import annotations

import math
from typing import List, Sequence, Tuple

__all__ = [
    "distance",
    "unit_vector",
    "rotate_point",
    "polygon_area",
    "moving_average",
    "linear_interpolate",
]


def distance(p: Sequence[float], q: Sequence[float]) -> float:
    """Return the Euclidean distance between two points in 2-D.

    Parameters
    ----------
    p, q : Sequence[float]
        Coordinate pairs *(x, y)*.

    Returns
    -------
    float

    ASCII maths::

        d = sqrt((x2 - x1)^2 + (y2 - y1)^2)
    """

    return math.hypot(q[0] - p[0], q[1] - p[1])


def unit_vector(v: Sequence[float]) -> Tuple[float, float]:
    """Return the unit-length vector parallel to *v* in 2-D.

    Parameters
    ----------
    v : Sequence[float]
        Vector components *(x, y)*.

    Returns
    -------
    Tuple[float, float]
    
    ASCII maths::
    
        û = v / |v| = (vx, vy) / sqrt(vx² + vy²)
    """
    norm = math.hypot(v[0], v[1])
    return (v[0] / norm, v[1] / norm) if norm > 1e-12 else (0.0, 0.0)


def rotate_point(point: Sequence[float], angle: float, center: Sequence[float] = (0.0, 0.0)) -> Tuple[float, float]:
    """Rotate a point around a center by the given angle.
    
    Parameters
    ----------
    point : Sequence[float]
        Point coordinates *(x, y)*.
    angle : float
        Rotation angle in radians (counter-clockwise positive).
    center : Sequence[float], default=(0.0, 0.0)
        Center of rotation *(cx, cy)*.
        
    Returns
    -------
    Tuple[float, float]
        Rotated point coordinates.
        
    ASCII maths::
    
        x' = cx + (x - cx)*cos(θ) - (y - cy)*sin(θ)
        y' = cy + (x - cx)*sin(θ) + (y - cy)*cos(θ)
    """
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    
    # Translate to origin
    dx = point[0] - center[0]
    dy = point[1] - center[1]
    
    # Rotate and translate back
    x_rot = center[0] + dx * cos_a - dy * sin_a
    y_rot = center[1] + dx * sin_a + dy * cos_a
    
    return (x_rot, y_rot)


def polygon_area(vertices: List[Tuple[float, float]]) -> float:
    """Calculate the area of a polygon using the shoelace formula.
    
    Parameters
    ----------
    vertices : List[Tuple[float, float]]
        Polygon vertices in order (clockwise or counter-clockwise).
        
    Returns
    -------
    float
        Polygon area (always positive).
        
    ASCII maths::
    
        A = (1/2) * |Σ(xi * yi+1 - xi+1 * yi)|  (shoelace formula)
    """
    if len(vertices) < 3:
        return 0.0
        
    area = 0.0
    n = len(vertices)
    
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]
        
    return abs(area) / 2.0


def moving_average(data: Sequence[float], window_size: int) -> List[float]:
    """Calculate moving average of a data sequence.
    
    Parameters
    ----------
    data : Sequence[float]
        Input data sequence.
    window_size : int
        Size of the moving window.
        
    Returns
    -------
    List[float]
        Moving averages (length = len(data) - window_size + 1).
        
    ASCII maths::
    
        MA[i] = (1/n) * Σ(data[i:i+n])
    """
    if window_size <= 0 or window_size > len(data):
        return []
        
    result = []
    for i in range(len(data) - window_size + 1):
        window_sum = sum(data[i:i + window_size])
        result.append(window_sum / window_size)
        
    return result


def linear_interpolate(x: float, x1: float, y1: float, x2: float, y2: float) -> float:
    """Linear interpolation between two points.
    
    Parameters
    ----------
    x : float
        Input value to interpolate.
    x1, y1 : float
        First point coordinates.
    x2, y2 : float
        Second point coordinates.
        
    Returns
    -------
    float
        Interpolated y-value.
        
    ASCII maths::
    
        y = y1 + (y2 - y1) * (x - x1) / (x2 - x1)
    """
    if abs(x2 - x1) < 1e-12:
        return y1  # Avoid division by zero
        
    return y1 + (y2 - y1) * (x - x1) / (x2 - x1) 