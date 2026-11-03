# Mini Inventory API - DevOps assignment

**Emaad Mirza | USN 1ms24cy020**

Repository: https://github.com/EmaadMirza/Inventory-devops

## Application and enhancement
Java 17 REST API, built with Maven. The executable shaded JAR includes Gson.

| Endpoint | Purpose |
| --- | --- |
| GET /health | Health and container identity |
| GET /products | List inventory |
| POST /products | Create: {"name":"Notebook","stock":10} |
| GET /products/1 | Find a product; missing product returns 404 |
| PUT /products/1/stock | Update: {"stock":15} |
| GET /products?maxStock=5 | Enhancement: find products needing replenishment |

Invalid product data returns 400; unsupported methods return 405. Request bodies are limited to 8 KiB. Inventory uses synchronized operations and a bounded HTTP worker pool.

The low-stock filter was implemented and tested on `feature/low-stock-filter`, then merged into `main` with `--no-ff`. Both local and remote branches are preserved. Seven automated tests cover inventory rules and real HTTP behavior. See evidence/git-merge.txt and target/surefire-reports.

## Resource-conscious execution
Use Windows and Docker Desktop. Execute one stage at a time. Existing unrelated images, containers, volumes, repositories and the earlier Jenkins assignment are preserved. This lab uses the Compose project `mini-inventory-lab` and the separate Kind context `kind-inventory-lab`.

Build: `docker compose --profile build run --rm maven`

Executable JAR: `target/mini-inventory.jar`. Live HTTP verification: `python scripts/smoke.py http://127.0.0.1:8083` (single replica).

Jenkins: `docker compose --profile ci up -d --build jenkins`, at **http://127.0.0.1:18081**. Port 8081 was occupied and was left untouched. Pipeline job: `Mini-Inventory`; its definition is in infra/jenkins/job.xml. Jenkinsfile polls GitHub once per minute, tests before packaging, publishes JUnit results and archives the JAR. A manual first build registers polling; subsequent SCM changes trigger automatically. The local account is `emaad`; its generated password is in ignored `.secrets/jenkins-admin-password`. The localhost-only lab allows anonymous read access to results; writes require authentication. It has no Docker socket or Docker API access.

Before Ansible/Kubernetes, stop only this Jenkins: `docker compose --profile ci stop jenkins`.

Ansible: generate the dedicated `.secrets/id_ed25519` key, start `inventory-target`, then run the controller with `docker compose --profile ansible run --rm --build ansible`. Inventory, playbook, role defaults, tasks, template and restart handler are under ansible/. The service manager is Supervisor because this isolated container does not boot systemd. The controller copies the Windows-mounted key to a private 0600 Linux file. Run twice to verify idempotence. Application endpoint: http://127.0.0.1:8082/health. Stop the target before cluster work.

Docker: `docker build -t mini-inventory:1.0.0 .`, then `docker run --rm -d --name mini-inventory-smoke -p 127.0.0.1:8083:8080 --memory 192m mini-inventory:1.0.0`. Run the smoke script and stop that named container.

Kubernetes: create the dedicated `inventory-lab` Kind cluster using k8s/kind.yaml; load the local image. Use `--context kind-inventory-lab` on every kubectl mutation. Apply k8s/deployment.yaml and k8s/service.yaml, verify 3 Ready replicas, scale to 5 and back to 3. The deployment has startup, readiness and liveness probes, bounded resources and a non-root process. Port-forward service/mini-inventory 8084:80 to inspect the API.

## Limitations and evidence
Inventory is process-local and resets on restart. Replicas do not share a database. Scaling checks use health responses and independent replicas; use one replica for stateful smoke checks. A production version needs shared persistence and authentication.

Evidence contains actual logs and unaltered screenshots. STATUS.md distinguishes completed and pending work. Reports must only claim observed results. Coordinator invitation remains deferred.
