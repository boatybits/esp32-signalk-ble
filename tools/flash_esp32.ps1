# PowerShell script to flash MicroPython to ESP32
# Usage: .\flash_esp32.ps1 -Port COM3 -Firmware "ESP32_GENERIC-20231005-v1.21.0.bin"

param(
    [Parameter(Mandatory=$true)]
    [string]$Port,
    
    [Parameter(Mandatory=$false)]
    [string]$Firmware = "",
    
    [Parameter(Mandatory=$false)]
    [switch]$EraseOnly
)

Write-Host "ESP32 MicroPython Flasher" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan
Write-Host ""

# Check if esptool is installed
Write-Host "Checking for esptool..." -ForegroundColor Yellow
try {
    $esptoolVersion = python -m esptool version 2>&1
    Write-Host "✓ esptool found" -ForegroundColor Green
} catch {
    Write-Host "✗ esptool not found" -ForegroundColor Red
    Write-Host "Installing esptool..." -ForegroundColor Yellow
    pip install esptool
}

Write-Host ""

# Erase flash
Write-Host "Erasing ESP32 flash..." -ForegroundColor Yellow
python -m esptool --port $Port erase_flash

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Flash erase failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Flash erased successfully" -ForegroundColor Green
Write-Host ""

# If EraseOnly flag is set, stop here
if ($EraseOnly) {
    Write-Host "Erase complete. Exiting." -ForegroundColor Cyan
    exit 0
}

# Flash firmware if provided
if ($Firmware -ne "" -and (Test-Path $Firmware)) {
    Write-Host "Flashing MicroPython firmware..." -ForegroundColor Yellow
    Write-Host "Firmware: $Firmware" -ForegroundColor Gray
    Write-Host ""
    
    python -m esptool --chip esp32 --port $Port write_flash -z 0x1000 $Firmware
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Firmware flash failed!" -ForegroundColor Red
        exit 1
    }
    
    Write-Host ""
    Write-Host "✓ Firmware flashed successfully" -ForegroundColor Green
    Write-Host ""
    Write-Host "ESP32 is ready! You can now upload your Python code." -ForegroundColor Cyan
    
} elseif ($Firmware -eq "") {
    Write-Host "No firmware specified. Flash erased only." -ForegroundColor Yellow
    Write-Host "Download MicroPython firmware from:" -ForegroundColor Cyan
    Write-Host "https://micropython.org/download/ESP32_GENERIC/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Then run:" -ForegroundColor Yellow
    Write-Host ".\flash_esp32.ps1 -Port $Port -Firmware <firmware.bin>" -ForegroundColor White
    
} else {
    Write-Host "✗ Firmware file not found: $Firmware" -ForegroundColor Red
    exit 1
}
