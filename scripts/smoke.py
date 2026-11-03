"""Exercise a running executable JAR/container through the real HTTP API."""
import json
import sys
import urllib.request
import urllib.error

base = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8083"

def check(method, path, expected, body=None):
    data = None if body is None else json.dumps(body).encode()
    request = urllib.request.Request(base + path, data=data, method=method,
                                     headers={"Content-Type": "application/json"})
    try:
        response = urllib.request.urlopen(request, timeout=15)
    except urllib.error.HTTPError as error:
        response = error
    with response:
        result = json.loads(response.read())
        print(f"{method} {path} -> {response.status}: {json.dumps(result)}", flush=True)
        assert response.status == expected, (path, response.status, expected)
        return result

check("GET", "/health", 200)
check("GET", "/products", 200)
product = check("POST", "/products", 201, {"name": "Smoke product", "stock": 3})
path = f"/products/{product['id']}"
assert check("GET", path, 200)["stock"] == 3
assert check("PUT", path + "/stock", 200, {"stock": 7})["stock"] == 7
assert all(p["stock"] <= 7 for p in check("GET", "/products?maxStock=7", 200))
check("POST", "/products", 400, {"name": "Invalid", "stock": -1})
check("PUT", "/products/999999/stock", 404, {"stock": 1})
check("POST", "/health", 405, {})
print("PASS: 9 HTTP checks", flush=True)
