"""Testbench setup helpers for capacitance measurement.

This module provides both mock and real instrument interfaces for capacitance
measurement using PyVISA. Mock instruments allow testing without hardware.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional, Tuple
import math
import random

try:
    import pyvisa as visa  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    visa = None  # type: ignore

__all__ = [
    "MockLCRMeter",
    "read_capacitance",
    "calibrate_sensor",
    "log_measurement_series",
]


class MockLCRMeter:
    """Mock LCR meter for testing without hardware."""
    
    def __init__(self, base_capacitance: float = 1e-12):
        """Initialize mock instrument.
        
        Parameters
        ----------
        base_capacitance : float, default=1e-12
            Baseline capacitance value in farads.
        """
        self.base_capacitance = base_capacitance
        self.noise_level = 0.01  # 1% noise
        self.connected = True
        
    def query(self, command: str) -> str:
        """Mock SCPI command response."""
        if "MEAS:C?" in command:
            # Simulate capacitance with small random variation
            noise = random.gauss(0, self.noise_level)
            value = self.base_capacitance * (1 + noise)
            return f"{value:.12e}"
        elif "*IDN?" in command:
            return "Mock,LCR-Meter,12345,1.0"
        else:
            return "OK"
            
    def write(self, command: str) -> None:
        """Mock write command."""
        pass
        
    def close(self) -> None:
        """Mock close connection."""
        self.connected = False


def read_capacitance(inst: Any, channel: int = 1, frequency: float = 1000.0) -> float:
    """Read capacitance value from an LCR-meter via PyVISA.

    Parameters
    ----------
    inst : visa.resources.MessageBasedResource or MockLCRMeter
        Instrument session object (mock or real).
    channel : int, default=1
        Measurement channel.
    frequency : float, default=1000.0
        Test frequency in Hz.

    Returns
    -------
    float
        Measured capacitance in farads.
        
    Notes
    -----
    ASCII symbolic form::
    
        C = Q/V = ε₀ * ε_r * A / d
        
    Where ε₀ = 8.854e-12 F/m (vacuum permittivity)
    """
    try:
        # Set measurement frequency if supported
        if hasattr(inst, 'write'):
            inst.write(f"FREQ {frequency}")
            
        # Query capacitance measurement
        if hasattr(inst, 'query'):
            response = inst.query(f"MEAS:C? (@{channel})")
            return float(response.strip())
        else:
            # Fallback for basic instruments
            return float("nan")
            
    except Exception:
        return float("nan")


def calibrate_sensor(
    inst: Any, 
    reference_loads: List[float],
    num_samples: int = 10
) -> Dict[str, List[float]]:
    """Calibrate sensor by measuring known reference loads.
    
    Parameters
    ----------
    inst : instrument object
        Connected LCR meter.
    reference_loads : List[float]
        Known applied loads/strains for calibration.
    num_samples : int, default=10
        Number of samples per calibration point.
        
    Returns
    -------
    Dict[str, List[float]]
        Calibration data with 'loads' and 'capacitances' keys.
        
    Notes
    -----
    ASCII symbolic form::
    
        C(ε) = C₀ * (1 + k*ε)  (linear approximation)
        
    Where k is the sensitivity coefficient.
    """
    loads = []
    capacitances = []
    
    for load in reference_loads:
        # Simulate applying load (in real setup, this would be manual)
        print(f"Apply load: {load:.3f} N (press Enter when ready)")
        # input()  # Uncomment for interactive calibration
        
        # Take multiple samples and average
        samples = []
        for _ in range(num_samples):
            cap = read_capacitance(inst)
            if not math.isnan(cap):
                samples.append(cap)
            time.sleep(0.1)  # Brief delay between samples
            
        if samples:
            avg_capacitance = sum(samples) / len(samples)
            loads.append(load)
            capacitances.append(avg_capacitance)
            print(f"Load: {load:.3f} N -> Capacitance: {avg_capacitance:.3e} F")
        else:
            print(f"Warning: No valid readings for load {load:.3f} N")
    
    return {"loads": loads, "capacitances": capacitances}


def log_measurement_series(
    inst: Any,
    duration: float,
    sample_rate: float = 10.0,
    filename: Optional[str] = None
) -> List[Tuple[float, float]]:
    """Log a time series of capacitance measurements.
    
    Parameters
    ----------
    inst : instrument object
        Connected LCR meter.
    duration : float
        Total measurement duration in seconds.
    sample_rate : float, default=10.0
        Sampling rate in Hz.
    filename : str, optional
        If provided, save data to CSV file.
        
    Returns
    -------
    List[Tuple[float, float]]
        Time series data as (timestamp, capacitance) pairs.
        
    Notes
    -----
    ASCII symbolic form::
    
        Δt = 1/f_sample
        t_i = i * Δt  for i = 0, 1, 2, ...
    """
    data = []
    sample_interval = 1.0 / sample_rate
    num_samples = int(duration * sample_rate)
    
    start_time = time.time()
    
    for i in range(num_samples):
        target_time = start_time + i * sample_interval
        
        # Wait until target time
        current_time = time.time()
        if current_time < target_time:
            time.sleep(target_time - current_time)
            
        # Take measurement
        capacitance = read_capacitance(inst)
        timestamp = time.time() - start_time
        
        if not math.isnan(capacitance):
            data.append((timestamp, capacitance))
            
        # Progress indicator
        if i % int(sample_rate) == 0:  # Every second
            print(f"Progress: {i/num_samples*100:.1f}% ({len(data)} valid samples)")
    
    # Save to file if requested
    if filename and data:
        with open(filename, 'w') as f:
            f.write("timestamp,capacitance\n")
            for timestamp, capacitance in data:
                f.write(f"{timestamp:.6f},{capacitance:.12e}\n")
        print(f"Data saved to {filename}")
    
    return data 