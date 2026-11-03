"""Create reports from executed evidence. Original screenshots are embedded unchanged."""
import json
from pathlib import Path
import textwrap
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Preformatted, Table, TableStyle
from PIL import Image as PILImage

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output/pdf"
OUT.mkdir(parents=True, exist_ok=True)
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CodeSmall", fontName="Courier", fontSize=7, leading=9))
styles.add(ParagraphStyle(name="CaptionSmall", fontSize=9, leading=12, textColor=colors.HexColor("#435366"), spaceAfter=12))
styles["BodyText"].fontSize = 10
styles["BodyText"].leading = 14
styles["BodyText"].spaceAfter = 8
styles["Heading1"].textColor = colors.HexColor("#123c63")
styles["Heading2"].textColor = colors.HexColor("#176a83")

def read(path):
    raw = (ROOT / path).read_bytes()
    return raw.decode("utf-16" if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8-sig", errors="replace")

def para(story, text):
    story.append(Paragraph(text, styles["BodyText"]))

def heading(story, text, level=1):
    story.append(Paragraph(text, styles[f"Heading{level}"]))

def code(story, path, lines=None):
    heading(story, escape(path), 2)
    source = read(path)
    if lines:
        source = "\n".join(source.splitlines()[-lines:])
    wrapped = []
    for line in source.expandtabs(4).splitlines():
        wrapped.extend(textwrap.wrap(line, width=108, subsequent_indent="    ",
                                     replace_whitespace=False, drop_whitespace=False) or [""])
    story.append(Preformatted("\n".join(wrapped), styles["CodeSmall"]))
    story.append(Spacer(1, 10))

def screenshot(story, name, caption):
    path = ROOT / "evidence" / name
    assert path.exists(), path
    story.append(PageBreak())
    heading(story, caption)
    with PILImage.open(path) as im:
        width, height = im.size
    factor = min(500 / width, 620 / height)
    story.append(Image(str(path), width=width * factor, height=height * factor))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Original screenshot: evidence/" + escape(name) + ". Embedded without alteration; zoom to inspect command output.", styles["CaptionSmall"]))
    if name.startswith("jenkins-browser-"):
        provenance = json.loads(read("evidence/jenkins-browser-provenance.json"))
        story.append(Paragraph("Live Jenkins page captured with Playwright and installed Google Chrome in headless mode. Capture time: " + escape(provenance["captured_local"]) + ". The displayed build executed on 3 November 2026.", styles["CaptionSmall"]))

def table(story, rows):
    wrapped = [[Paragraph(escape(str(cell)), styles["BodyText"]) for cell in row] for row in rows]
    t = Table(wrapped, colWidths=[155, 345], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#e8f0f6")),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#cbd7e3")),
        ("LEFTPADDING", (0,0), (-1,-1), 8), ("RIGHTPADDING", (0,0), (-1,-1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#cad7e3"))
    canvas.line(48, 42, A4[0]-48, 42)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#435366"))
    canvas.drawString(48, 29, "Emaad Mirza | 1ms24cy020 | Mini Inventory DevOps")
    canvas.drawRightString(A4[0]-48, 29, str(doc.page))
    canvas.restoreState()

def cover(story, component, subtitle, pending=False):
    story.append(Spacer(1, 80))
    story.append(Paragraph("MINI INVENTORY", styles["Title"]))
    story.append(Paragraph(component, styles["Heading1"]))
    para(story, subtitle)
    story.append(Spacer(1, 35))
    table(story, [["Student", "Emaad Mirza"], ["USN", "1ms24cy020"],
                  ["Execution date", "3 November 2026"], ["Platform", "Windows and Docker Desktop"],
                  ["Repository", "https://github.com/EmaadMirza/Inventory-devops"]])
    if pending:
        para(story, "<b>Evidence checkpoint:</b> Backend execution is verified. Jenkins browser screenshots are pending because browser automation could not verify the Windows browser URL. This report is a review draft until those screenshots are inserted; terminal/API records below are genuine and are not described as browser screenshots.")
    para(story, "This report records observed execution results. Configuration listings are the reviewed assignment source. Screenshots originate from actual terminal or Jenkins sessions. No coordinator invitation is claimed.")
    story.append(PageBreak())

def refs(story, sources):
    heading(story, "References")
    for title, url in sources:
        para(story, f'{escape(title)}. <link href="{escape(url)}" color="#176a83">{escape(url)}</link>. Accessed 3 November 2026.')

ci = json.loads(read("evidence/jenkins-summary.json"))
assert ci["result"] == "SUCCESS" and ci["tests"] == 7
assert "changed=0" in read("evidence/ansible-run-2.txt")
pods = json.loads(read("evidence/kubernetes-pods-3.json"))
assert len(pods["items"]) == 3
browser_shots = sorted((ROOT / "evidence").glob("jenkins-browser-*.png"))
browser_complete = all((ROOT / "evidence" / name).exists() for name in ["jenkins-browser-1-build.png", "jenkins-browser-2-tests.png", "jenkins-browser-3-config.png", "jenkins-browser-4-pipeline.png", "jenkins-browser-5-polling.png"])

one = []
cover(one, "Component 1: Build and Continuous Integration", "Java REST API, Git workflow, Maven testing and automatic Jenkins SCM builds", pending=not browser_complete)
heading(one, "Abstract")
para(one, "A small inventory REST service was developed in Java and packaged as an executable Maven JAR. Git preserved a real feature branch and merge. Jenkins checked out the GitHub repository, ran automated tests, packaged the service and archived its artifact. A later documentation push was detected automatically by SCM polling. All seven automated tests passed; live JAR and Docker HTTP checks returned the expected success and error responses.")
heading(one, "Introduction")
para(one, "Manual builds are difficult to reproduce and can distribute untested changes. This assignment connects version control, automated validation and artifact publication around one inspectable service. The inventory application supplies product creation, lookup, listing and stock updates. Its low-stock filter is an enhancement with a clear replenishment use case.")
heading(one, "Implementation: environment and review")
para(one, "The work used an 8 GB Windows laptop with Docker Desktop 4.91.0 and Docker Engine 29.8.0. Initial inspection found roughly 1.8 GB free host RAM, 18.7 GB free on C:, four cached unrelated images and no containers. None of those images supplied the required Java/Jenkins runtimes. Downloads and running services were staged sequentially. Existing projects and the earlier Jenkins assignment were retained. Resource snapshots are in evidence/resources.txt.")
para(one, "All 24 prepared files were reviewed before execution. The root Docker ignore file incorrectly excluded the Ansible target entrypoint and was corrected. Jenkins was moved from its prepared Java 17 tag to lts-jdk21 to meet current requirements. The image actually ran Jenkins 2.580.2 on Java 21.0.13. Port 8081 was occupied, so this isolated lab uses localhost:18081. Jenkins has one executor and a 1 GiB container limit; its Java heap is capped at 512 MiB.")
heading(one, "REST API design", 2)
table(one, [["Request", "Observed behavior"], ["GET /health", "200; UP and instance identity"],
            ["GET /products", "200; product list"], ["POST /products", "201; validated name and nonnegative integer stock"],
            ["GET /products/{id}", "200 for existing product, 404 otherwise"],
            ["PUT /products/{id}/stock", "200 update; 400 negative stock; 404 missing product"],
            ["GET /products?maxStock=N", "200; products whose stock is at most N"],
            ["Invalid input/method", "400 for malformed/product input; 405 for unsupported method"]])
para(one, "Inventory methods synchronize access to immutable Product records. JSON bodies are limited to 8 KiB, and the HTTP server uses a bounded worker queue. Maven compiles with release 17 and shades Gson into target/mini-inventory.jar. The service can therefore run without a separate dependency classpath.")
heading(one, "Git feature branch and real merge", 2)
para(one, "The baseline commit was a783f65. Branch feature/low-stock-filter added GET /products?maxStock=N and a real HTTP regression test in commit 8ae847a. Main merged it with --no-ff in commit e7dc7ea, preserving both parents. Main and the feature branch were pushed to the new Inventory-devops repository. No history rewrite or branch deletion was used.")
heading(one, "Jenkins automatic SCM pipeline", 2)
para(one, "The Pipeline from SCM job uses the public GitHub repository, branch */main and Jenkinsfile. Build #1 was intentionally started once to register polling. A real documentation commit a61cb7c was then pushed. The configured once-per-minute poll found that revision and scheduled build #2. Its recorded cause is hudson.triggers.SCMTrigger$SCMTriggerCause, with description 'Started by an SCM change'. No build request was sent for build #2.")
para(one, "The pipeline checks out source, runs mvn clean test, and packages only after the test stage succeeds. Its post block publishes Surefire XML through JUnit and archives the executable JAR with fingerprinting. A timeout, retention policy and disabled concurrent builds keep the lab bounded. Local writes require the generated emaad account; read-only results are accessible on the loopback-only Jenkins port. Credentials are excluded from Git and the package.")
heading(one, "Enhancement rationale")
para(one, "The low-stock filter makes the demo useful for identifying items requiring replenishment. It operates on a snapshot of inventory without mutating products. Its regression test creates products above and below a threshold, checks the filtered response, verifies the full inventory remains intact, and rejects a negative threshold. This is the actual change committed and merged on the feature branch. Automated HTTP tests extend the original three inventory tests to exercise the application boundary.")
heading(one, "Actual results")
table(one, [["Check", "Actual result"], ["Maven clean verify", "BUILD SUCCESS; 7 tests; 0 failures/errors/skips"],
            ["Executable JAR HTTP", "9 checks passed, including 201/400/404/405 behavior"],
            ["Git", "Real merge e7dc7ea; main and feature branch retained locally/remotely"],
            ["Jenkins #1", "SUCCESS; JUnit results and JAR archived"],
            ["Jenkins #2", "SUCCESS; Started by an SCM change; 7 tests, 0 failures"],
            ["Archived JAR", f"{ci['jar_bytes']:,} bytes; target/mini-inventory.jar"],
            ["Artifact SHA256", ci["jar_sha256"]]])
para(one, "The local Maven/JDK 17 JAR and the Jenkins/JDK 21 JAR need not have identical bytes because build timestamps and compiler versions differ. The archived JAR was downloaded through Jenkins and its actual checksum recorded. The application image was separately built and checked; those results are also included in Component 2.")
for name, caption in [("terminal-Git.png", "Evidence: real Git merge and preserved branches"),
                      ("terminal-Maven.png", "Evidence: live Maven verification")]:
    screenshot(one, name, caption)
for shot in browser_shots:
    if shot.name == 'jenkins-browser-3-config.png':
        continue  # Full-page original is retained; use readable viewport details in the PDF.
    captions = {"jenkins-browser-1-build.png":"Evidence: SCM-triggered success and archived JAR", "jenkins-browser-2-tests.png":"Evidence: seven tests passing in Jenkins", "jenkins-browser-4-pipeline.png":"Evidence: GitHub SCM pipeline configuration", "jenkins-browser-5-polling.png":"Evidence: automatic SCM polling schedule"}
    screenshot(one, shot.name, captions.get(shot.name,"Evidence: genuine Jenkins browser view"))
one.append(PageBreak())
heading(one, "Conclusion")
para(one, "The API, executable artifact, feature workflow and automatic SCM-triggered CI were executed successfully. The results demonstrate tested changes flowing from GitHub to a published Jenkins artifact. Genuine browser-rendered Jenkins evidence shows the SCM build cause, archived JAR, test results and job configuration. Inventory remains process-local and is unsuitable for shared state across replicas; a production version should use a shared database and authenticated API access.")
refs(one, [("Apache Maven lifecycle", "https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html"),
           ("Jenkins Pipeline syntax and pollSCM", "https://www.jenkins.io/doc/book/pipeline/syntax/"),
           ("Jenkins Java support", "https://www.jenkins.io/doc/book/platform-information/support-policy-java/"),
           ("Git merge", "https://git-scm.com/docs/git-merge"),
           ("Assignment repository and execution evidence", "https://github.com/EmaadMirza/Inventory-devops")])
one.append(PageBreak())
heading(one, "Code and configuration listings")
for path in ["pom.xml", "src/main/java/com/emaad/inventory/Inventory.java", "src/main/java/com/emaad/inventory/App.java", "src/test/java/com/emaad/inventory/InventoryTest.java", "src/test/java/com/emaad/inventory/ApiTest.java", "Jenkinsfile", "infra/jenkins/Dockerfile", "infra/jenkins/job.xml"]:
    code(one, path)
SimpleDocTemplate(str(OUT / "Emaad-Mirza-Component-1-CI.pdf"), pagesize=A4, leftMargin=48, rightMargin=48, topMargin=48, bottomMargin=55, title="Mini Inventory - Component 1", author="Emaad Mirza").build(one, onFirstPage=footer, onLaterPages=footer)

two = []
cover(two, "Component 2: Automated Deployment", "Ansible managed service, Docker packaging and Kubernetes scaling with health probes")
heading(two, "Abstract")
para(two, "The tested inventory JAR was deployed to an isolated SSH target using an Ansible role, variable, template and restart handler. A repeated run reported zero changes. A non-root Docker image passed live HTTP checks. The same image was loaded into a dedicated Kind cluster, exposed through a Kubernetes Service and scaled from three to five and back to three Ready replicas. Startup, readiness and liveness probes provide explicit health behavior.")
heading(two, "Introduction")
para(two, "This component turns a built artifact into a managed application and a repeatable container deployment. Ansible expresses target configuration, Docker packages the runtime, and Kubernetes maintains the requested number of healthy instances. The demonstration keeps persistent inventory consistency outside scope: each replica owns an independent in-memory inventory.")
heading(two, "Implementation: environment and sequence")
para(two, "Stages ran sequentially on Windows with existing Docker Desktop. Jenkins was stopped before the Ansible deployment. The Ansible target was stopped before cluster creation. A dedicated cluster name and .lab/kubeconfig isolated this work from existing Kubernetes contexts. Kubectl 1.36.1 was already supplied by Docker Desktop. Only Kind v0.33.0 was downloaded locally, and its SHA256 was checked against the official release. The pinned official node image is Kubernetes v1.36.4, matching kubectl's minor version.")
heading(two, "Ansible inventory, role and variable", 2)
para(two, "The inventory defines inventory-target in inventory_servers, reached over the private Compose network with a dedicated ED25519 key. SSH is not published to the Windows host, and password login is disabled. ansible-galaxy role init inventory_app actually generated a skeleton in .lab; the reviewed prepared role was reconciled into it. The role's default app_port is 8080, explicitly shown as a playbook variable. Defaults also supply the application directory and artifact source.")
para(two, "Tasks install the Java runtime and Supervisor, create /opt/mini-inventory, copy the JAR and render inventory.conf.j2. Changed files notify Restart inventory service; flush_handlers applies configuration before process and HTTP checks. Process readiness is retried to avoid racing Supervisor's STARTING state. The controller copies the mounted private key into a 0600 Linux file because Windows bind-mount permissions are unsuitable for OpenSSH private keys.")
heading(two, "Managed service and platform adaptation", 2)
para(two, "The isolated Debian target does not boot systemd. Supervisor is therefore the actual service manager, with autostart and autorestart enabled for the Java process. This is an explicit adaptation, not evidence of a systemd service run. The first play reported ok=8, changed=5, unreachable=0, failed=0 and executed the restart handler. The second reported ok=7, changed=0, unreachable=0, failed=0. The service kept PID 1243 across verification. A third actual run was captured on screen and again showed zero changes and HTTP status UP.")
heading(two, "Docker image and API verification", 2)
para(two, "The runtime image uses eclipse-temurin:17-jre-jammy, copies the executable JAR and runs as UID/GID 10001 with a 96 MiB maximum heap. The corrected Docker ignore rules permit the Ansible target entrypoint while excluding secrets and report/evidence directories from the application context. The image mini-inventory:1.0.0 built successfully. A 192 MiB test container bound only localhost:8083 and passed nine live HTTP checks before being stopped.")
heading(two, "Kubernetes Deployment, Service and scaling", 2)
para(two, "Kind loaded the already-built local image. The Deployment specifies three replicas and imagePullPolicy Never, avoiding a registry upload and repeated pulls. Its ClusterIP Service maps port 80 to container port 8080 and selects app=mini-inventory. The application uses a non-root security context, drops Linux capabilities and has a read-only root filesystem. Each replica requests 25 millicores/64 MiB and is limited to 250 millicores/160 MiB.")
para(two, "The original streaming image import stalled. A single-platform linux/amd64 archive was exported, copied into the dedicated node's root filesystem and successfully imported with containerd's supported --local mode. Docker's host settings and permissions were not changed. The reproducible procedure is in scripts/verify-kubernetes.ps1; initial unsuccessful transcripts are retained separately.")
para(two, "The deployment rolled out at three replicas, scaled to five Ready pods and returned to three. Each stage was verified against live pod readiness and captured in a terminal screenshot. Service endpoints and API responses were checked through localhost port-forwarding. Scaling evidence uses health and independent instances; it does not imply shared product data or load-test performance.")
heading(two, "Enhancement rationale: health-aware deployment")
para(two, "A running process is insufficient evidence that an application can serve requests. The startup probe allows up to 60 seconds for initialization before other health checks begin. Readiness probes remove an unready instance from Service endpoints, while liveness probes permit Kubernetes to restart a persistently unhealthy container. All three call /health. The saved deployment and Ready pods verify the configured probes and healthy operation; no fault-injection or measured outage-recovery claim is made.")
para(two, "During the observed initial startup, probe events recorded connection refusals and timeouts before the pods became Ready. The three initial containers subsequently reached readiness without restarts. These transient events are retained rather than omitted; they demonstrate that startup readiness was actually evaluated, without constituting an induced failure-recovery experiment.")
para(two, "The node was later deliberately stopped to recover RAM and restarted to retake screenshots that had captured the wrong foreground window. Later screenshots therefore show restart counters from that node restart. Only screenshots inspected as the actual verification console are included; rejected captures remain outside the deliverables in ignored .lab.")
heading(two, "Actual results")
table(two, [["Check", "Actual result"], ["Role generator", "ansible-galaxy role init succeeded"],
            ["Ansible first run", "ok=8 changed=5 unreachable=0 failed=0; handler executed"],
            ["Ansible second run", "ok=7 changed=0 unreachable=0 failed=0"],
            ["Managed service", "Supervisor RUNNING; /health returned UP"],
            ["Docker image", "Build succeeded; 9 live HTTP checks passed"],
            ["Kubernetes scaling", "3 Ready -> 5 Ready -> 3 Ready"],
            ["Service and health", "Live endpoints and HTTP responses saved in evidence"],
            ["Health probes", "Startup/readiness/liveness configured; final pods Ready"]])
for name, caption in [("terminal-Ansible.png", "Evidence: idempotent Ansible run and managed health"),
                      ("terminal-Docker.png", "Evidence: live Docker API checks"),
                      ("terminal-Kubernetes3.png", "Evidence: initial three Ready replicas"),
                      ("terminal-Kubernetes5.png", "Evidence: five Ready replicas"),
                      ("terminal-KubernetesFinal.png", "Evidence: return to three Ready replicas")]:
    screenshot(two, name, caption)
two.append(PageBreak())
heading(two, "Conclusion")
para(two, "The deployment chain was executed using a managed SSH target, an idempotent Ansible role, a verified Docker image and a dedicated Kubernetes cluster. The requested scaling cycle completed with health probes present and replicas Ready. The main limitation is process-local inventory. Shared persistence, application authentication and production-grade multi-node infrastructure remain future work. Neither a production high-availability guarantee nor fault-recovery performance is claimed.")
refs(two, [("Ansible handlers", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_handlers.html"),
           ("Ansible roles", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html"),
           ("Dockerfile reference", "https://docs.docker.com/reference/dockerfile/"),
           ("Kind v0.33.0 release and node digests", "https://github.com/kubernetes-sigs/kind/releases/tag/v0.33.0"),
           ("Kind image-store known issues", "https://kind.sigs.k8s.io/docs/user/known-issues/"),
           ("Kubernetes health probes", "https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/"),
           ("Kubernetes Deployments", "https://kubernetes.io/docs/concepts/workloads/controllers/deployment/")])
two.append(PageBreak())
heading(two, "Code and configuration listings")
for path in ["compose.yaml", "ansible/inventory.ini", "ansible/playbook.yml", "ansible/roles/inventory_app/defaults/main.yml", "ansible/roles/inventory_app/tasks/main.yml", "ansible/roles/inventory_app/handlers/main.yml", "ansible/roles/inventory_app/templates/inventory.conf.j2", "infra/ansible-controller/Dockerfile", "infra/ansible-controller/entrypoint.sh", "infra/ansible-target/Dockerfile", "infra/ansible-target/start.sh", "Dockerfile", "k8s/kind.yaml", "k8s/deployment.yaml", "k8s/service.yaml"]:
    code(two, path)
SimpleDocTemplate(str(OUT / "Emaad-Mirza-Component-2-Deployment.pdf"), pagesize=A4, leftMargin=48, rightMargin=48, topMargin=48, bottomMargin=55, title="Mini Inventory - Component 2", author="Emaad Mirza").build(two, onFirstPage=footer, onLaterPages=footer)
print("Created two evidence-based reports in", OUT)
