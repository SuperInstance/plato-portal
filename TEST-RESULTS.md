# Test Results — Full Sweep

Generated: 2026-05-23

| Package | Tests | Pass | Fail | Notes |
|---------|-------|------|------|-------|
| constraint-theory-core | 83 | 83 | 0 | |
| counterpoint-engine | 109 | 109 | 0 | |
| groove-analyzer | 11 | 11 | 0 | |
| holonomy-harmony | 94 | 94 | 0 | |
| spline-midi-smooth | 55 | 55 | 0 | |
| plato-room-musician | 42 | 42 | 0 | |
| jazz-voicing-engine | 26 | 26 | 0 | |
| style-dna | 29 | 29 | 0 | |
| constraint-synth | 20 | 20 | 0 | |
| constraint-viz | 8 | 8 | 0 | |
| constraint-substrate/python | 34 | 34 | 0 | |
| constraint-substrate/rust | 30 | 30 | 0 | Cargo tests |
| constraint_instrument | 126 | 126 | 0 | Fixed 2 bugs (GoodmanEngine) |
| **Integration test** | **15** | **15** | **0** | test_integration.py |

## Totals

- **Unit tests: 673 passed, 0 failed**
- **Integration: 15 passed, 0 failed**
- **Grand total: 688 tests, all passing ✅**

## Fixes Applied

1. **constraint_instrument/goodman.py**: Added `prescribe()` public method to `GoodmanEngine`
2. **constraint_instrument/goodman.py**: Fixed `_prescribe()` crash on empty `order.components` (added fallback)
3. **constraint_instrument/goodman.py**: Fixed `DiagnosticReport` missing `stars` property (test accessed `report.stars`)
4. **constraint_instrument/goodman.py**: Fixed `KeyError` when accessing `order.components[weakest_component]` with `.get()` fallback
