$ErrorActionPreference = 'Stop'
$api = 'http://localhost:8088/api/v1'
$fecha = (Get-Date).AddDays(3).ToString('yyyy-MM-dd')
$uri = "$api/reservas?usuarioId=1&facultadId=1&salaId=1"
$d = Invoke-RestMethod "$api/reservas/disponibilidad?facultadId=1&fecha=$fecha"
$slot = ($d.salas | Where-Object id_sala -eq 1).disponibles | Select-Object -First 1
if (!$slot) { throw 'Sala sin franja disponible para la demo.' }
$body = @{fecha=$fecha;hora_inicio=$slot.hora_inicio;hora_fin=$slot.hora_fin} | ConvertTo-Json
$r = Invoke-RestMethod $uri -Method Post -Body $body -ContentType 'application/json'
Write-Host "Reserva creada: $($r.id_reserva)"
try {
    Invoke-RestMethod $uri -Method Post -Body $body -ContentType 'application/json'
    throw 'La reserva duplicada debio fallar'
} catch {
    if (!$_.Exception.Response -or [int]$_.Exception.Response.StatusCode -ne 409) { throw }
    Write-Host 'Conflicto de horario comprobado: HTTP 409'
}
Invoke-RestMethod "$api/reportes/ocupacion" | ConvertTo-Json -Depth 5
Invoke-RestMethod "$api/reservas/$($r.id_reserva)/cancelar?usuarioId=1" -Method Put
Invoke-RestMethod "$api/auditoria?limit=2" | ConvertTo-Json -Depth 5
