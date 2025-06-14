import pytest
import math

from src.utils import (
    distance, unit_vector, rotate_point, polygon_area, 
    moving_average, linear_interpolate
)


def test_distance():
    """Test Euclidean distance calculation."""
    # Basic cases
    assert distance([0, 0], [3, 4]) == 5.0
    assert distance([1, 1], [1, 1]) == 0.0
    assert distance([0, 0], [1, 0]) == 1.0
    assert distance([0, 0], [0, 1]) == 1.0
    
    # Negative coordinates
    assert distance([-1, -1], [2, 3]) == 5.0


def test_unit_vector():
    """Test unit vector calculation."""
    # Basic cases
    assert unit_vector([3, 4]) == (0.6, 0.8)
    assert unit_vector([1, 0]) == (1.0, 0.0)
    assert unit_vector([0, 1]) == (0.0, 1.0)
    
    # Zero vector
    assert unit_vector([0, 0]) == (0.0, 0.0)
    
    # Very small vector (numerical stability)
    result = unit_vector([1e-15, 1e-15])
    assert result == (0.0, 0.0)


def test_rotate_point():
    """Test point rotation."""
    # 90-degree rotation around origin
    result = rotate_point([1, 0], math.pi/2)
    assert abs(result[0]) < 1e-10  # Should be ~0
    assert abs(result[1] - 1.0) < 1e-10  # Should be ~1
    
    # 180-degree rotation
    result = rotate_point([1, 0], math.pi)
    assert abs(result[0] + 1.0) < 1e-10  # Should be ~-1
    assert abs(result[1]) < 1e-10  # Should be ~0
    
    # Rotation around custom center
    result = rotate_point([2, 1], math.pi/2, center=[1, 1])
    assert abs(result[0] - 1.0) < 1e-10  # Should be ~1
    assert abs(result[1] - 2.0) < 1e-10  # Should be ~2


def test_polygon_area():
    """Test polygon area calculation."""
    # Square
    square = [(0, 0), (1, 0), (1, 1), (0, 1)]
    assert polygon_area(square) == 1.0
    
    # Triangle
    triangle = [(0, 0), (1, 0), (0.5, 1)]
    assert polygon_area(triangle) == 0.5
    
    # Empty/degenerate cases
    assert polygon_area([]) == 0.0
    assert polygon_area([(0, 0)]) == 0.0
    assert polygon_area([(0, 0), (1, 1)]) == 0.0
    
    # Order shouldn't matter for area magnitude
    square_reversed = [(0, 1), (1, 1), (1, 0), (0, 0)]
    assert polygon_area(square_reversed) == 1.0


def test_moving_average():
    """Test moving average calculation."""
    # Basic case
    data = [1, 2, 3, 4, 5]
    result = moving_average(data, 3)
    expected = [2.0, 3.0, 4.0]  # (1+2+3)/3, (2+3+4)/3, (3+4+5)/3
    assert result == expected
    
    # Window size = 1 (should return original data)
    result = moving_average(data, 1)
    assert result == [1.0, 2.0, 3.0, 4.0, 5.0]
    
    # Window size = data length
    result = moving_average(data, 5)
    assert result == [3.0]  # Average of all elements
    
    # Edge cases
    assert moving_average([], 3) == []
    assert moving_average([1, 2], 3) == []  # Window larger than data
    assert moving_average([1, 2, 3], 0) == []  # Invalid window size


def test_linear_interpolate():
    """Test linear interpolation."""
    # Basic interpolation
    result = linear_interpolate(1.5, 1.0, 10.0, 2.0, 20.0)
    assert result == 15.0  # Midpoint
    
    # Extrapolation
    result = linear_interpolate(0.0, 1.0, 10.0, 2.0, 20.0)
    assert result == 0.0
    
    result = linear_interpolate(3.0, 1.0, 10.0, 2.0, 20.0)
    assert result == 30.0
    
    # Edge cases
    result = linear_interpolate(1.0, 1.0, 10.0, 2.0, 20.0)
    assert result == 10.0  # At first point
    
    result = linear_interpolate(2.0, 1.0, 10.0, 2.0, 20.0)
    assert result == 20.0  # At second point
    
    # Degenerate case (x1 == x2)
    result = linear_interpolate(1.5, 1.0, 10.0, 1.0, 20.0)
    assert result == 10.0  # Should return y1


def test_mathematical_consistency():
    """Test consistency between related functions."""
    # Unit vector should have length 1 (except for zero vector)
    vectors = [[3, 4], [1, 1], [-2, 5], [0.1, 0.1]]
    for v in vectors:
        unit = unit_vector(v)
        if unit != (0.0, 0.0):  # Skip zero vector case
            length = distance([0, 0], unit)
            assert abs(length - 1.0) < 1e-10, f"Unit vector {unit} should have length 1"
    
    # Rotation should preserve distance from center
    point = [3, 4]
    center = [1, 2]
    original_dist = distance(point, center)
    
    for angle in [0, math.pi/4, math.pi/2, math.pi, 3*math.pi/2]:
        rotated = rotate_point(point, angle, center)
        rotated_dist = distance(rotated, center)
        assert abs(rotated_dist - original_dist) < 1e-10, "Rotation should preserve distance"


if __name__ == "__main__":
    pytest.main([__file__]) 