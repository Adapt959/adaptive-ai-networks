# Adaptive AI Command Center - one-command setup (Windows)
# In PowerShell run:
#   irm https://raw.githubusercontent.com/Adapt959/adaptive-ai-networks/main/setup.ps1 | iex
$ErrorActionPreference = "Stop"
Write-Host "=== Adaptive AI Command Center setup ==="

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
  Write-Host "Python was not found."
  Write-Host "Install it from https://www.python.org/downloads/ (tick 'Add python.exe to PATH'), then run this again."
  exit 1
}

$dest = "$HOME\adaptive-ai-command-center"
if (Test-Path $dest) { Write-Host "Removing old copy..."; Remove-Item -Recurse -Force $dest }
Write-Host "Downloading the app..."
$zip = "$env:TEMP\cc.zip"
Invoke-WebRequest -Uri "https://github.com/Adapt959/adaptive-ai-networks/archive/refs/heads/main.zip" -OutFile $zip
$tmp = "$env:TEMP\ccx"
if (Test-Path $tmp) { Remove-Item -Recurse -Force $tmp }
Expand-Archive -Path $zip -DestinationPath $tmp -Force
Move-Item "$tmp\adaptive-ai-networks-main" $dest
Remove-Item $zip
Remove-Item -Recurse -Force $tmp
Set-Location $dest

Write-Host "Installing dependencies (a minute or two)..."
python -m venv .venv
& ".\.venv\Scripts\pip.exe" install -q -r requirements.txt

try { Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/version" -TimeoutSec 5 | Out-Null }
catch {
  Write-Host "Starting Ollama in the background..."
  Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
  Start-Sleep 3
}
if (-not (ollama list 2>$null | Select-String "llama3.1")) {
  Write-Host "Downloading the llama3.1 model (a few minutes, one time only)..."
  ollama pull llama3.1
}

Write-Host ""
Write-Host "Starting the server. Open http://127.0.0.1:8001/docs in your browser to use it."
Write-Host "Keep this window open. Press Ctrl+C to stop the server."
& ".\.venv\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8001
