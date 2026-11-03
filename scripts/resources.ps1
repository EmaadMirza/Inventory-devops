$snapshot = [ordered]@{
    Timestamp = (Get-Date -Format o)
    FreeRAM_MB = [math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1024)
    C_Free_GB = [math]::Round((Get-PSDrive C).Free/1GB,2)
    DockerMemoryBytes = (docker info --format '{{.MemTotal}}')
    Containers = @(docker ps -a --format '{{.Names}} | {{.Status}}')
    Memory = @(docker stats --no-stream --format '{{.Name}} | {{.MemUsage}}')
}
$snapshot | ConvertTo-Json -Depth 3 | Tee-Object -Append evidence/resources.txt
