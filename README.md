# OMEGA2AUTO

A Python module that converts the [OMEGA format](https://github.com/ika-rwth-aachen/omega_format/) into [A.U.T.O.](https://github.com/lu-w/auto/) ABoxes based on the [`pyauto` library](https://github.com/lu-w/pyauto/).

![OMEGA2AUTO](./images/omega2auto.svg)

## Getting Started

OMEGA2AUTO has been tested with Python v3.12. 
It is recommended to set up a virtual environment.  
First, initialize all submodules: `git submodule update --init --recursive`.

### Dependencies

Install the dependencies of pyauto by `cd pyauto; pip install -r requirements.txt`
Change back into this directory and install the requirements of this module by running `pip install -r requirements.txt`.

### Installation

Install this module by `pip install .`.

## Example Usage

This module provides only a single function to its user: `convert(...)`.
Use it e.g. as follows, assuming you have obtained a file `scenarios_0_to_100.hdf5` in the OMEGA format.

```python
from omega2auto import omega2auto
scenarios = omega2auto.convert("scenarios_0_to_100.hdf5")
```

`scenarios` then contains a list of `pyauto` `Scenario` objects, each representing an OMEGA scenario.
You can, for example, save the first scenario as an OWL file and inspect it in some other tool:

```python
scenarios[0].save_abox("scenario_0.owl")
```

The output will be stored in a temporal knowledge base file (containing a list of OWL file paths) in `scenario_0.kbs`.
