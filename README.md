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
│   └── auxetic_cell.f3d
├── docs/
│   └── project_outline.md
├── simulations/
│   └── simulation.ipynb
├── src/
│   ├── design.py
│   ├── utils.py
│   └── test_setup.py
├── tests/
│   └── test_design.py
└── .gitignore
```

Quickstart
----------
1. Create an isolated environment:
   ```bash
   python -m venv env
   source env/bin/activate
   pip install -r requirements.txt  # coming soon
   ```
2. Run the test suite:
   ```bash
   pytest
   ```
3. Open the simulation notebook:
   ```bash
   jupyter lab simulations/simulation.ipynb
   ``` 