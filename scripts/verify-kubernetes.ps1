param([switch]$ArchiveExported, [switch]$ImageLoaded)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
function K {
    & kubectl --kubeconfig .lab/kubeconfig --context kind-inventory-lab @args
    if ($LASTEXITCODE -ne 0) { throw "kubectl failed: $args" }
}
function Capture([string]$stage) {
    $process = Start-Process powershell.exe -WindowStyle Maximized -PassThru -ArgumentList @('-NoProfile','-File',"$PWD/scripts/capture-terminal.ps1",'-Stage',$stage)
    Wait-Process -Id $process.Id -Timeout 60
    if (!(Test-Path "evidence/terminal-$stage.png")) { throw "Missing live screenshot: $stage" }
}
function VerifyCount([int]$count) {
    K rollout status deployment/mini-inventory --timeout=180s
    for ($attempt = 0; $attempt -lt 40; $attempt++) {
        $pods = K get pods -l app=mini-inventory -o json | ConvertFrom-Json
        $ready = @($pods.items | Where-Object { !$_.metadata.deletionTimestamp -and $_.status.phase -eq 'Running' -and $_.status.containerStatuses[0].ready })
        if ($pods.items.Count -eq $count -and $ready.Count -eq $count) { break }
        Start-Sleep -Seconds 2
    }
    if ($pods.items.Count -ne $count -or $ready.Count -ne $count) { throw "Expected $count Ready pods" }
    $pods | ConvertTo-Json -Depth 40 | Set-Content -Encoding UTF8 "evidence/kubernetes-pods-$count.json"
    K get 'deployment,pods,service'
}
Start-Transcript evidence/kubernetes-run.txt
if (!$ArchiveExported -and !$ImageLoaded) {
    & docker image save --platform linux/amd64 --output .lab/mini-inventory-image.tar mini-inventory:1.0.0
    if ($LASTEXITCODE -ne 0) { throw 'Single-platform image export failed' }
}
if (!$ImageLoaded) {
    # Import the archive locally in the dedicated node, avoiding the stalled streaming path.
    & docker cp .lab/mini-inventory-image.tar inventory-lab-control-plane:/mini-inventory-image.tar
    if ($LASTEXITCODE -ne 0) { throw 'Image archive copy failed' }
    & docker exec inventory-lab-control-plane ctr --namespace=k8s.io images import --local --platform linux/amd64 --snapshotter overlayfs /mini-inventory-image.tar
    if ($LASTEXITCODE -ne 0) { throw 'Node-local image import failed' }
}
$apiReady = $false
for ($attempt = 0; $attempt -lt 60; $attempt++) {
    try { K get --raw /readyz | Out-Null; $apiReady = $true; break }
    catch { Start-Sleep -Seconds 2 }
}
if (!$apiReady) { throw 'Cluster API did not become ready' }
K apply -f k8s/deployment.yaml -f k8s/service.yaml
VerifyCount 3
Capture Kubernetes3
K scale deployment/mini-inventory --replicas=5
VerifyCount 5
Capture Kubernetes5
K scale deployment/mini-inventory --replicas=3
VerifyCount 3
Capture KubernetesFinal
K get deployment mini-inventory -o yaml | Set-Content -Encoding UTF8 evidence/kubernetes-deployment.yaml
K get events --sort-by=.lastTimestamp | Set-Content evidence/kubernetes-events.txt
K get nodes -o wide | Set-Content evidence/kubernetes-nodes.txt
K get endpointslices -o yaml | Set-Content evidence/kubernetes-endpoints.yaml
Stop-Transcript
