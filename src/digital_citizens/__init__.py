"""digital_citizens: build and validate LLM-simulated populations ("digital citizens").

The package is organised around one loop:

    real population data  ->  persona bank  ->  simulated answers  ->  compare with real answers

- ``data``       loaders for real human ground truth (surveys, panels) and persona skeletons
- ``population`` tools to make a persona bank match a population's census margins (raking / IPF)
- ``simulate``   the LLM response engine (role-play sampling and direct distribution prediction)
- ``evaluate``   fidelity metrics, baselines the LLM must beat, and ceilings it cannot exceed
"""

__version__ = "0.0.1"
