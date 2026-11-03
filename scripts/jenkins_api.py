"""Authenticated localhost Jenkins requests; secrets remain in ignored .secrets."""
import base64
import http.cookiejar
import json
from pathlib import Path
import sys
import urllib.request

root = Path(__file__).resolve().parent.parent
base = "http://127.0.0.1:18081/"
password = (root / ".secrets/jenkins-admin-password").read_text().strip()
authorization = "Basic " + base64.b64encode(("emaad:" + password).encode()).decode()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
opener.addheaders = [("Authorization", authorization)]

def request(path, data=None, content_type="application/xml"):
    headers = {"Content-Type": content_type}
    if data is not None:
        crumb = json.load(opener.open(base + "crumbIssuer/api/json", timeout=30))
        headers[crumb["crumbRequestField"]] = crumb["crumb"]
    return opener.open(urllib.request.Request(base + path, data=data, headers=headers), timeout=60).read()

if __name__ == "__main__":
    path = sys.argv[1]
    data = Path(sys.argv[2]).read_bytes() if len(sys.argv) > 2 else None
    sys.stdout.buffer.write(request(path, data))
