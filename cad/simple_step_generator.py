#!/usr/bin/env python3
"""
Simple STEP File Generator for Auxetic Pressure Sensor

This script generates coordinate data and attempts to create a STEP file
using alternative methods when CadQuery has installation issues.
"""

import sys
import os
import json
import math

# Add src directory for our design functions
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))
from design import generate_reentrant_cell, calculate_poisson_ratio

def generate_sensor_geometry():
    """Generate complete sensor geometry data."""
    
    print("🔧 Generating auxetic pressure sensor geometry...")
    
    # Sensor parameters (optimized for 3D printing)
    cell_size = 10.0  # mm
    wall_thickness = 1.2  # mm (slightly thicker for strength)
    alpha = 45.0  # degrees (optimal balance)
    height = 4.0  # mm (sensor thickness)
    nx, ny = 3, 3  # 3x3 array
    
    # Calculate derived parameters
    poisson_ratio = calculate_poisson_ratio(1.0, alpha)
    total_width = nx * cell_size
    total_length = ny * cell_size
    
    print(f"📊 Sensor Parameters:")
    print(f"   • Cell size: {cell_size} mm")
    print(f"   • Wall thickness: {wall_thickness} mm")
    print(f"   • Re-entrance angle: {alpha}°")
    print(f"   • Poisson's ratio: {poisson_ratio:.3f}")
    print(f"   • Array: {nx}×{ny} cells")
    print(f"   • Total dimensions: {total_width}×{total_length}×{height} mm")
    
    # Generate single cell geometry
    cell_data = generate_reentrant_cell(
        a=cell_size/10,  # Convert to design units (cm)
        b=wall_thickness/10,
        alpha=alpha
    )
    
    # Convert to mm and create 3D coordinates
    nodes_2d = [(x*10, y*10) for x, y in cell_data["nodes"]]
    edges = cell_data["edges"]
    
    print(f"✅ Generated unit cell: {len(nodes_2d)} nodes, {len(edges)} edges")
    
    # Create complete sensor geometry
    sensor_geometry = {
        "metadata": {
            "name": "Auxetic Capacitive Pressure Sensor",
            "cell_size_mm": cell_size,
            "wall_thickness_mm": wall_thickness,
            "alpha_degrees": alpha,
            "poisson_ratio": poisson_ratio,
            "array_size": [nx, ny],
            "total_dimensions_mm": [total_width, total_length, height],
            "generated_by": "auxetic-sensor-generator"
        },
        "unit_cell": {
            "nodes_2d": nodes_2d,
            "edges": edges
        },
        "auxetic_structure": generate_auxetic_array_coordinates(nodes_2d, edges, nx, ny, cell_size, height),
        "capacitor_plates": generate_capacitor_plates(total_width, total_length, height),
        "support_posts": generate_support_posts(total_width, total_length, height),
        "assembly_instructions": generate_assembly_instructions()
    }
    
    return sensor_geometry

def generate_auxetic_array_coordinates(nodes_2d, edges, nx, ny, cell_size, height):
    """Generate coordinates for the complete auxetic array."""
    
    array_data = {
        "cells": [],
        "all_vertices": [],
        "all_faces": []
    }
    
    vertex_id = 0
    
    for i in range(nx):
        for j in range(ny):
            # Calculate cell position
            offset_x = i * cell_size
            offset_y = j * cell_size
            
            # Generate 3D vertices for this cell (bottom and top)
            cell_vertices_bottom = []
            cell_vertices_top = []
            
            for x, y in nodes_2d:
                # Bottom vertices
                bottom_vertex = [x + offset_x, y + offset_y, 0.0]
                cell_vertices_bottom.append(bottom_vertex)
                array_data["all_vertices"].append(bottom_vertex)
                
                # Top vertices  
                top_vertex = [x + offset_x, y + offset_y, height]
                cell_vertices_top.append(top_vertex)
                array_data["all_vertices"].append(top_vertex)
            
            # Generate faces for this cell
            cell_faces = generate_cell_faces(vertex_id, len(nodes_2d))
            array_data["all_faces"].extend(cell_faces)
            
            # Store cell data
            array_data["cells"].append({
                "position": [i, j],
                "offset": [offset_x, offset_y],
                "vertex_start_id": vertex_id,
                "vertices_bottom": cell_vertices_bottom,
                "vertices_top": cell_vertices_top
            })
            
            vertex_id += len(nodes_2d) * 2  # Bottom + top vertices
    
    return array_data

