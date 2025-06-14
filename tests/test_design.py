import pytest
import math

from src.design import generate_reentrant_cell, calculate_poisson_ratio, estimate_capacitance_change


def test_generate_reentrant_cell_structure():
    """Test that generate_reentrant_cell returns correct structure."""
    cell = generate_reentrant_cell(1.0, 0.1, 30.0)

    assert isinstance(cell, dict)
    assert set(cell.keys()) == {"nodes", "edges"}, "Expected keys 'nodes' and 'edges'"
    assert isinstance(cell["nodes"], list)
    assert isinstance(cell["edges"], list)


def test_generate_reentrant_cell_geometry():
    """Test geometric properties of generated cell."""
    a, b, alpha = 1.0, 0.1, 30.0
    cell = generate_reentrant_cell(a, b, alpha)
    
    nodes = cell["nodes"]
    edges = cell["edges"]
    
    # Should have 8 nodes for re-entrant cell
    assert len(nodes) == 8, f"Expected 8 nodes, got {len(nodes)}"
    
    # Should have 8 edges forming closed loop
    assert len(edges) == 8, f"Expected 8 edges, got {len(edges)}"
    
    # All nodes should be 2D coordinates
    for i, node in enumerate(nodes):
        assert len(node) == 2, f"Node {i} should be 2D coordinate"
        assert all(isinstance(coord, (int, float)) for coord in node), f"Node {i} coordinates should be numeric"
    
    # All edges should be valid node index pairs
    for i, edge in enumerate(edges):
        assert len(edge) == 2, f"Edge {i} should connect two nodes"
        start, end = edge
        assert 0 <= start < len(nodes), f"Edge {i} start index {start} out of range"
        assert 0 <= end < len(nodes), f"Edge {i} end index {end} out of range"


def test_generate_reentrant_cell_parameters():
    """Test cell generation with different parameters."""
    # Test with different angles
    for alpha in [15.0, 30.0, 45.0, 60.0]:
        cell = generate_reentrant_cell(1.0, 0.1, alpha)
        assert len(cell["nodes"]) == 8
        assert len(cell["edges"]) == 8
    
    # Test with different sizes
    for a in [0.5, 1.0, 2.0]:
        cell = generate_reentrant_cell(a, 0.1, 30.0)
        assert len(cell["nodes"]) == 8
        
    # Test with different wall thickness
    for b in [0.05, 0.1, 0.2]:
        cell = generate_reentrant_cell(1.0, b, 30.0)
        assert len(cell["nodes"]) == 8


def test_calculate_poisson_ratio():
    """Test Poisson's ratio calculation for auxetic behavior."""
    # Test typical auxetic angles
    nu_30 = calculate_poisson_ratio(1.0, 30.0)
    assert nu_30 < 0, "Poisson's ratio should be negative for auxetic behavior"
    assert -1 < nu_30 < 0, f"Poisson's ratio {nu_30} should be between -1 and 0"
    
    nu_45 = calculate_poisson_ratio(1.0, 45.0)
    assert nu_45 < 0, "Poisson's ratio should be negative for auxetic behavior"
    
    # Test that larger angles give more negative ratios (larger absolute value)
    nu_15 = calculate_poisson_ratio(1.0, 15.0)
    assert nu_15 > nu_30, "Larger angles should give more negative Poisson's ratio"
    assert nu_30 > nu_45, "Larger angles should give more negative Poisson's ratio"


def test_calculate_poisson_ratio_edge_cases():
    """Test edge cases for Poisson's ratio calculation."""
    # Test near-degenerate case (alpha close to 180°)
    nu_179 = calculate_poisson_ratio(1.0, 179.0)
    assert nu_179 < -10, "Should approach negative infinity as alpha approaches 180°"
    
    # Test zero angle
    nu_0 = calculate_poisson_ratio(1.0, 0.0)
    assert nu_0 == 0.0, "Zero angle should give zero Poisson's ratio"
    
    # Test 90 degree angle
    nu_90 = calculate_poisson_ratio(1.0, 90.0)
    assert abs(nu_90 + 1.0) < 1e-10, "90° angle should give Poisson's ratio of -1"


def test_estimate_capacitance_change():
    """Test capacitance change estimation."""
    # Test with typical auxetic material
    poisson_ratio = -0.5  # Typical auxetic value
    strain = 0.01  # 1% strain
    initial_gap = 1e-3  # 1mm gap
    
    delta_c = estimate_capacitance_change(initial_gap, strain, poisson_ratio)
    
    # For auxetic materials under tension:
    # - Area increases (positive contribution to capacitance)
    # - Gap increases (negative contribution to capacitance)
    # Net effect depends on relative magnitudes
    assert isinstance(delta_c, float), "Should return numeric value"
    
    # Test that larger strain gives larger change
    delta_c_small = estimate_capacitance_change(initial_gap, 0.005, poisson_ratio)
    delta_c_large = estimate_capacitance_change(initial_gap, 0.02, poisson_ratio)
    # Allow for the case where both might be zero due to cancellation
    if abs(delta_c_small) > 1e-10 or abs(delta_c_large) > 1e-10:
        assert abs(delta_c_large) >= abs(delta_c_small), "Larger strain should give larger or equal capacitance change"


def test_estimate_capacitance_change_sign():
    """Test sign of capacitance change for different scenarios."""
    initial_gap = 1e-3
    strain = 0.01
    
    # Conventional material (positive Poisson's ratio)
    conventional_nu = 0.3
    delta_c_conv = estimate_capacitance_change(initial_gap, strain, conventional_nu)
    
    # Auxetic material (negative Poisson's ratio)
    auxetic_nu = -0.5
    delta_c_aux = estimate_capacitance_change(initial_gap, strain, auxetic_nu)
    
    # Auxetic should have different (likely larger positive) capacitance change
    assert delta_c_aux != delta_c_conv, "Auxetic and conventional materials should behave differently"


def test_mathematical_consistency():
    """Test mathematical consistency between functions."""
    a, b, alpha = 1.0, 0.1, 30.0
    
    # Generate cell and calculate Poisson's ratio
    cell = generate_reentrant_cell(a, b, alpha)
    nu = calculate_poisson_ratio(a, alpha)
    
    # Both should be consistent with the same angle
    assert len(cell["nodes"]) > 0, "Cell should have nodes"
    assert nu < 0, "Should be auxetic for this angle"
    
    # Test capacitance estimation with calculated Poisson's ratio
    delta_c = estimate_capacitance_change(1e-3, 0.01, nu)
    assert isinstance(delta_c, float), "Should return valid capacitance change"


if __name__ == "__main__":
    pytest.main([__file__]) 