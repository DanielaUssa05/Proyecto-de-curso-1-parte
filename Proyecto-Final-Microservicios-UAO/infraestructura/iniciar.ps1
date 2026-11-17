$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
function Invoke-Docker {
    & docker @args
    if ($LASTEXITCODE -ne 0) { throw "Fallo Docker: $($args[0]). Revisa el mensaje anterior." }
}
function Ensure-Secret($name, $value) {
    if ((Invoke-Docker secret ls --format '{{.Name}}') -notcontains $name) {
        $path = [IO.Path]::GetTempFileName()
        try {
            [IO.File]::WriteAllText($path, $value)
            Invoke-Docker secret create $name $path
        } finally { Remove-Item $path -Force }
    }
}
$state = Invoke-Docker info --format '{{.Swarm.LocalNodeState}}'
if ($state -eq 'inactive') { Invoke-Docker swarm init }
$manager = Invoke-Docker info --format '{{.Swarm.ControlAvailable}}'
if ($manager -ne 'true') { throw 'Ejecutar en el manager de Docker Desktop.' }
$nodes = @(Invoke-Docker node ls -q)
if ($nodes.Count -ne 1) { throw 'Este despliegue usa imagenes locales y requiere un Swarm de un nodo.' }
Invoke-Docker node update --label-add reservas_datos=si $nodes[0]
Ensure-Secret reservas_root ([guid]::NewGuid().ToString('N'))
Ensure-Secret reservas_app ([guid]::NewGuid().ToString('N'))
Ensure-Secret reservas_grafana 'Grafana-Demo-Reservas'
Invoke-Docker build -f ./docker/api.Dockerfile -t uao-reservas-api:estructura1 ..
Invoke-Docker build -f ./docker/web.Dockerfile -t uao-reservas-web:estructura1 ..
Invoke-Docker build -f ./docker/db.Dockerfile -t uao-reservas-db:estructura1 ..
Invoke-Docker stack deploy --resolve-image never -c stack.yml uao
$ready = $false
for ($i=0; $i -lt 120; $i++) {
    try {
        $catalog = Invoke-RestMethod 'http://localhost:8088/api/v1/facultades' -TimeoutSec 3
        $report = Invoke-RestMethod 'http://localhost:8088/api/v1/reportes/ocupacion' -TimeoutSec 5
        if ($catalog.Count -gt 0 -and $report.particiones -eq 2) { $ready = $true; break }
    } catch {}
    Start-Sleep -Seconds 3
}
Invoke-Docker stack services uao
if (!$ready) { throw 'Revisa docker stack ps uao --no-trunc y docker service logs uao_db.' }
Write-Host 'Portal http://localhost:8088 | Prometheus :9091 | Grafana :3001'
