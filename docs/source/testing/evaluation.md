# RAG Evaluation Benchmark

The evaluation module (`src/ai/evaluation.py`) provides an automated benchmark evaluating retrieval accuracy, source correctness, and anti-hallucination fallback.

## Benchmark Dataset (`BENCHMARK_DATASET`)

| Test ID | Question | Expected Source Document | Expect Fallback |
| :--- | :--- | :--- | :--- |
| `TC-001` | What should be checked when an EV reports repeated battery overheating? | `sample_ev_battery_service.txt` | `False` |
| `TC-002` | What are the recommended checks for a charging system fault? | `sample_charging_system.txt` | `False` |
| `TC-003` | What checks should be performed on the battery cooling circuit? | `sample_thermal_management.txt` | `False` |
| `TC-004` | How do I reset the oil change service light on a 1995 E36 3-Series? | `None` | `True` |
| `TC-005` | What is the recommended brake fluid change interval for a bicycle? | `None` | `True` |

## Evaluation Metrics
- **Retrieval Success Rate**: Percentage of test cases where expected document was retrieved.
- **Fallback Verification Rate**: Percentage of out-of-domain test cases where fallback was correctly triggered.
- **Accuracy Percentage**: Overall percentage of test cases passing criteria ($\ge 80\%$ required for `PASSED` status).
