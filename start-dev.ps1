$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendDir = Join-Path $repoRoot "patrimonio-autopilot"
$frontendDir = Join-Path $repoRoot "dashboard"

if (-not (Test-Path $backendDir)) {
    Write-Error "Backend folder not found: $backendDir"
}

if (-not (Test-Path $frontendDir)) {
    Write-Error "Dashboard folder not found: $frontendDir"
}

Write-Host "Starting backend on http://127.0.0.1:8000 ..."
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "Set-Location '$backendDir'; python -m uvicorn src.api.main:app --reload --port 8000"
)

Write-Host "Starting dashboard (Next.js) ..."
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "Set-Location '$frontendDir'; npm run dev"
)

Write-Host "Done. Two terminals were opened (backend + dashboard)."
