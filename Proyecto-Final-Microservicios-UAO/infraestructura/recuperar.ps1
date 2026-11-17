$ErrorActionPreference = 'Stop'
$api = 'http://localhost:8088/api/v1/reservas'
$filter = 'label=com.docker.swarm.service.name=uao_reservas'
$before = @(docker ps -q --filter $filter)
if ($before.Count -ne 2) { throw 'Espera hasta tener dos replicas en ejecucion.' }
docker stop -t 1 $before[0]
if ($LASTEXITCODE -ne 0) { throw 'No se pudo detener la replica de prueba.' }
$limit = (Get-Date).AddMinutes(2)
do {
    try { $http = (Invoke-WebRequest -UseBasicParsing $api -TimeoutSec 3).StatusCode }
    catch { $http = 'sin respuesta' }
    $now = @(docker ps -q --filter $filter --filter health=healthy)
    Write-Host "$(Get-Date -Format HH:mm:ss) HTTP $http | replicas saludables: $($now.Count)"
    if ($http -eq 200 -and $now.Count -eq 2 -and ($now | Where-Object { $_ -notin $before })) {
        docker service ps uao_reservas
        return
    }
    Start-Sleep 2
} while ((Get-Date) -lt $limit)
throw 'No se verifico la recuperacion en dos minutos. Revisa docker service ps uao_reservas.'
