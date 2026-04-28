
from tester.tests import AgifyAPITests
from datetime import datetime
import numpy as np

def run_tests():
    test_suite = AgifyAPITests()
    results = []
    latencies = []
    success_count = 0
    error_count = 0
    
    # Dynamically find and run all methods starting with 'test_'
    for method_name in dir(test_suite):
        if method_name.startswith('test_') and callable(getattr(test_suite, method_name)):
            test_method = getattr(test_suite, method_name)
            status, latency, message = test_method()
            
            results.append({
                'test_name': method_name,
                'status': status,
                'latency_ms': round(latency, 2),
                'message': message
            })
            latencies.append(latency)
            
            if status == 'PASS':
                success_count += 1
            else:
                error_count += 1

    total_tests = len(results)
    overall_status = 'PASS' if error_count == 0 else 'FAIL'
    
    avg_latency = round(np.mean(latencies), 2) if latencies else 0.0
    p95_latency = round(np.percentile(latencies, 95), 2) if latencies else 0.0
    error_rate = round((error_count / total_tests) * 100, 2) if total_tests > 0 else 0.0

    return {
        'timestamp': datetime.now().isoformat(),
        'status': overall_status,
        'total_tests': total_tests,
        'success_count': success_count,
        'error_count': error_count,
        'avg_latency': avg_latency,
        'p95_latency': p95_latency,
        'error_rate': error_rate,
        'results': results
    }
