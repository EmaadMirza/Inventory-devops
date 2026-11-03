# Execution checkpoint - 3 November 2026

## Verified execution
- Docker client/server access works. No Docker permission changes, API exposure, or host-wide Docker configuration changes.
- Reviewed all 24 prepared files. Fixed Docker build context exclusions, Jenkins Java compatibility, Ansible service readiness/key permissions, and verification-script quoting/API readiness.
- Maven clean verify: 7 tests, 0 failures/errors; executable target/mini-inventory.jar.
- Live executable JAR and Docker image: each passed 9 HTTP checks.
- Real feature/low-stock-filter commit 8ae847a and --no-ff merge e7dc7ea into main. Both local and remote branches retained.
- GitHub: https://github.com/EmaadMirza/Inventory-devops
- Jenkins localhost:18081; occupied port 8081 left untouched. Build #2 SUCCESS, Started by an SCM change, 7 published tests, archived JAR. Exact artifact SHA256 and results are in evidence/jenkins-summary.json.
- Ansible role generator executed. First deployment ok=8 changed=5 failed=0; handler ran. Second run ok=7 changed=0 failed=0. Supervisor managed the actual application and health returned UP. Genuine third-run screenshot also shows zero changes.
- Docker image mini-inventory:1.0.0 built and HTTP-verified as non-root.
- Kind v0.33.0 checksum verified; Kubernetes v1.36.4 node. Dedicated .lab/kubeconfig and kind-inventory-lab context preserve existing contexts.
- Kubernetes Deployment and Service executed. Scaling 3 Ready -> 5 Ready -> 3 Ready verified twice (second run retook screenshots). Service API and each final replica health verified. Startup/readiness/liveness probes present.
- Streaming image import stalled; single-platform archive plus node-local containerd --local import succeeded. No Docker settings changed. Initial unsuccessful transcripts retained.
- Genuine Git/Maven/Docker/Ansible/Kubernetes terminal screenshots inspected. Wrong foreground captures rejected into ignored .lab, excluded from deliverables.
- Two PDF reports generated and visually reviewed: Component 1 10 pages; Component 2 13 pages. Component 1 is explicitly a review draft pending Jenkins browser screenshots.
- Storage attribution saved in evidence/disk-usage.json: approximately 7.59 decimal GB assignment logical usage, excluding pre-existing/shared data and avoiding shared-layer double-counting. Snapshot precedes final source ZIP.

## Remaining genuine blocker
Browser automation stopped because it could not verify the current browser URL on Windows. Browser UI input stopped. Genuine Jenkins browser screenshots remain pending. API/terminal evidence is not represented as browser screenshots. Component 1 must be regenerated with those screenshots before claiming the entire assignment complete.

Manual next step: with this lab's Jenkins running, open http://127.0.0.1:18081/job/Mini-Inventory/2/ in a normal browser window and signal readiness for capture. Also capture its Test Result page and archived artifact section.

## Isolation and preservation
Stages ran sequentially. Kubernetes and Ansible target are stopped to recover RAM; their data and configuration remain. Jenkins may be started alone for browser evidence. The cluster can resume with docker start inventory-lab-control-plane; wait for its API before using the dedicated kubeconfig.

Secrets remain in ignored .secrets. Downloads, exported image and QA files remain in ignored .lab. No unrelated projects, existing images, volumes, or earlier Jenkins assignment were deleted or altered. Nothing deleted for disk recovery. No coordinator invitation sent.