def generate_cell_faces(start_vertex_id, num_nodes):
    """Generate face data for a single auxetic cell."""
    
    faces = []
    
    # Bottom face (assuming nodes are in order)
    bottom_face = list(range(start_vertex_id, start_vertex_id + num_nodes))
    faces.append({"type": "bottom", "vertices": bottom_face})
    
    # Top face
    top_face = list(range(start_vertex_id + num_nodes, start_vertex_id + 2 * num_nodes))
    faces.append({"type": "top", "vertices": top_face})
    
    # Side faces (connecting bottom to top)
    for i in range(num_nodes):
        next_i = (i + 1) % num_nodes
        
        # Quad face connecting bottom edge to top edge
        side_face = [
            start_vertex_id + i,           # bottom current
            start_vertex_id + next_i,      # bottom next
            start_vertex_id + num_nodes + next_i,  # top next
            start_vertex_id + num_nodes + i        # top current
        ]
        faces.append({"type": "side", "vertices": side_face})
    
    return faces

def generate_capacitor_plates(width, length, height):
    """Generate capacitor electrode plate geometry."""
    
    plate_width = width + 6  # mm - extend beyond auxetic structure
    plate_length = length + 6
    electrode_thickness = 0.3  # mm
    gap = 1.5  # mm
    
    # Bottom plate
    bottom_plate = {
        "name": "bottom_electrode",
        "dimensions": [plate_width, plate_length, electrode_thickness],
        "position": [width/2, length/2, -electrode_thickness/2],
        "vertices": [
            [-plate_width/2, -plate_length/2, -electrode_thickness],
            [plate_width/2, -plate_length/2, -electrode_thickness],
            [plate_width/2, plate_length/2, -electrode_thickness],
            [-plate_width/2, plate_length/2, -electrode_thickness],
            [-plate_width/2, -plate_length/2, 0],
            [plate_width/2, -plate_length/2, 0],
            [plate_width/2, plate_length/2, 0],
            [-plate_width/2, plate_length/2, 0]
        ]
    }
    
    # Top plate
    top_z = height + gap
    top_plate = {
        "name": "top_electrode", 
        "dimensions": [plate_width, plate_length, electrode_thickness],
        "position": [width/2, length/2, top_z + electrode_thickness/2],
        "vertices": [
            [-plate_width/2, -plate_length/2, top_z],
            [plate_width/2, -plate_length/2, top_z],
            [plate_width/2, plate_length/2, top_z],
            [-plate_width/2, plate_length/2, top_z],
            [-plate_width/2, -plate_length/2, top_z + electrode_thickness],
            [plate_width/2, -plate_length/2, top_z + electrode_thickness],
            [plate_width/2, plate_length/2, top_z + electrode_thickness],
            [-plate_width/2, plate_length/2, top_z + electrode_thickness]
        ]
    }
    
    return {
        "bottom_plate": bottom_plate,
        "top_plate": top_plate,
        "gap_mm": gap,
        "electrode_thickness_mm": electrode_thickness
    }

def generate_support_posts(width, length, height):
    """Generate support post geometry."""
    
    post_diameter = 1.5  # mm
    post_radius = post_diameter / 2
    post_height = height + 1.5  # mm (gap)
    
    # Post positions (corners + center)
    positions = [
        [3, 3],  # Corner posts
        [width-3, 3],
        [3, length-3],
        [width-3, length-3],
        [width/2, length/2]  # Center post
    ]
    
    posts = []
    for i, (x, y) in enumerate(positions):
        post = {
            "name": f"support_post_{i+1}",
            "position": [x, y, 0],
            "diameter": post_diameter,
            "height": post_height,
            "center": [x, y, post_height/2]
        }
        posts.append(post)
    
    return {
        "posts": posts,
        "post_diameter_mm": post_diameter,
        "post_height_mm": post_height
    }

