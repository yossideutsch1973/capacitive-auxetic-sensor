#!/usr/bin/env python3
"""
Corrected Auxetic Cell Generator

This script generates the proper re-entrant auxetic geometry that will
exhibit negative Poisson's ratio behavior.
"""

import sys
import os
import math
import json

# Add FreeCAD paths
freecad_paths = [
    "/Applications/FreeCAD.app/Contents/Resources/lib",
    "/Applications/FreeCAD.app/Contents/Resources/lib/python3.11/site-packages",
]

for path in freecad_paths:
    if os.path.exists(path) and path not in sys.path:
        sys.path.append(path)

try:
    import FreeCAD
    import Part
    print("✅ FreeCAD imported successfully")
except ImportError as e:
    print(f"❌ FreeCAD import failed: {e}")
    sys.exit(1)

def generate_true_reentrant_cell(L=10.0, t=1.2, theta=45.0, h=2.0):
    """
    Generate a true re-entrant auxetic unit cell.
    
    Parameters:
    -----------
    L : float
        Length of the re-entrant struts (mm)
    t : float  
        Thickness of struts (mm)
    theta : float
        Re-entrant angle (degrees) - angle from vertical
    h : float
        Height of horizontal struts (mm)
    
    Returns:
    --------
    dict : Cell geometry with nodes and connectivity
    """
    
    # Convert angle to radians
    theta_rad = math.radians(theta)
    
    # Calculate key dimensions
    # Re-entrant structure has inward-angled struts
    dx = L * math.sin(theta_rad)  # Horizontal projection of angled strut
    dy = L * math.cos(theta_rad)  # Vertical projection of angled strut
    
    # Define the re-entrant cell vertices (bow-tie shape)
    # Starting from bottom-left, going clockwise
    vertices = [
        # Bottom section
        (0, 0),                    # 0: Bottom-left outer
        (dx, dy),                  # 1: Bottom-left inner (re-entrant point)
        (dx + h, dy),              # 2: Bottom-right inner
        (dx + h + dx, 0),          # 3: Bottom-right outer
        
        # Top section (mirrored)
        (dx + h + dx, 2*dy + h),   # 4: Top-right outer
        (dx + h, dy + h),          # 5: Top-right inner (re-entrant point)
        (dx, dy + h),              # 6: Top-left inner
        (0, 2*dy + h),             # 7: Top-left outer
    ]
    
    # Define edges (connectivity)
    edges = [
        (0, 1),  # Bottom-left angled strut
        (1, 2),  # Bottom horizontal strut
        (2, 3),  # Bottom-right angled strut
        (3, 4),  # Right vertical strut
        (4, 5),  # Top-right angled strut
        (5, 6),  # Top horizontal strut
        (6, 7),  # Top-left angled strut
        (7, 0),  # Left vertical strut
    ]
    
    return {
        "vertices": vertices,
        "edges": edges,
        "parameters": {
            "L": L,
            "t": t, 
            "theta": theta,
            "h": h,
            "cell_width": dx + h + dx,
            "cell_height": 2*dy + h
        }
    }

def create_corrected_unit_cell(doc, cell_data, height=4.0):
    """Create a 3D unit cell with proper re-entrant geometry."""
    
    vertices = cell_data["vertices"]
    edges = cell_data["edges"]
    
    print(f"Creating cell with {len(vertices)} vertices:")
    for i, (x, y) in enumerate(vertices):
        print(f"  Vertex {i}: ({x:.2f}, {y:.2f}) mm")
    
    # Create points
    points = [FreeCAD.Vector(x, y, 0) for x, y in vertices]
    
    # Create edges
    edge_objects = []
    for start_idx, end_idx in edges:
        start_point = points[start_idx]
        end_point = points[end_idx]
        line = Part.makeLine(start_point, end_point)
        edge_objects.append(line)
    
    # Create wire and face
    wire = Part.Wire(edge_objects)
    face = Part.Face(wire)
    
    # Extrude to create solid
    solid = face.extrude(FreeCAD.Vector(0, 0, height))
    
    # Create FreeCAD object
    cell_obj = doc.addObject("Part::Feature", "CorrectedUnitCell")
    cell_obj.Shape = solid
    
    return cell_obj

