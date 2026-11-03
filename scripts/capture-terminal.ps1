param([ValidateSet('Git','Maven','Docker','Ansible','Kubernetes3','Kubernetes5','KubernetesFinal')][string]$Stage)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
Start-Transcript -Path ".lab/capture-$Stage.txt" | Out-Null
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
        Write-Host '> docker compose --profile build run --rm maven'
        docker compose --profile build run --rm maven
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
        Write-Host '> kubectl --kubeconfig .lab/kubeconfig --context kind-inventory-lab get deployment,pods,service'
        kubectl --kubeconfig .lab/kubeconfig --context kind-inventory-lab get 'deployment,pods,service'
        Write-Host '> kubectl --context kind-inventory-lab get endpointslices'
        kubectl --kubeconfig .lab/kubeconfig --context kind-inventory-lab get endpointslices
    }
}
Write-Host "Live terminal execution completed at $(Get-Date -Format HH:mm:ss)" -ForegroundColor Green
Start-Sleep -Seconds 2
Add-Type -AssemblyName System.Drawing
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class InventoryConsoleCapture {
    [StructLayout(LayoutKind.Sequential)] public struct Rect { public int Left, Top, Right, Bottom; }
    [DllImport("kernel32.dll")] public static extern IntPtr GetConsoleWindow();
    [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr window, out Rect rect);
    [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr window, IntPtr dc, uint flags);
}
'@
$window = [InventoryConsoleCapture]::GetConsoleWindow()
$rectangle = New-Object InventoryConsoleCapture+Rect
if (![InventoryConsoleCapture]::GetWindowRect($window,[ref]$rectangle)) { throw 'Console bounds unavailable' }
$bitmap = New-Object System.Drawing.Bitmap ($rectangle.Right-$rectangle.Left),($rectangle.Bottom-$rectangle.Top)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$dc = $graphics.GetHdc()
try {
    if (![InventoryConsoleCapture]::PrintWindow($window,$dc,2)) { throw 'Console screenshot capture failed' }
} finally { $graphics.ReleaseHdc($dc) }
$bitmap.Save((Join-Path (Get-Location) "evidence/terminal-$Stage.png"),[System.Drawing.Imaging.ImageFormat]::Png)
$graphics.Dispose()
$bitmap.Dispose()
Stop-Transcript | Out-Null
Start-Sleep -Seconds 3
