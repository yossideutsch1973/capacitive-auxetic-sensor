#!/usr/bin/env python3
"""
FreeCAD STEP File Generator for Auxetic Pressure Sensor

This script uses FreeCAD to create a proper STEP file of the auxetic sensor.
"""

import sys
import os
import json

# Add FreeCAD to Python path
freecad_paths = [
    "/Applications/FreeCAD.app/Contents/Resources/lib",
    "/Applications/FreeCAD.app/Contents/Resources/lib/python3.11/site-packages",
    "/usr/lib/freecad/lib",
    "/usr/lib/freecad-python3/lib"
]

for path in freecad_paths:
    if os.path.exists(path) and path not in sys.path:
        sys.path.append(path)

# Add src directory for our design functions
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

try:
    import FreeCAD
    import Part
    import Draft
    print("✅ FreeCAD imported successfully")
except ImportError as e:
    print(f"❌ FreeCAD import failed: {e}")
    print("💡 Try running FreeCAD GUI first, then run this script")
    sys.exit(1)

from design import generate_reentrant_cell, calculate_poisson_ratio

def create_auxetic_sensor_step():
    """Create a complete auxetic sensor and export as STEP file."""
    
    print("🔧 Creating auxetic pressure sensor in FreeCAD...")
    
    # Create new document
    doc = FreeCAD.newDocument("AuxeticSensor")
    
    # Sensor parameters
    cell_size = 10.0  # mm
    wall_thickness = 1.2  # mm
    alpha = 45.0  # degrees
    height = 4.0  # mm
    nx, ny = 3, 3  # 3x3 array
    
    print(f"📊 Parameters: {cell_size}mm cells, {alpha}° angle, {nx}×{ny} array")
    
    # Generate unit cell geometry
    cell_data = generate_reentrant_cell(
        a=cell_size/10,  # Convert to design units (cm)
        b=wall_thickness/10,
        alpha=alpha
    )
    
    nodes_2d = [(x*10, y*10) for x, y in cell_data["nodes"]]  # Convert to mm
    edges = cell_data["edges"]
    
    print(f"✅ Unit cell: {len(nodes_2d)} nodes, {len(edges)} edges")
    
    # Create unit cell profile
    unit_cell = create_unit_cell_profile(doc, nodes_2d, edges, height)
    
    # Create 3x3 array
    auxetic_array = create_auxetic_array(doc, unit_cell, nx, ny, cell_size)
    
    # Create capacitor plates
    bottom_plate, top_plate = create_capacitor_plates(doc, nx * cell_size, ny * cell_size, height)
    
    # Create support posts
    support_posts = create_support_posts(doc, nx * cell_size, ny * cell_size, height)
    
    # Combine all parts
    all_objects = auxetic_array + [bottom_plate, top_plate] + support_posts
    
    # Create compound
    compound = doc.addObject("Part::Compound", "AuxeticSensor")
    compound.Links = all_objects
    
    # Recompute document
    doc.recompute()
    
    # Export STEP file
    step_file = "cad/auxetic_sensor.step"
    Part.export(all_objects, step_file)
    
    print(f"✅ STEP file created: {step_file}")
    
    # Also export individual components
    Part.export([bottom_plate], "cad/bottom_plate.step")
    Part.export([top_plate], "cad/top_plate.step")
    Part.export(auxetic_array, "cad/auxetic_structure.step")
    
    print(f"✅ Individual components exported")
    
    # Close document
    FreeCAD.closeDocument(doc.Name)
    
    return step_file

def create_unit_cell_profile(doc, nodes_2d, edges, height):
    """Create a 3D unit cell from 2D profile."""
    
    # Create points
    points = []
    for x, y in nodes_2d:
        points.append(FreeCAD.Vector(x, y, 0))
    
    # Create wire from edges
    edge_objects = []
    for start_idx, end_idx in edges:
        start_point = points[start_idx]
        end_point = points[end_idx]
        line = Part.makeLine(start_point, end_point)
        edge_objects.append(line)
    
    # Create wire
    wire = Part.Wire(edge_objects)
    
    # Create face
    face = Part.Face(wire)
    
    # Extrude to create solid
    solid = face.extrude(FreeCAD.Vector(0, 0, height))
    
    # Create FreeCAD object
    cell_obj = doc.addObject("Part::Feature", "UnitCell")
    cell_obj.Shape = solid
    
    return cell_obj