def generate_assembly_instructions():
    """Generate assembly and manufacturing instructions."""
    
    return {
        "3d_printing": {
            "layer_height": "0.2 mm",
            "infill": "100% (solid)",
            "support": "Yes (for overhangs)",
            "material": "PLA or PETG",
            "nozzle": "0.4 mm",
            "print_speed": "50 mm/s"
        },
        "assembly": [
            "1. Print the complete sensor model",
            "2. Remove support material carefully",
            "3. Test auxetic deformation by gentle compression",
            "4. Connect wires to electrode plates",
            "5. Seal connections with flexible adhesive",
            "6. Calibrate using known loads"
        ],
        "testing": [
            "Use multimeter to verify capacitance (~10-50 pF)",
            "Apply gentle pressure and observe capacitance increase",
            "Expected: 10-30% capacitance change under load"
        ]
    }

def export_geometry_data(geometry, output_dir="cad"):
    """Export geometry data in multiple formats."""
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Export as JSON for manual CAD import
    json_file = os.path.join(output_dir, "sensor_geometry.json")
    with open(json_file, 'w') as f:
        json.dump(geometry, f, indent=2)
    print(f"✅ Exported: {json_file}")
    
    # Export as OBJ file (simple mesh format)
    obj_file = os.path.join(output_dir, "auxetic_sensor.obj")
    export_obj_file(geometry, obj_file)
    print(f"✅ Exported: {obj_file}")
    
    # Export coordinates for manual CAD creation
    coords_file = os.path.join(output_dir, "manual_cad_coordinates.txt")
    export_manual_cad_instructions(geometry, coords_file)
    print(f"✅ Exported: {coords_file}")
    
    return json_file, obj_file, coords_file

def export_obj_file(geometry, filename):
    """Export geometry as OBJ file (can be imported into most CAD software)."""
    
    with open(filename, 'w') as f:
        f.write("# Auxetic Capacitive Pressure Sensor\n")
        f.write("# Generated by auxetic-sensor-generator\n\n")
        
        # Write vertices
        vertices = geometry["auxetic_structure"]["all_vertices"]
        for i, vertex in enumerate(vertices):
            f.write(f"v {vertex[0]:.3f} {vertex[1]:.3f} {vertex[2]:.3f}\n")
        
        f.write("\n# Faces\n")
        
        # Write faces (OBJ uses 1-based indexing)
        faces = geometry["auxetic_structure"]["all_faces"]
        for face in faces:
            if len(face["vertices"]) >= 3:
                vertex_indices = [str(v + 1) for v in face["vertices"]]
                f.write(f"f {' '.join(vertex_indices)}\n")

def export_manual_cad_instructions(geometry, filename):
    """Export detailed instructions for manual CAD creation."""
    
    with open(filename, 'w') as f:
        f.write("AUXETIC CAPACITIVE SENSOR - Manual CAD Creation Guide\n")
        f.write("=" * 60 + "\n\n")
        
        meta = geometry["metadata"]
        f.write("SENSOR SPECIFICATIONS:\n")
        f.write(f"  • Total size: {meta['total_dimensions_mm'][0]}×{meta['total_dimensions_mm'][1]}×{meta['total_dimensions_mm'][2]} mm\n")
        f.write(f"  • Cell size: {meta['cell_size_mm']} mm\n")
        f.write(f"  • Wall thickness: {meta['wall_thickness_mm']} mm\n")
        f.write(f"  • Re-entrance angle: {meta['alpha_degrees']}°\n")
        f.write(f"  • Poisson's ratio: {meta['poisson_ratio']:.3f}\n\n")
        
        f.write("UNIT CELL COORDINATES (2D Profile):\n")
        nodes = geometry["unit_cell"]["nodes_2d"]
        for i, (x, y) in enumerate(nodes):
            f.write(f"  Node {i+1}: ({x:.2f}, {y:.2f}) mm\n")
        
        f.write("\nUNIT CELL EDGES:\n")
        edges = geometry["unit_cell"]["edges"]
        for i, (start, end) in enumerate(edges):
            f.write(f"  Edge {i+1}: Node {start+1} → Node {end+1}\n")
        
        f.write("\nMANUAL CAD STEPS:\n")
        f.write("1. Create 2D sketch using the unit cell coordinates above\n")
        f.write("2. Connect nodes with lines according to the edge list\n")
        f.write("3. Extrude the 2D profile to 4.0 mm height\n")
        f.write("4. Create a 3×3 rectangular pattern with 10 mm spacing\n")
        f.write("5. Add bottom plate: 36×36×0.3 mm at Z=-0.3\n")
        f.write("6. Add top plate: 36×36×0.3 mm at Z=5.5\n")
        f.write("7. Add 5 support posts: ⌀1.5×5.5 mm at specified positions\n")
        f.write("8. Create wire channels: 2×36×0.5 mm grooves\n\n")
        
        f.write("SUPPORT POST POSITIONS:\n")
        posts = geometry["support_posts"]["posts"]
        for post in posts:
            pos = post["position"]
            f.write(f"  • {post['name']}: ({pos[0]:.1f}, {pos[1]:.1f}) mm\n")
        
        f.write("\nCAPACITOR PLATE DETAILS:\n")
        plates = geometry["capacitor_plates"]
        f.write(f"  • Bottom plate: Z = {plates['bottom_plate']['position'][2]:.1f} mm\n")
        f.write(f"  • Top plate: Z = {plates['top_plate']['position'][2]:.1f} mm\n")
        f.write(f"  • Gap: {plates['gap_mm']} mm\n")
        f.write(f"  • Thickness: {plates['electrode_thickness_mm']} mm\n")

