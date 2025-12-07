# ESP32 Flashing Troubleshooting

## "Failed to connect to Espressif device: No serial data received"

This usually means the ESP32 is not in bootloader mode.

### Solution: Manual Boot Mode

1. **Hold down the BOOT button** on your ESP32
2. **While holding BOOT, press and release the RESET button**
3. **Release the BOOT button**
4. **Run the flash command immediately**

### ESP32 Board Buttons
- **BOOT** button: Usually labeled "BOOT", "IO0", or "FLASH"
- **RESET** button: Usually labeled "RESET", "RST", or "EN"

### Alternative: Try Different Baud Rate

Some ESP32 boards work better with lower baud rates:
```powershell
# Try with slower baud rate
python -m esptool --port COM6 --baud 115200 erase_flash
```

### Check USB Connection
1. Try a different USB cable (data cable, not charge-only)
2. Try a different USB port
3. Check Device Manager for COM port status

### Driver Issues
If COM6 doesn't work:
- Install CH340/CP2102 USB drivers
- Check Device Manager → Ports (COM & LPT)
- Verify ESP32 shows up as "USB-SERIAL CH340" or "Silicon Labs CP210x"

### Auto-Reset Circuit
Some ESP32 dev boards have auto-reset. If yours doesn't:
- Hold BOOT before running command
- Release after "Connecting...." appears

## Next Steps
After successful connection, you'll see:
```
Connecting....
Chip is ESP32-D0WDQ6 (revision 1)
Features: WiFi, BT, Dual Core, 240MHz, VRef calibration in efuse, Coding Scheme None
Crystal is 40MHz
```
