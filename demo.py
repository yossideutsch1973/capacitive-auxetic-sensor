#!/usr/bin/env python3
"""
Capacitive Auxetic Sensor - Complete Demonstration

This script demonstrates all implemented functionality of the capacitive
auxetic sensor project, including design generation, analysis, and simulation.
"""

import numpy as np
import matplotlib.pyplot as plt
from src.design import generate_reentrant_cell, calculate_poisson_ratio, estimate_capacitance_change
from src.utils import polygon_area, distance, moving_average
from src.test_setup import MockLCRMeter, read_capacitance, calibrate_sensor, log_measurement_series

def main():
    print("🔬 Capacitive Auxetic Sensor - Complete Demonstration")
    print("=" * 60)
    
    # 1. Design Generation
    print("\n1. 📐 AUXETIC CELL DESIGN")
    print("-" * 30)
    
    # Generate different cell designs
    designs = [
        {"a": 1.0, "b": 0.1, "alpha": 30.0, "name": "Conservative"},
        {"a": 1.0, "b": 0.1, "alpha": 45.0, "name": "Balanced"},
        {"a": 1.0, "b": 0.1, "alpha": 60.0, "name": "Aggressive"},
    ]
    
    for design in designs:
        cell = generate_reentrant_cell(design["a"], design["b"], design["alpha"])
        area = polygon_area(cell["nodes"])
        nu = calculate_poisson_ratio(design["a"], design["alpha"])
        
        print(f"{design['name']} Design (α={design['alpha']}°):")
        print(f"  • Nodes: {len(cell['nodes'])}, Edges: {len(cell['edges'])}")
        print(f"  • Cell Area: {area:.4f} m²")
        print(f"  • Poisson's Ratio: {nu:.3f} (auxetic: {nu < 0})")
        print()
    
    # 2. Performance Analysis
    print("2. 📊 PERFORMANCE ANALYSIS")
    print("-" * 30)
    
    # Compare sensor sensitivity
    strains = np.linspace(0, 0.05, 20)  # 0-5% strain
    initial_gap = 1e-3  # 1mm
    
    plt.figure(figsize=(15, 10))
    
    # Plot 1: Poisson's ratio vs angle
    plt.subplot(2, 3, 1)
    angles = np.linspace(10, 80, 50)
    poisson_ratios = [calculate_poisson_ratio(1.0, alpha) for alpha in angles]
    plt.plot(angles, poisson_ratios, 'b-', linewidth=2)
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    plt.xlabel('Re-entrance Angle (°)')
    plt.ylabel("Poisson's Ratio")
    plt.title('Auxetic Behavior')
    plt.grid(True, alpha=0.3)
    
    # Plot 2: Capacitance response
    plt.subplot(2, 3, 2)
    colors = ['blue', 'green', 'red']
    for i, design in enumerate(designs):
        nu = calculate_poisson_ratio(design["a"], design["alpha"])
        cap_changes = [estimate_capacitance_change(initial_gap, strain, nu) * 100 
                      for strain in strains]
        plt.plot(strains * 100, cap_changes, color=colors[i], linewidth=2, 
                label=f'{design["name"]} (α={design["alpha"]}°)')
    
    plt.xlabel('Applied Strain (%)')
    plt.ylabel('Capacitance Change (%)')
    plt.title('Sensor Response')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 3: Cell visualization
    plt.subplot(2, 3, 3)
    cell_45 = generate_reentrant_cell(1.0, 0.1, 45.0)
    nodes = np.array(cell_45["nodes"])
    edges = cell_45["edges"]
    
    for edge in edges:
        start, end = edge
        x_coords = [nodes[start][0], nodes[end][0]]
        y_coords = [nodes[start][1], nodes[end][1]]
        plt.plot(x_coords, y_coords, 'b-', linewidth=3)
    
    plt.scatter(nodes[:, 0], nodes[:, 1], c='red', s=50, zorder=5)
    plt.axis('equal')
    plt.title('Re-entrant Cell (α=45°)')
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    plt.grid(True, alpha=0.3)
    
    # 3. Mock Measurement Simulation
    print("3. 🔬 MEASUREMENT SIMULATION")
    print("-" * 30)
    
    # Initialize mock instrument
    mock_lcr = MockLCRMeter(base_capacitance=10e-12)  # 10pF
    print(f"Mock LCR Meter initialized: {mock_lcr.base_capacitance*1e12:.1f} pF baseline")
    
    # Single measurement
    single_cap = read_capacitance(mock_lcr)
    print(f"Single measurement: {single_cap*1e12:.3f} pF")
    
    # Calibration simulation
    reference_loads = [0.0, 0.5, 1.0, 1.5, 2.0]  # N
    print(f"\nCalibrating with loads: {reference_loads} N")
    cal_data = calibrate_sensor(mock_lcr, reference_loads, num_samples=3)
    
    # Plot 4: Calibration curve
    plt.subplot(2, 3, 4)
    plt.plot(cal_data["loads"], np.array(cal_data["capacitances"]) * 1e12, 'go-', linewidth=2)
    plt.xlabel('Applied Load (N)')
    plt.ylabel('Capacitance (pF)')
    plt.title('Calibration Curve')
    plt.grid(True, alpha=0.3)
    
    # Time series measurement
    print("\nLogging time series (2 seconds)...")
    time_data = log_measurement_series(mock_lcr, duration=2.0, sample_rate=20.0)
    
    if time_data:
        timestamps, capacitances = zip(*time_data)
        capacitances_pf = np.array(capacitances) * 1e12
        
        # Plot 5: Time series
        plt.subplot(2, 3, 5)
        plt.plot(timestamps, capacitances_pf, 'g-', linewidth=1)
        plt.xlabel('Time (s)')
        plt.ylabel('Capacitance (pF)')
        plt.title('Time Series Measurement')
        plt.grid(True, alpha=0.3)
        
        # Plot 6: Moving average
        plt.subplot(2, 3, 6)
        smoothed = moving_average(capacitances_pf, window_size=5)
        smooth_times = timestamps[2:-2]  # Adjust for window
        plt.plot(timestamps, capacitances_pf, 'lightgray', alpha=0.5, label='Raw')
        plt.plot(smooth_times, smoothed, 'darkgreen', linewidth=2, label='Smoothed')
        plt.xlabel('Time (s)')
        plt.ylabel('Capacitance (pF)')
        plt.title('Signal Processing')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        print(f"Collected {len(time_data)} samples")
        print(f"Average capacitance: {np.mean(capacitances_pf):.3f} pF")
        print(f"Noise level: {np.std(capacitances_pf):.3f} pF")
    
    plt.tight_layout()
    plt.show()
    
    # 4. Performance Summary
    print("\n4. 📈 PERFORMANCE SUMMARY")
    print("-" * 30)
    
    print("Design Comparison:")
    print(f"{'Design':<12} {'Angle':<8} {'Poisson':<10} {'Sensitivity':<12} {'Max Change'}")
    print("-" * 60)
    
    for design in designs:
        nu = calculate_poisson_ratio(design["a"], design["alpha"])
        sensitivity = estimate_capacitance_change(initial_gap, 0.001, nu) / 0.001 * 100
        max_change = estimate_capacitance_change(initial_gap, 0.05, nu) * 100
        
        print(f"{design['name']:<12} {design['alpha']:<8.0f}° {nu:<10.3f} "
              f"{sensitivity:<12.2f}%/% {max_change:<10.2f}%")
    
    print("\nRecommendation: 45° design offers good balance of sensitivity and manufacturability")
    
    # 5. Utility Functions Demo
    print("\n5. 🔧 UTILITY FUNCTIONS")
    print("-" * 30)
    
    # Geometric calculations
    p1, p2 = [0, 0], [3, 4]
    dist = distance(p1, p2)
    print(f"Distance between {p1} and {p2}: {dist:.2f}")
    
    # Area calculation
    square = [(0, 0), (1, 0), (1, 1), (0, 1)]
    area = polygon_area(square)
    print(f"Unit square area: {area:.2f}")
    
    # Signal processing
    noisy_data = [1 + 0.1*np.random.randn() for _ in range(10)]
    smoothed_data = moving_average(noisy_data, 3)
    print(f"Smoothed {len(noisy_data)} points to {len(smoothed_data)} points")
    
    print("\n✅ Demonstration complete!")
    print("🚀 Ready for real-world implementation!")

if __name__ == "__main__":
    main() 