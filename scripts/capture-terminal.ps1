param([ValidateSet('Git','Maven','Docker','Ansible','Kubernetes3','Kubernetes5','KubernetesFinal')][string]$Stage)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
$Host.UI.RawUI.WindowTitle = "Mini Inventory - $Stage - Emaad Mirza 1ms24cy020"
Clear-Host
Write-Host "Mini Inventory DevOps | Emaad Mirza | 1ms24cy020" -ForegroundColor Cyan
Get-Date -Format 'yyyy-MM-dd HH:mm:ss K'
switch ($Stage) {
    Git {
        Write-Host '> git log --graph --oneline --all -6'
        git log --graph --oneline --all -6
        Write-Host '> git branch -av'
        git branch -av
    }
    Maven {
        Write-Host '> docker compose --profile build run --rm maven mvn -B -ntp verify'
        docker compose --profile build run --rm maven mvn -B -ntp verify
    }
    Docker {
        Write-Host '> docker images mini-inventory'
        docker images mini-inventory
        Write-Host '> python scripts/smoke.py http://127.0.0.1:8083'
        python scripts/smoke.py http://127.0.0.1:8083
    }
    Ansible {
        Write-Host '> docker compose --profile ansible run --rm ansible'
        docker compose --profile ansible run --rm ansible
        Write-Host '> Invoke-RestMethod http://127.0.0.1:8082/health'
        Invoke-RestMethod http://127.0.0.1:8082/health | ConvertTo-Json -Compress
    }
    default {
        Write-Host '> kubectl --context kind-inventory-lab get deployment,pods,service'
        kubectl --context kind-inventory-lab get deployment,pods,service
        Write-Host '> kubectl --context kind-inventory-lab get endpointslices'
        kubectl --context kind-inventory-lab get endpointslices
    }
}
Write-Host "Live terminal execution completed at $(Get-Date -Format HH:mm:ss)" -ForegroundColor Green
Start-Sleep -Seconds 2
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bitmap = New-Object System.Drawing.Bitmap $bounds.Width,$bounds.Height
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($bounds.Location,[System.Drawing.Point]::Empty,$bounds.Size)
$bitmap.Save((Join-Path (Get-Location) "evidence/terminal-$Stage.png"),[System.Drawing.Imaging.ImageFormat]::Png)
$graphics.Dispose()
$bitmap.Dispose()
Start-Sleep -Seconds 3
