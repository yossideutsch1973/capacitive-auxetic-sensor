# Project Outline

## Phase 1 – Design
- Define target capacitance range and mechanical constraints.
- Parameterize the re-entrant auxetic unit-cell geometry.
- Implement pure-functional generator in `src/design.py`.

## Phase 2 – Simulate
- Export generated geometry to FEA / electromagnetic solvers.
- Validate mechanical and electrical response (capacitance vs strain).
- Iterate on geometric parameters to meet specifications.

## Phase 3 – Test
- Fabricate prototype via additive manufacturing.
- Use PyVISA to log capacitance under controlled loading.
- Compare empirical data with simulation results.

## Phase 4 – Iterate
- Refine design based on discrepancies.
- Optimize for manufacturability and robustness.
- Prepare documentation for publication. 