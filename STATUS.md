# Completed assignment - 4 November 2026

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
- Two separate PDF reports finalized with explanations, code/configuration, enhancement rationale, actual results, genuine screenshots, conclusions and references.
- Storage attribution saved in evidence/disk-usage.json: approximately 7.59 decimal GB assignment logical usage, excluding pre-existing/shared data and avoiding shared-layer double-counting. Snapshot precedes final source ZIP.

## Final browser evidence
The existing-browser connector was unavailable, but CLI browser testing worked. Playwright 1.63.0 reused installed Google Chrome in an isolated headless context. Genuine live Jenkins UI screenshots were captured on 4 November, showing the historical 3 November build #2, its SCM-triggered cause, archived JAR, seven passing tests and current SCM/polling configuration. No responses were mocked and no screenshot content was fabricated. The configuration form was read without saving changes. Timestamps, URLs and capture method are recorded in evidence/jenkins-browser-provenance.json.

Both reports and source-package.zip are finalized. The ZIP includes the runnable JAR and a verified complete Git history bundle preserving main and feature/low-stock-filter; it excludes credentials and runtime caches. No assignment requirements remain unexecuted. Coordinator invitation remains deferred by user instruction.

## Isolation and preservation
Stages ran sequentially. Kubernetes and Ansible target are stopped to recover RAM; their data and configuration remain. Jenkins may be started alone for browser evidence. The cluster can resume with docker start inventory-lab-control-plane; wait for its API before using the dedicated kubeconfig.

Secrets remain in ignored .secrets. Downloads, exported image and QA files remain in ignored .lab. No unrelated projects, existing images, volumes, or earlier Jenkins assignment were deleted or altered. Nothing deleted for disk recovery. No coordinator invitation sent.
