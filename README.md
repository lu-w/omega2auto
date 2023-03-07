# OMEGA2AUTO

A Python module that converts the [OMEGA format](https://github.com/ika-rwth-aachen/omega_format/) into [A.U.T.O.](https://github.com/lu-w/auto/) ABoxes.

## Getting Started

First, initialize all submodules: `git submodule update --init --recursive`.

### Dependencies

Install the requirements by running `pip install -r requirements.txt`.

### Installation

Install this module by `pip install .`.

## Example Usage

This module provides only a single function to its user: `convert(...)`.
Use it e.g. as follows, assuming you have obtained a file `scenario.hdf5` in the OMEGA format.

```python
import omega2auto
scenarios = omega2auto.convert("scenarios_0_to_100.hdf5")
scenarios[0].save("/tmp/scenario_0.owl")
```

`scenarios` then contains a list of owlready2 worlds, each representing an OMEGA scenario.
You can, for example, save the first scenario as an OWL file and inspect it in some other tool.
