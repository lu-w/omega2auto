# OMEGA2AUTO

A Python module that converts the [OMEGA format](https://github.com/ika-rwth-aachen/omega_format/) into [A.U.T.O.](https://github.com/lu-w/auto/) ABoxes.

## Getting Started

First, initialize all submodules: `git submodule update --init --recursive`.

### Dependencies

This module requires the `omega_format` module, for which you can find installation instructions in `omega_format/README.md`.
We moreover require the `pyauto` module, which can be simply installed by `pip install -e pyauto`.
All requirements are also given in `requirements.txt`.

### Installation

Install this module by `pip install -e .`.

## Example Usage

This module provides only a single function to its user: `convert()`.
Use it e.g. as follows, assuming you have obtained a file `scenario.hdf5` in the OMEGA format.

```python
from omega2auto import omega_to_auto
scenarios = omega_to_auto.convert("scenario.hdf5")
```

`scenarios` then contains a list of owlready2 worlds, each representing an OMEGA scenario.
You can, for example, save the first scenario as an OWL file and inspect it in some other tool by

```python
scenarios[0].save("/tmp/scenario0.owl")
```