# PowerShell script to upload code to ESP32 using ampy
# Usage: .\upload_code.ps1 -Port COM3

param(
    [Parameter(Mandatory=$true)]
    [string]$Port
)

Write-Host "ESP32 Code Uploader" -ForegroundColor Cyan
Write-Host "===================" -ForegroundColor Cyan
Write-Host ""

# Check if ampy is installed
Write-Host "Checking for ampy..." -ForegroundColor Yellow
try {
    $ampyVersion = ampy --version 2>&1
    Write-Host "✓ ampy found" -ForegroundColor Green
} catch {
    Write-Host "✗ ampy not found" -ForegroundColor Red
    Write-Host "Installing ampy..." -ForegroundColor Yellow
    pip install adafruit-ampy
}

Write-Host ""

# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$esp32Dir = Join-Path (Split-Path -Parent $scriptDir) "esp32"

if (!(Test-Path $esp32Dir)) {
    Write-Host "✗ ESP32 code directory not found: $esp32Dir" -ForegroundColor Red
    exit 1
}

Write-Host "Uploading files from: $esp32Dir" -ForegroundColor Yellow
Write-Host ""

# List of files to upload
$files = @(
    "config.py",
    "ble_server.py",
    "sensor_handler.py",
    "main.py"
)

foreach ($file in $files) {
    $filePath = Join-Path $esp32Dir $file
    
    if (Test-Path $filePath) {
        Write-Host "Uploading $file..." -ForegroundColor Yellow
        ampy --port $Port put $filePath
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ $file uploaded" -ForegroundColor Green
        } else {
            Write-Host "  ✗ Failed to upload $file" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "  ⚠ File not found: $file" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "✓ All files uploaded successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "To run the code, reset your ESP32 or use:" -ForegroundColor Cyan
Write-Host "ampy --port $Port run main.py" -ForegroundColor White
Write-Host ""
Write-Host "To view serial output:" -ForegroundColor Cyan
Write-Host "python -m serial.tools.miniterm $Port 115200" -ForegroundColor White
