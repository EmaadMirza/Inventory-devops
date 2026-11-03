# Mini Inventory API — DevOps assignment

**Student:** Emaad Mirza · **USN:** 1ms24cy020

## Current status
Prepared source/configuration only. Windows command execution is blocked by the session sandbox provisioning error. No successful build, image build, Jenkins run, Ansible run, cluster deployment, screenshot, or GitHub push is claimed. See STATUS.md.

## Application
Java 17+, Maven, JSON REST API. GET /products lists products; POST /products accepts {"name":"Notebook","stock":10}; PUT /products/1/stock accepts {"stock":15}; GET /health returns health and instance identity. Invalid inputs return 400, unknown products return 404. Initial demo products are Notebook and Pen.

Inventory is process-local and resets on restart. Kubernetes replicas do **not** share inventory. This is a pipeline demonstration, not a distributed inventory database. Use a single replica for consistent stateful interactions; scaling evidence uses health checks and independent replicas. A later production version should use a shared database.

## Deliverables
Component 1: meaningful feature branch + merge, Maven artifact, automatic Jenkins polling, three unit tests before packaging, JUnit publication and archived JAR.
Component 2: Ansible SSH target with variable, role and restart handler, Docker image, single-node Kind cluster, Deployment + Service, 3 → 5 → 3 replicas, readiness/liveness probes.

## Execution order (pending)
1. Inspect live Docker daemon, existing images/containers, WSL limits, disk and RAM. Reuse available compatible images before pulling any. Do not start all profiles together on an 8 GB machine.
2. Confirm a NEW GitHub repository URL. Initialize main, commit baseline, create a meaningful feature branch (for example add stock-update support), commit the actual change there, merge with --no-ff and retain both branches. Do not invent history or touch the earlier Jenkins assignment.
3. Build: docker compose --profile build run --rm maven
4. Smoke test the executable JAR in a runtime container, exercising create/list/update plus invalid data.
5. Start CI: docker compose --profile ci up -d --build jenkins. Open http://localhost:8081, complete initial local setup, create Pipeline from SCM using Jenkinsfile and the NEW repository. Supply credentials locally if private. Perform one initial build to register polling; then push a real change and wait for polling. Capture configuration, automatic cause, tests and archived artifact. Stop only this lab's Jenkins before cluster work when memory is tight.
6. Generate a dedicated SSH key in ignored .secrets using ssh-keygen -t ed25519 -f .secrets/id_ed25519. Use local tools; never commit the private key. The target is an isolated container; root SSH is key-only and SSH is not published on the host.
7. Prepare the role with ansible-galaxy init inventory_app in a temporary directory once Ansible is runnable, and reconcile the provided role files into that generated role. This PDF procedure is pending; no claim that the generator has run.
8. docker compose --profile ansible up -d --build inventory-target
9. docker compose --profile ansible run --rm --build ansible. Run twice and show the second run avoids unnecessary changes/restarts. Change a port/artifact only if demonstrating the handler, then restore and verify health. App is managed by Supervisor because a container does not boot systemd; document this adaptation explicitly.
10. Verify http://localhost:8082/health, then stop the target to recover memory.
11. docker build -t mini-inventory:1.0.0 .
12. docker run --rm -d --name mini-inventory-smoke -p 127.0.0.1:8083:8080 --memory 192m mini-inventory:1.0.0. Verify endpoints and stop this container.
13. Install Kind only if missing, using its official release and checksum. Reuse existing kubectl if compatible. kind create cluster --name inventory-lab --config k8s/kind.yaml
14. kind load docker-image mini-inventory:1.0.0 --name inventory-lab
15. kubectl --context kind-inventory-lab apply -f k8s/deployment.yaml -f k8s/service.yaml
16. kubectl --context kind-inventory-lab rollout status deployment/mini-inventory --timeout=180s
17. Capture get pods and get svc; port-forward service/mini-inventory 8084:80 and request /health and /products.
18. Scale deployment to 5, wait for rollout, capture 5 Ready pods, then scale to 3 and capture again. Use --context kind-inventory-lab on every kubectl mutation. Do not modify another cluster.
19. Inspect probe settings and Pod events; capture healthy Ready pods as the deployment enhancement evidence.
20. Complete both component reports only after execution; embed real screenshots. Commit source, reports and evidence to the new repo; exclude runtimes, credentials and caches. Coordinator invitation is deferred by user instruction.

## Evidence
Capture real Windows terminal and Jenkins browser windows. This assignment does not require Ubuntu specifically. Do not fabricate terminal images. Historical logs must be labelled as historical. Record tool versions, exact image tags/digests, build causes and actual outcomes. No screenshot exists yet.

## Reports
No supplied template. Use a clean title page and the required Abstract, Introduction, Implementation (environment/code/description), Enhancement rationale, Results, Conclusion and References for EACH component. Do not invent certificates, signatures, verification or execution results.
