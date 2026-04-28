
import requests
import time

class APIClient:
    def __init__(self, base_url, timeout=5, retries=1):
        self.base_url = base_url
        self.timeout = timeout
        self.retries = retries

    def _make_request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        for attempt in range(self.retries + 1):
            start_time = time.time()
            try:
                response = requests.request(method, url, timeout=self.timeout, **kwargs)
                latency_ms = (time.time() - start_time) * 1000
                return response, latency_ms
            except requests.exceptions.Timeout:
                latency_ms = (time.time() - start_time) * 1000
                if attempt < self.retries:
                    print(f"Timeout on {method} {url}, retrying...")
                    time.sleep(1) # Simple backoff
                else:
                    raise ConnectionError(f"Request to {url} timed out after {self.retries + 1} attempts") from None
            except requests.exceptions.RequestException as e:
                latency_ms = (time.time() - start_time) * 1000
                raise ConnectionError(f"Request to {url} failed: {e}") from e

    def get(self, endpoint, **kwargs):
        return self._make_request('GET', endpoint, **kwargs)

    def post(self, endpoint, json=None, **kwargs):
        return self._make_request('POST', endpoint, json=json, **kwargs)

    def put(self, endpoint, json=None, **kwargs):
        return self._make_request('PUT', endpoint, json=json, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self._make_request('DELETE', endpoint, **kwargs)
