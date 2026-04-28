
import requests
import time

def make_request(method, url, params=None, json_data=None, headers=None, timeout=5, max_retries=1, delay_between_retries=1):
    for i in range(max_retries + 1):
        start_time = time.time()
        try:
            if method.upper() == 'GET':
                response = requests.get(url, params=params, headers=headers, timeout=timeout)
            elif method.upper() == 'POST':
                response = requests.post(url, params=params, json=json_data, headers=headers, timeout=timeout)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            latency = (time.time() - start_time) * 1000  # Latency in ms
            return response, latency, None # No error

        except requests.exceptions.Timeout:
            error_msg = f"Request timed out after {timeout} seconds"
        except requests.exceptions.ConnectionError:
            error_msg = "Connection error occurred"
        except requests.exceptions.RequestException as e:
            error_msg = f"An unexpected request error occurred: {e}"
        
        latency = (time.time() - start_time) * 1000 # Still measure latency even on error
        print(f"Attempt {i+1}/{max_retries+1} failed for {url}: {error_msg}")
        if i < max_retries:
            time.sleep(delay_between_retries)

    return None, latency, error_msg # All retries failed
