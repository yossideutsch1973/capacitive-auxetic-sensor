import pytest
import math
import time

from src.test_setup import (
    MockLCRMeter, read_capacitance, calibrate_sensor, log_measurement_series
)


def test_mock_lcr_meter():
    """Test MockLCRMeter functionality."""
    # Basic initialization
    mock = MockLCRMeter()
    assert mock.connected is True
    assert mock.base_capacitance == 1e-12
    assert mock.noise_level == 0.01
    
    # Custom initialization
    mock_custom = MockLCRMeter(base_capacitance=5e-12)
    assert mock_custom.base_capacitance == 5e-12
    
    # Test query responses
    response = mock.query("MEAS:C? (@1)")
    capacitance = float(response)
    assert capacitance > 0  # Should be positive
    assert abs(capacitance - mock.base_capacitance) / mock.base_capacitance < 0.1  # Within noise range
    
    # Test identification query
    idn = mock.query("*IDN?")
    assert "Mock" in idn
    assert "LCR-Meter" in idn
    
    # Test write command (should not raise error)
    mock.write("FREQ 1000")
    
    # Test close
    mock.close()
    assert mock.connected is False


def test_read_capacitance():
    """Test capacitance reading function."""
    mock = MockLCRMeter(base_capacitance=10e-12)
    
    # Basic reading
    cap = read_capacitance(mock)
    assert not math.isnan(cap)
    assert cap > 0
    assert abs(cap - 10e-12) / 10e-12 < 0.1  # Within expected noise range
    
    # Test with different parameters
    cap_freq = read_capacitance(mock, channel=2, frequency=5000.0)
    assert not math.isnan(cap_freq)
    
    # Test with object that doesn't support query (should return NaN)
    class DummyInstrument:
        pass
    
    dummy = DummyInstrument()
    cap_dummy = read_capacitance(dummy)
    assert math.isnan(cap_dummy)


def test_calibrate_sensor():
    """Test sensor calibration function."""
    mock = MockLCRMeter(base_capacitance=10e-12)
    
    # Test calibration with known loads
    reference_loads = [0.0, 1.0, 2.0, 3.0]  # N
    cal_data = calibrate_sensor(mock, reference_loads, num_samples=3)
    
    # Check structure
    assert "loads" in cal_data
    assert "capacitances" in cal_data
    assert len(cal_data["loads"]) == len(reference_loads)
    assert len(cal_data["capacitances"]) == len(reference_loads)
    
    # Check that all capacitances are valid
    for cap in cal_data["capacitances"]:
        assert not math.isnan(cap)
        assert cap > 0
    
    # Test with empty reference loads
    cal_empty = calibrate_sensor(mock, [], num_samples=1)
    assert len(cal_empty["loads"]) == 0
    assert len(cal_empty["capacitances"]) == 0


def test_log_measurement_series():
    """Test time series measurement logging."""
    mock = MockLCRMeter(base_capacitance=5e-12)
    
    # Short measurement series
    duration = 0.5  # seconds
    sample_rate = 10.0  # Hz
    
    start_time = time.time()
    data = log_measurement_series(mock, duration, sample_rate)
    end_time = time.time()
    
    # Check timing (allow some tolerance for system timing variations)
    actual_duration = end_time - start_time
    assert actual_duration >= duration * 0.8  # Should take at least 80% of requested duration
    assert actual_duration < duration + 1.0  # But not too much longer
    
    # Check data structure
    assert isinstance(data, list)
    expected_samples = int(duration * sample_rate)
    assert len(data) <= expected_samples + 2  # Allow some tolerance
    
    # Check data format
    for timestamp, capacitance in data:
        assert isinstance(timestamp, float)
        assert isinstance(capacitance, float)
        assert timestamp >= 0
        assert timestamp <= duration + 0.1  # Small tolerance
        assert not math.isnan(capacitance)
        assert capacitance > 0
    
    # Check timestamps are roughly evenly spaced
    if len(data) > 1:
        time_diffs = [data[i+1][0] - data[i][0] for i in range(len(data)-1)]
        expected_interval = 1.0 / sample_rate
        for diff in time_diffs:
            assert abs(diff - expected_interval) < 0.1  # Allow timing tolerance


def test_log_measurement_series_with_file(tmp_path):
    """Test measurement logging with file output."""
    mock = MockLCRMeter(base_capacitance=1e-12)
    
    # Create temporary file path
    filename = tmp_path / "test_measurements.csv"
    
    # Log measurements
    data = log_measurement_series(mock, duration=0.2, sample_rate=5.0, filename=str(filename))
    
    # Check file was created
    assert filename.exists()
    
    # Check file content
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Should have header + data lines
    assert len(lines) >= 2
    assert lines[0].strip() == "timestamp,capacitance"
    
    # Check data lines format
    for line in lines[1:]:
        parts = line.strip().split(',')
        assert len(parts) == 2
        timestamp = float(parts[0])
        capacitance = float(parts[1])
        assert timestamp >= 0
        assert capacitance > 0


def test_measurement_consistency():
    """Test consistency between different measurement functions."""
    mock = MockLCRMeter(base_capacitance=20e-12)
    
    # Single reading
    single_reading = read_capacitance(mock)
    
    # Calibration reading (should be similar)
    cal_data = calibrate_sensor(mock, [0.0], num_samples=1)
    cal_reading = cal_data["capacitances"][0]
    
    # Time series reading
    series_data = log_measurement_series(mock, duration=0.1, sample_rate=1.0)
    series_reading = series_data[0][1] if series_data else float('nan')
    
    # All readings should be in similar range (allowing for noise)
    readings = [single_reading, cal_reading, series_reading]
    readings = [r for r in readings if not math.isnan(r)]
    
    if len(readings) >= 2:
        max_reading = max(readings)
        min_reading = min(readings)
        relative_spread = (max_reading - min_reading) / min_reading
        assert relative_spread < 0.2  # Should be within 20% due to noise


if __name__ == "__main__":
    pytest.main([__file__]) 