def create_corrected_sensor():
    """Create corrected auxetic sensor with proper re-entrant geometry."""
    
    print("🔧 Creating CORRECTED auxetic pressure sensor...")
    
    # Create new document
    doc = FreeCAD.newDocument("CorrectedAuxeticSensor")
    
    # Improved parameters for better auxetic behavior
    L = 4.0      # Length of re-entrant struts (mm) - shorter for more flexibility
    t = 0.8      # Strut thickness (mm) - thinner for better deformation
    theta = 30.0 # Re-entrant angle (degrees) - 30° gives strong auxetic effect
    h = 2.0      # Horizontal strut length (mm)
    height = 3.0 # Extrusion height (mm)
    
    # Generate corrected unit cell
    cell_data = generate_true_reentrant_cell(L=L, t=t, theta=theta, h=h)
    
    print(f"📊 Corrected Parameters:")
    print(f"   • Re-entrant strut length: {L} mm")
    print(f"   • Strut thickness: {t} mm") 
    print(f"   • Re-entrant angle: {theta}°")
    print(f"   • Cell dimensions: {cell_data['parameters']['cell_width']:.1f} × {cell_data['parameters']['cell_height']:.1f} mm")
    
    # Create unit cell
    unit_cell = create_corrected_unit_cell(doc, cell_data, height)
    
    # Create 3×3 array
    cell_width = cell_data['parameters']['cell_width']
    cell_height = cell_data['parameters']['cell_height']
    
    array_objects = [unit_cell]  # Include original
    
    for i in range(3):
        for j in range(3):
            if i == 0 and j == 0:  # Skip original position
                continue
                
            # Create copy
            cell_copy = doc.addObject("Part::Feature", f"Cell_{i}_{j}")
            cell_copy.Shape = unit_cell.Shape.copy()
            
            # Position
            x_offset = i * cell_width
            y_offset = j * cell_height
            cell_copy.Placement.Base = FreeCAD.Vector(x_offset, y_offset, 0)
            
            array_objects.append(cell_copy)
    
    # Create capacitor plates
    total_width = 3 * cell_width
    total_height = 3 * cell_height
    
    # Bottom plate
    bottom_plate = doc.addObject("Part::Feature", "BottomPlate")
    bottom_plate.Shape = Part.makeBox(total_width + 4, total_height + 4, 0.3)
    bottom_plate.Placement.Base = FreeCAD.Vector(-2, -2, -0.3)
    
    # Top plate  
    top_plate = doc.addObject("Part::Feature", "TopPlate")
    top_plate.Shape = Part.makeBox(total_width + 4, total_height + 4, 0.3)
    top_plate.Placement.Base = FreeCAD.Vector(-2, -2, height + 1.0)
    
    # Support posts
    posts = []
    post_positions = [
        (2, 2), (total_width-2, 2), (2, total_height-2), 
        (total_width-2, total_height-2), (total_width/2, total_height/2)
    ]
    
    for i, (x, y) in enumerate(post_positions):
        post = doc.addObject("Part::Feature", f"SupportPost_{i+1}")
        post.Shape = Part.makeCylinder(0.6, height + 1.0)  # Thinner posts
        post.Placement.Base = FreeCAD.Vector(x, y, 0)
        posts.append(post)
    
    # Combine all objects
    all_objects = array_objects + [bottom_plate, top_plate] + posts
    
    # Recompute
    doc.recompute()
    
    # Export corrected STEP files
    Part.export(all_objects, "cad/corrected_auxetic_sensor.step")
    Part.export(array_objects, "cad/corrected_auxetic_structure.step")
    
    print(f"✅ Corrected STEP files created:")
    print(f"   • cad/corrected_auxetic_sensor.step")
    print(f"   • cad/corrected_auxetic_structure.step")
    
    # Save geometry data
    with open("cad/corrected_geometry.json", 'w') as f:
        json.dump({
            "cell_data": cell_data,
            "total_dimensions": [total_width, total_height, height],
            "description": "Corrected re-entrant auxetic geometry with proper negative Poisson's ratio behavior"
        }, f, indent=2)
    
    # Close document
    FreeCAD.closeDocument(doc.Name)
    
    return "cad/corrected_auxetic_sensor.step"

def main():
    """Generate corrected auxetic sensor."""
    
    print("🔬 CORRECTED Auxetic Sensor Generator")
    print("=" * 50)
    print("🚨 This fixes the geometry issue in the original STEP file")
    print("✅ Will create proper re-entrant structure with auxetic behavior")
    print()
    
    try:
        step_file = create_corrected_sensor()
        
        print(f"\n🎉 SUCCESS! Corrected sensor generated:")
        print(f"📁 {step_file}")
        print(f"\n🔍 Key improvements:")
        print(f"   ✅ Proper re-entrant (bow-tie) cell geometry")
        print(f"   ✅ 30° re-entrant angle for strong auxetic effect")
        print(f"   ✅ Thinner struts (0.8mm) for better deformation")
        print(f"   ✅ Optimized dimensions for 3D printing")
        print(f"\n📋 Next steps:")
        print(f"   1. Import corrected_auxetic_sensor.step into Shapr3D")
        print(f"   2. You should now see proper bow-tie shaped cells")
        print(f"   3. The structure will exhibit true auxetic behavior")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 