
import pytest
import json
import time
from datetime import datetime
import io
from contextlib import redirect_stdout
from statistics import mean, quantiles

class TestRunner:
    def __init__(self, api_name="Agify"):
        self.api_name = api_name
        self.test_results = []

    def run_all_tests(self):
        print(f"\nRunning tests for {self.api_name}...")
        f = io.StringIO()
        with redirect_stdout(f):
            from . import tests as api_tests

            test_functions = [
                api_tests.test_agify_status_code_success,
                api_tests.test_agify_response_content_michael,
                api_tests.test_agify_response_content_invalid_name,
                api_tests.test_agify_no_name_parameter,
                api_tests.test_agify_multiple_names_status_code,
                api_tests.test_agify_multiple_names_content,
            ]

            latencies = []
            passed_count = 0
            failed_count = 0

            for test_func in test_functions:
                test_name = test_func.__name__
                status = "FAIL"
                latency = 0
                details = ""
                start_time_overall = time.time() # For total function execution time if test fails before returning latency

                try:
                    latency = test_func() # Test function now returns latency
                    status = "PASS"
                    passed_count += 1
                except Exception as e:
                    details = str(e)
                    failed_count += 1
                    # If an exception occurs, approximate latency with the total time taken for the function to run.
                    latency = (time.time() - start_time_overall) * 1000
                finally:
                    self.test_results.append({
                        "name": test_name,
                        "status": status,
                        "latency_ms": round(latency, 2),
                        "details": details
                    })
                    if status == "PASS":
                        latencies.append(latency)

        total_tests = passed_count + failed_count
        error_rate = failed_count / total_tests if total_tests > 0 else 0

        avg_latency = round(mean(latencies), 2) if latencies else 0
        p95_latency = round(quantiles(latencies, n=100)[94], 2) if latencies else 0 # 95th percentile

        summary = {
            "passed": passed_count,
            "failed": failed_count,
            "error_rate": round(error_rate, 3),
            "latency_ms_avg": avg_latency,
            "latency_ms_p95": p95_latency
        }

        run_data = {
            "api": self.api_name,
            "timestamp": datetime.now().isoformat(),
            "summary": summary,
            "tests": self.test_results
        }

        return run_data

if __name__ == '__main__':
    runner = TestRunner()
    run_results = runner.run_all_tests()
    print(json.dumps(run_results, indent=2))
