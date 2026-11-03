import hashlib
import json
from pathlib import Path
import re
from jenkins_api import request

out = Path("evidence")
build = json.loads(request("job/Mini-Inventory/2/api/json"))
assert not build["building"] and build["result"] == "SUCCESS", build.get("result")
causes = [c for a in build["actions"] for c in a.get("causes", [])]
assert any(c["_class"] == "hudson.triggers.SCMTrigger$SCMTriggerCause" for c in causes), causes
tests = json.loads(request("job/Mini-Inventory/2/testReport/api/json"))
total = tests["passCount"] + tests["failCount"] + tests["skipCount"]
assert tests["failCount"] == 0 and total == 7, tests
for number in (1, 2):
    for suffix, filename in [("api/json", f"jenkins-build-{number}.json"),
                             ("consoleText", f"jenkins-console-{number}.txt"),
                             ("testReport/api/json", f"jenkins-tests-{number}.json")]:
        (out / filename).write_bytes(request(f"job/Mini-Inventory/{number}/{suffix}"))
(out / "jenkins-job-config.xml").write_bytes(request("job/Mini-Inventory/config.xml"))
polling = request("job/Mini-Inventory/scmPollLog/").decode()
match = re.search(r"<pre>(.*?)</pre>", polling, flags=re.S)
(out / "jenkins-polling.txt").write_text(match.group(1) if match else polling, encoding="utf-8")
jar = request("job/Mini-Inventory/2/artifact/target/mini-inventory.jar")
Path(".lab/jenkins-mini-inventory.jar").write_bytes(jar)
summary = {"build": 2, "result": build["result"], "causes": causes,
           "tests": total, "failures": tests["failCount"],
           "artifacts": build["artifacts"], "jar_bytes": len(jar),
           "jar_sha256": hashlib.sha256(jar).hexdigest()}
(out / "jenkins-summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(json.dumps(summary, indent=2))
