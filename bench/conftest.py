import pytest
# Force pytest benchmark to use seconds
def pytest_benchmark_scale_unit(config, unit, benchmarks, best, worst, sort):
    if unit == "seconds":
        return "m", 1000
