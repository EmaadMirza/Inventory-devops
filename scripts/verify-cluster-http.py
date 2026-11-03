import json
from pathlib import Path
import subprocess
import time
import urllib.request

root = Path(__file__).resolve().parent.parent
log = root / "evidence/kubernetes-http.txt"
command = ["kubectl", "--kubeconfig", str(root / ".lab/kubeconfig"),
           "--context", "kind-inventory-lab"]
results = []
with open(root / "evidence/kubernetes-port-forward.txt", "w") as output:
    process = subprocess.Popen(command + ["port-forward", "--address", "127.0.0.1",
                                         "service/mini-inventory", "8084:80"],
                               stdout=output, stderr=subprocess.STDOUT,
                               creationflags=subprocess.CREATE_NO_WINDOW)
    try:
        for attempt in range(40):
            try:
                response = urllib.request.urlopen("http://127.0.0.1:8084/health", timeout=3)
                health = json.load(response)
                assert health["status"] == "UP"
                results.append("Service port-forward GET /health -> 200: " + json.dumps(health))
                break
            except Exception:
                if attempt == 39:
                    raise
                time.sleep(1)
        with urllib.request.urlopen("http://127.0.0.1:8084/products", timeout=15) as response:
            products = json.load(response)
            assert {p["name"] for p in products} == {"Notebook", "Pen"}
            results.append("Service port-forward GET /products -> 200: " + json.dumps(products))
        pods = json.loads(subprocess.check_output(command + ["get", "pods", "-l", "app=mini-inventory", "-o", "json"]))
        assert len(pods["items"]) == 3
        for pod in pods["items"]:
            name = pod["metadata"]["name"]
            result = json.loads(subprocess.check_output(command + ["get", "--raw", f"/api/v1/namespaces/default/pods/{name}:8080/proxy/health"]))
            assert result["status"] == "UP" and result["instance"] == name
            results.append("Pod proxy health -> 200: " + json.dumps(result))
        results.append("PASS: Service API and all 3 replica health identities verified")
    finally:
        process.terminate()
        process.wait(timeout=15)
log.write_text("\n".join(results) + "\n", encoding="utf-8")
print(log.read_text())
