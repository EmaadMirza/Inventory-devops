$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
New-Item -ItemType Directory -Force .lab | Out-Null
$release = 'https://github.com/kubernetes-sigs/kind/releases/download/v0.33.0'
if (!(Test-Path .lab/kind.exe)) {
    Invoke-WebRequest "$release/kind-windows-amd64" -OutFile .lab/kind.exe
}
Invoke-WebRequest "$release/kind-windows-amd64.sha256sum" -OutFile .lab/kind.sha256sum
$expected = ((Get-Content .lab/kind.sha256sum) -split '\s+')[0].ToLowerInvariant()
$actual = (Get-FileHash .lab/kind.exe -Algorithm SHA256).Hash.ToLowerInvariant()
if ($actual -ne $expected) { throw 'Kind checksum mismatch' }
"Official Kind v0.33.0 SHA256 verified: $actual" | Tee-Object evidence/kind-checksum.txt
& .lab/kind.exe version
if ($LASTEXITCODE -ne 0) { throw 'Kind version failed' }
