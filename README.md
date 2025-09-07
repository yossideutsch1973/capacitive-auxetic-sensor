# Capacitive Auxetic Sensor

Overview
--------
A capacitive pressure/strain sensor leveraging a re-entrant auxetic lattice to achieve large, nearly linear capacitance changes under load.

Repository Layout
-----------------
```
.
├── README.md
├── .github/
│   └── workflows/
│       └── pages.yml             # GitHub Pages deployment
├── cad/
│   ├── auxetic_cell_3d.py        # 3D CAD model generator (CadQuery)
│   └── test_3d_model.py          # Test 3D model generation
├── docs/
│   ├── index.html                # Web frontend landing page
│   ├── auxetic_simulator.html    # Interactive pattern simulator
│   ├── review_landing.html       # User reviews page
│   └── project_outline.md
├── scripts/
│   └── serve_docs.py             # Local development server
├── simulations/
│   └── simulation.ipynb
├── src/
│   ├── design.py                 # Auxetic cell design functions
│   ├── utils.py                  # Mathematical utilities
│   └── test_setup.py             # Measurement system setup
├── tests/
│   ├── test_design.py            # Design function tests
│   ├── test_utils.py             # Utility function tests
│   └── test_test_setup.py        # Measurement system tests
├── requirements.txt              # Python dependencies
├── demo.py                       # Complete demonstration
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
6. Launch the interactive auxetic pattern simulator:
   
   **Online Version (GitHub Pages):**
   Visit `https://yossideutsch1973.github.io/capacitive-auxetic-sensor/` for the online demo (requires GitHub Pages to be enabled).
   
   **Local Version:**
   Simply open [`docs/auxetic_simulator.html`](docs/auxetic_simulator.html) in your web browser.

   To access it from another device (e.g. your phone) on the same network, run:
   ```bash
   python scripts/serve_docs.py --host 0.0.0.0 --port 8000
   ```
   Then browse to `http://<your-ip>:8000/` on your phone.

## 🌐 Web Frontend

The project includes a complete web-based frontend deployed via GitHub Pages:

- **Interactive Pattern Simulator**: Real-time visualization of auxetic cell patterns
- **User Reviews & Feedback**: Community reviews and direct GitHub integration  
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **No Installation Required**: Browser-based tools accessible to anyone

### Enabling GitHub Pages
To enable the web frontend:
1. Go to repository Settings → Pages
2. Set Source to "GitHub Actions"
3. The site will be available at `https://yossideutsch1973.github.io/capacitive-auxetic-sensor/`

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