# MicroPython Firmware Download

## Latest Stable Version

**ESP32 Generic:**
- Version: 1.24.1 (Latest stable as of Dec 2025)
- Download: https://micropython.org/download/ESP32_GENERIC/

Direct link to latest:
https://micropython.org/resources/firmware/ESP32_GENERIC-20241129-v1.24.1.bin

## Alternative - ESP32-S3 (if using S3 variant):
https://micropython.org/download/ESP32_GENERIC_S3/

## Download Instructions

### Option 1: Manual Download
1. Visit: https://micropython.org/download/ESP32_GENERIC/
2. Download the latest .bin file
3. Save to `ble/` directory

### Option 2: PowerShell Download
```powershell
# Download latest firmware
$url = "https://micropython.org/resources/firmware/ESP32_GENERIC-20241129-v1.24.1.bin"
$output = "ESP32_GENERIC-20241129-v1.24.1.bin"
Invoke-WebRequest -Uri $url -OutFile $output
```

## Verify Your ESP32 Type

If unsure which ESP32 you have:
- Most common: ESP32-WROOM or ESP32-DevKit → Use ESP32_GENERIC
- Newer boards: ESP32-S3 → Use ESP32_GENERIC_S3
- ESP32-C3: Use ESP32_GENERIC_C3

When in doubt, try ESP32_GENERIC first.
