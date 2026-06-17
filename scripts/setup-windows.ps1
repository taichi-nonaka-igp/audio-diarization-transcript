# Windows environment setup for audio-diarization-transcript
# Run from an elevated or normal PowerShell: .\scripts\setup-windows.ps1

$ErrorActionPreference = "Stop"

function Refresh-Path {
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" +
        [System.Environment]::GetEnvironmentVariable("Path", "User")
}

Write-Host "==> Checking winget..."
if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    throw "winget is required. Install App Installer from Microsoft Store."
}

$packages = @(
    @{ Id = "astral-sh.uv"; Name = "uv" },
    @{ Id = "Python.Python.3.11"; Name = "Python 3.11" },
    @{ Id = "BtbN.FFmpeg.GPL.Shared.7.1"; Name = "FFmpeg 7.1 (shared, for torchcodec)" }
)

foreach ($pkg in $packages) {
    $installed = winget list --id $pkg.Id --accept-source-agreements 2>$null |
        Select-String $pkg.Id
    if ($installed) {
        Write-Host "==> $($pkg.Name) already installed"
    }
    else {
        Write-Host "==> Installing $($pkg.Name)..."
        winget install $pkg.Id --accept-package-agreements --accept-source-agreements
    }
}

Refresh-Path

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

Write-Host "==> Installing Python dependencies (uv sync)..."
uv sync

Write-Host ""
Write-Host "Setup complete."
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Accept model terms: https://huggingface.co/pyannote/speaker-diarization-community-1"
Write-Host "  2. Login: uv run huggingface-cli login"
Write-Host "  3. Run: uv run main.py path\to\audio.wav"
Write-Host ""
Write-Host "Note: FFmpeg 7.x shared build is required on Windows (torchcodec does not support FFmpeg 8)."
