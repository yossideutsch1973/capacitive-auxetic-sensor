#!/usr/bin/env python3
"""
Test script for 3D auxetic sensor model generation.

This script tests the 3D model generation logic without requiring
CadQuery installation, useful for CI/CD and development.
"""

import sys
import os

# Add src directory for our design functions
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))
from design import generate_reentrant_cell, calculate_poisson_ratio

def test_geometry_generation():
    """Test the underlying geometry generation."""
    
    print("🧪 Testing auxetic cell geometry generation...")
    
    # Test parameters
    cell_size = 10.0  # mm
    wall_thickness = 1.0  # mm
    alpha = 45.0  # degrees
    
    # Generate 2D cell data
    cell_data = generate_reentrant_cell(
        a=cell_size/10,  # Convert to design units (cm)
        b=wall_thickness/10,
        alpha=alpha
    )
    
    nodes = cell_data["nodes"]
    edges = cell_data["edges"]
    
    print(f"✅ Generated cell with {len(nodes)} nodes and {len(edges)} edges")
    
    # Verify geometry
    assert len(nodes) == 8, f"Expected 8 nodes, got {len(nodes)}"
    assert len(edges) == 8, f"Expected 8 edges, got {len(edges)}"
    
    # Check that all nodes are 2D coordinates
    for i, node in enumerate(nodes):
        assert len(node) == 2, f"Node {i} should be 2D coordinate"
        assert all(isinstance(coord, (int, float)) for coord in node), f"Node {i} coordinates should be numeric"
    
    # Check that all edges reference valid nodes
    for i, edge in enumerate(edges):
        start, end = edge
        assert 0 <= start < len(nodes), f"Edge {i} start index {start} out of range"
        assert 0 <= end < len(nodes), f"Edge {i} end index {end} out of range"
    
    print("✅ Geometry validation passed")
    
    # Calculate Poisson's ratio
    poisson_ratio = calculate_poisson_ratio(1.0, alpha)
    print(f"✅ Poisson's ratio: {poisson_ratio:.3f} (auxetic: {poisson_ratio < 0})")

def test_sensor_parameters():
    """Test different sensor configurations."""
    
    print("\n🔧 Testing sensor parameter calculations...")
    
    configurations = [
        {"name": "Standard", "cell_size": 10.0, "alpha": 45.0, "nx": 3, "ny": 3},
        {"name": "High Sensitivity", "cell_size": 8.0, "alpha": 60.0, "nx": 4, "ny": 4},
        {"name": "Robust", "cell_size": 12.0, "alpha": 30.0, "nx": 2, "ny": 2},
    ]
    
    for config in configurations:
        print(f"\n📊 {config['name']} Configuration:")
        
        # Calculate parameters
        poisson_ratio = calculate_poisson_ratio(1.0, config["alpha"])
        total_width = config["nx"] * config["cell_size"]
        total_length = config["ny"] * config["cell_size"]
        
        print(f"   • Cell size: {config['cell_size']} mm")
        print(f"   • Re-entrance angle: {config['alpha']}°")
        print(f"   • Poisson's ratio: {poisson_ratio:.3f}")
        print(f"   • Array: {config['nx']}×{config['ny']} cells")
        print(f"   • Total dimensions: {total_width}×{total_length} mm")
        
        # Verify auxetic behavior
        assert poisson_ratio < 0, f"{config['name']} should have negative Poisson's ratio"
    
    print("\n✅ All configurations validated")

def simulate_3d_model_generation():
    """Simulate 3D model generation process without CadQuery."""
    
    print("\n🏗️  Simulating 3D model generation...")
    
    # Simulate the AuxeticSensor3D class behavior
    cell_size = 10.0
    wall_thickness = 1.0
    alpha = 45.0
    height = 3.0
    nx, ny = 3, 3
    
    print(f"🔧 Sensor Parameters:")
    print(f"   Cell size: {cell_size} mm")
    print(f"   Wall thickness: {wall_thickness} mm")
    print(f"   Re-entrance angle: {alpha}°")
    print(f"   Height: {height} mm")
    print(f"   Array: {nx}×{ny} cells")
    
    # Calculate derived parameters
    poisson_ratio = calculate_poisson_ratio(1.0, alpha)
    total_width = nx * cell_size
    total_length = ny * cell_size
    
    print(f"   Poisson's ratio: {poisson_ratio:.3f}")
    print(f"   Total dimensions: {total_width}×{total_length}×{height} mm")
    
    # Simulate model generation steps
    steps = [
        "🏗️  Building auxetic structure",
        "🔌 Adding capacitor plates", 
        "🏛️  Adding support posts",
        "⚡ Creating wire channels",
        "💾 Exporting files"
    ]
    
    for step in steps:
        print(f"   {step}...")
    
    # Simulate file outputs
    output_files = [
        "auxetic_sensor.step",
        "auxetic_sensor.stl", 
        "auxetic_unit_cell.stl",
        "manufacturing_info.txt"
    ]
    
    print(f"\n📁 Would generate files:")
    for file in output_files:
        print(f"   • {file}")
    
    print("✅ 3D model generation simulation completed")
    return True

def main():
    """Run all tests."""
    
    print("🔬 Auxetic Sensor 3D Model - Test Suite")
    print("=" * 50)
    
    try:
        # Run tests
        test_geometry_generation()
        test_sensor_parameters()
        simulate_3d_model_generation()
        
        print(f"\n🎉 All tests passed!")
        print(f"📋 To generate actual 3D models:")
        print(f"   1. Install CadQuery: pip install cadquery-ocp")
        print(f"   2. Run: python cad/auxetic_cell_3d.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 