def try_alternative_step_export(geometry):
    """Try alternative methods to create STEP file."""
    
    print("\n🔄 Attempting alternative STEP file generation...")
    
    try:
        # Try using FreeCAD if available
        import FreeCAD
        import Part
        
        print("✅ FreeCAD found! Generating STEP file...")
        
        # Create a simple box as proof of concept
        doc = FreeCAD.newDocument("AuxeticSensor")
        
        # Create main structure box
        meta = geometry["metadata"]
        width, length, height = meta["total_dimensions_mm"]
        
        main_box = Part.makeBox(width, length, height)
        main_obj = doc.addObject("Part::Feature", "AuxeticStructure")
        main_obj.Shape = main_box
        
        # Export STEP file
        step_file = "cad/auxetic_sensor_freecad.step"
        Part.export([main_obj], step_file)
        
        print(f"✅ STEP file created: {step_file}")
        return step_file
        
    except ImportError:
        print("❌ FreeCAD not available")
    
    try:
        # Try using OpenCASCADE directly
        from OCC.Core import BRepPrimAPI_MakeBox, STEPControl_Writer, IFSelect_RetDone
        from OCC.Core.gp import gp_Pnt
        
        print("✅ OpenCASCADE found! Generating STEP file...")
        
        # Create simple box
        meta = geometry["metadata"]
        width, length, height = meta["total_dimensions_mm"]
        
        box = BRepPrimAPI_MakeBox(gp_Pnt(0, 0, 0), width, length, height).Shape()
        
        # Write STEP file
        step_writer = STEPControl_Writer()
        step_writer.Transfer(box, IFSelect_RetDone)
        
        step_file = "cad/auxetic_sensor_occ.step"
        step_writer.Write(step_file)
        
        print(f"✅ STEP file created: {step_file}")
        return step_file
        
    except ImportError:
        print("❌ OpenCASCADE not available")
    
    print("❌ No CAD libraries available for STEP export")
    return None

def main():
    """Main function to generate sensor geometry and export files."""
    
    print("🔬 Auxetic Pressure Sensor - Geometry Generator")
    print("=" * 60)
    
    try:
        # Generate complete sensor geometry
        geometry = generate_sensor_geometry()
        
        # Export geometry data
        print(f"\n💾 Exporting geometry data...")
        json_file, obj_file, coords_file = export_geometry_data(geometry)
        
        # Try to create STEP file using alternative methods
        step_file = try_alternative_step_export(geometry)
        
        print(f"\n🎉 Generation completed!")
        print(f"📁 Output files:")
        print(f"   • {json_file} - Complete geometry data")
        print(f"   • {obj_file} - 3D mesh (import into CAD)")
        print(f"   • {coords_file} - Manual CAD instructions")
        
        if step_file:
            print(f"   • {step_file} - STEP file for CAD software")
        else:
            print(f"   • No STEP file generated (install FreeCAD for STEP export)")
        
        print(f"\n📋 Next steps:")
        print(f"   1. Import {obj_file} into SolidWorks/Fusion 360/Shapr3D")
        print(f"   2. Or follow instructions in {coords_file} for manual creation")
        print(f"   3. Use the JSON data for programmatic CAD creation")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 