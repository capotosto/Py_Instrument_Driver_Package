"""
The instrument_module package provides a collection of Python classes
for controlling various lab instruments via PyVISA.

All core instrument drivers (e.g., DMMs, Function Generators, Oscilloscopes)
and common utility functions are exposed directly at the package root
for simplified imports.

Usage Example:
--------------
To import a specific instrument class:
    from instrument_suite import DP800, Keithley2100

To import utility functions (like listing resources):
    from instrument_suite import visa_utils

Package Contents:
-----------------
- Keithley2100: Driver for Keithley 2100 Series DMM.
- Keithley6221: Driver for Keithley 622x Series Current/Voltage Source.
- DG4000: Driver for Rigol DG4000 Series Function Generators.
- DP800: Driver for Rigol DP800 Series Power Supplies.
- DPO4000: Driver for Tektronix DPO4000/MSO4000 Series Oscilloscopes.
- visa_utils: Helper functions for VISA connection and resource listing.
"""

# instrument_module/__init__.py
# This file defines the instrument_suite directory as a Python package.

# Expose main classes directly for cleaner imports
# (e.g., from instrument_suite import DP800)

from .keithley_2100 import Keithley2100
from .keithley_6221 import Keithley6221
from .keysight_34461a import Keysight34461A
from .keysight_E4980A import KeysightE4980A
from .rigol_dg4000 import DG4000
from .rigol_dp800 import DP800
from .rigol_dl3000 import DL3000
from .Tek_DPO4000 import DPO4000

# Also expose the utility functions/module
from . import visa_utils


__version__ = "1.0.0"

__all__ = [
    "Keithley2100",
    "Keithley6221",
    "Keysight34461A",
    "KeysightE4980A",
    "DG4000",
    "DP800",
    "DL3000",
    "DPO4000",
    "visa_utils",
    "__version__"
]