def create_auxetic_array(doc, unit_cell, nx, ny, cell_size):
    """Create array of auxetic cells."""
    
    array_objects = []
    
    for i in range(nx):
        for j in range(ny):
            # Calculate position
            x_offset = i * cell_size
            y_offset = j * cell_size
            
            # Create copy of unit cell
            cell_copy = doc.addObject("Part::Feature", f"Cell_{i}_{j}")
            cell_copy.Shape = unit_cell.Shape.copy()
            
            # Move to position
            cell_copy.Placement.Base = FreeCAD.Vector(x_offset, y_offset, 0)
            
            array_objects.append(cell_copy)
    
    return array_objects

def create_capacitor_plates(doc, width, length, height):
    """Create capacitor electrode plates."""
    
    plate_width = width + 6  # mm - extend beyond structure
    plate_length = length + 6
    electrode_thickness = 0.3  # mm
    gap = 1.5  # mm
    
    # Bottom plate
    bottom_box = Part.makeBox(plate_width, plate_length, electrode_thickness)
    bottom_plate = doc.addObject("Part::Feature", "BottomPlate")
    bottom_plate.Shape = bottom_box
    bottom_plate.Placement.Base = FreeCAD.Vector(-3, -3, -electrode_thickness)
    
    # Top plate
    top_box = Part.makeBox(plate_width, plate_length, electrode_thickness)
    top_plate = doc.addObject("Part::Feature", "TopPlate")
    top_plate.Shape = top_box
    top_plate.Placement.Base = FreeCAD.Vector(-3, -3, height + gap)
    
    return bottom_plate, top_plate

def create_support_posts(doc, width, length, height):
    """Create support posts."""
    
    post_diameter = 1.5  # mm
    post_height = height + 1.5  # mm (gap)
    
    # Post positions
    positions = [
        (3, 3),
        (width-3, 3),
        (3, length-3),
        (width-3, length-3),
        (width/2, length/2)
    ]
    
    posts = []
    for i, (x, y) in enumerate(positions):
        # Create cylinder
        cylinder = Part.makeCylinder(post_diameter/2, post_height)
        
        # Create FreeCAD object
        post = doc.addObject("Part::Feature", f"SupportPost_{i+1}")
        post.Shape = cylinder
        post.Placement.Base = FreeCAD.Vector(x, y, 0)
        
        posts.append(post)
    
    return posts

def create_manufacturing_info():
    """Create manufacturing information file."""
    
    info = {
        "sensor_specifications": {
            "total_dimensions_mm": [30, 30, 4],
            "cell_size_mm": 10.0,
            "wall_thickness_mm": 1.2,
            "re_entrance_angle_deg": 45.0,
            "poisson_ratio": -0.414,
            "capacitor_gap_mm": 1.5,
            "electrode_thickness_mm": 0.3
        },
        "3d_printing": {
            "layer_height_mm": 0.2,
            "infill_percent": 100,
            "support_required": True,
            "material": "PLA or PETG",
            "nozzle_diameter_mm": 0.4,
            "print_speed_mm_per_s": 50
        },
        "files_generated": [
            "auxetic_sensor.step - Complete sensor assembly",
            "auxetic_structure.step - Auxetic lattice only",
            "bottom_plate.step - Bottom electrode",
            "top_plate.step - Top electrode"
        ],
        "assembly_notes": [
            "Print as single assembly or separate components",
            "Remove support material carefully from auxetic structure",
            "Test mechanical deformation before electrical connections",
            "Connect wires to electrode plates via edge contacts",
            "Seal electrical connections with flexible adhesive"
        ]
    }
    
    with open("cad/manufacturing_info.json", 'w') as f:
        json.dump(info, f, indent=2)
    
    print("✅ Manufacturing info saved: cad/manufacturing_info.json")

def main():
    """Main function."""
    
    print("🔬 FreeCAD STEP Generator for Auxetic Pressure Sensor")
    print("=" * 60)
    
    try:
        # Create STEP file
        step_file = create_auxetic_sensor_step()
        
        # Create manufacturing info
        create_manufacturing_info()
        
        print(f"\n🎉 Success! Files created:")
        print(f"   • {step_file} - Main STEP file")
        print(f"   • cad/auxetic_structure.step - Auxetic lattice")
        print(f"   • cad/bottom_plate.step - Bottom electrode")
        print(f"   • cad/top_plate.step - Top electrode")
        print(f"   • cad/manufacturing_info.json - Manufacturing data")
        
        print(f"\n📋 Next steps:")
        print(f"   1. Open {step_file} in SolidWorks/Fusion 360/Shapr3D")
        print(f"   2. Verify geometry and dimensions")
        print(f"   3. Export as STL for 3D printing")
        print(f"   4. Follow manufacturing guidelines in JSON file")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 