# Capacitive Auxetic Sensor

Overview
--------
A capacitive pressure/strain sensor leveraging a re-entrant auxetic lattice to achieve large, nearly linear capacitance changes under load.

Repository Layout
-----------------
```
.
├── README.md
├── cad/
│   ├── auxetic_cell_3d.py      # 3D CAD model generator (CadQuery)
│   └── test_3d_model.py        # Test 3D model generation
├── docs/
│   └── project_outline.md
├── simulations/
│   └── simulation.ipynb
├── src/
│   ├── design.py               # Auxetic cell design functions
│   ├── utils.py                # Mathematical utilities
│   └── test_setup.py           # Measurement system setup
├── tests/
│   ├── test_design.py          # Design function tests
│   ├── test_utils.py           # Utility function tests
│   └── test_test_setup.py      # Measurement system tests
├── requirements.txt            # Python dependencies
├── demo.py                     # Complete demonstration
└── .gitignore
```

Quickstart
----------
1. Create an isolated environment:
   ```bash
   python -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```
2. Run the complete demo:
   ```bash
   python demo.py
   ```
3. Run the test suite:
   ```bash
   pytest
   ```
4. Generate 3D models for printing:
   ```bash
   pip install cadquery-ocp  # Install 3D CAD library
   python cad/auxetic_cell_3d.py  # Generate STL files
   ```
5. Open the simulation notebook:
   ```bash
   jupyter lab simulations/simulation.ipynb
   ```

## 🖨️ 3D Printing

The project includes a complete **CadQuery-based 3D model generator** that creates STL files ready for 3D printing:

- **`cad/auxetic_cell_3d.py`**: Parametric 3D model generator
- **Output files**: `.stl` (3D printing), `.step` (CAD editing)
- **Three configurations**: Standard, High Sensitivity, Robust
- **Complete sensor**: Auxetic structure + capacitor plates + support posts + wire channels

**Key Features:**
- Parametric design (easily modify cell size, wall thickness, re-entrance angle)
- Multiple sensor configurations optimized for different applications
- Manufacturing instructions and 3D printing settings included
- Integration with existing design functions for mathematical accuracy 