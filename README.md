# ESP32 to SignalK BLE Bridge

Send sensor data from ESP32 to SignalK server via Bluetooth Low Energy.

## 🚀 Quick Start

### Prerequisites

**Hardware:**
- ESP32 board (ESP32-S3, ESP32-WROOM, or similar)
- USB cable for programming
- Raspberry Pi 5 (or any Pi with Bluetooth)
- Sensors (optional for initial testing)

**Software:**
- Python 3.7+ (for flashing tools)
- [esptool](https://github.com/espressif/esptool) for flashing
- SignalK server on Raspberry Pi
- [bt-sensors-plugin-sk](https://github.com/naugehyde/bt-sensors-plugin-sk) plugin

### Step 1: Install MicroPython on ESP32

1. **Download MicroPython firmware:**
   ```powershell
   # Visit https://micropython.org/download/ESP32_GENERIC/
   # Download the latest stable .bin file
   ```

2. **Install esptool:**
   ```powershell
   pip install esptool
   ```

3. **Find your ESP32 COM port:**
   ```powershell
   # Check Device Manager or:
   python -m serial.tools.list_ports
   ```

4. **Erase flash (first time only):**
   ```powershell
   esptool.py --port COM3 erase_flash
   ```

5. **Flash MicroPython:**
   ```powershell
   esptool.py --chip esp32 --port COM3 write_flash -z 0x1000 ESP32_GENERIC-20231005-v1.21.0.bin
   ```

### Step 2: Upload Code to ESP32

1. **Install Thonny IDE (recommended) or use ampy:**
   ```powershell
   pip install adafruit-ampy
   ```

2. **Upload files using ampy:**
   ```powershell
   # Navigate to ble/esp32 directory
   cd pythonScripts/ble/esp32
   
   # Upload config
   ampy --port COM3 put config.py
   
   # Upload BLE advertiser (advertisement mode)
   ampy --port COM3 put ble_advertiser.py
   
   # Upload sensor handler
   ampy --port COM3 put sensor_handler.py
   
   # Upload main (advertisement mode)
   ampy --port COM3 put main_adv.py
   
   # Rename to main.py on device
   ampy --port COM3 rm main.py
   ampy --port COM3 put main_adv.py main.py
   ```

3. **Or use Thonny:**
   - Open Thonny IDE
   - Tools → Options → Interpreter
   - Select "MicroPython (ESP32)"
   - Select correct COM port
   - Open files and click "Save to MicroPython device"

### Step 3: Configure Raspberry Pi

1. **Install SignalK:**
   ```bash
   # On Raspberry Pi
   curl -sS https://signalk.org/install.sh | sudo bash
   ```

2. **Install bt-sensors-plugin-sk:**
   ```bash
   # Via SignalK App Store or:
   cd ~/.signalk
   npm install @naugehyde/bt-sensors-plugin-sk
   ```

3. **Install custom sensor class:**
   ```bash
   # Copy ESP32SignalK_adv.js to plugin sensor classes directory
   cp ESP32SignalK_adv.js ~/.signalk/node_modules/@naugehyde/bt-sensors-plugin-sk/src/sensors/
   ```

4. **Configure the plugin:**
   - Open SignalK web interface (http://10.42.0.1:3000)
   - Go to Server → Plugin Config → BT Sensors
   - Enable the plugin
   - Add ESP32 device and select "ESP32SignalK" sensor class
   - Configure zone (e.g., "inside" for environment.inside.temperature)

### Step 4: Test the Connection

1. **Reset ESP32** - It will start advertising via BLE

2. **Check SignalK logs:**
   ```bash
   tail -f ~/.signalk/logs/signalk.log
   ```

3. **Verify data in SignalK:**
   - Open http://10.42.0.1:3000/@signalk/instrumentpanel
   - Look for your sensor data paths

## 📁 Project Structure

```
ble/
├── README.md                    # This file
├── scope.md                     # Project scope & roadmap
├── architecture.md              # Technical design
├── development_diary.md         # Development history
├── social_media_overview.md     # Project summary
│
├── esp32/                       # ESP32 MicroPython code
│   ├── main.py                  # Entry point
│   ├── config.py                # Configuration
│   ├── ble_server.py            # BLE GATT server
│   ├── sensor_handler.py        # Sensor management
│   └── lib/                     # External libraries
│       └── requirements.txt
│
├── tests/                       # Testing utilities
│   ├── ble_scanner.py           # BLE debugging tool
│   └── mock_server.py           # Testing without hardware
│
├── docs/                        # Documentation
│   ├── setup_guide.md           # Detailed setup
│   ├── ble_protocol.md          # BLE protocol spec
│   ├── troubleshooting.md       # Common issues
│   └── signalk_mapping.md       # Data path mapping
│
└── tools/                       # Development tools
    ├── flash_esp32.ps1          # Flashing script
    └── upload_code.ps1          # Upload helper
```

## 🔧 Development

### Testing BLE Advertising

Use nRF Connect app (iOS/Android) to scan for BLE devices:
1. Install nRF Connect
2. Scan for devices
3. Look for "ESP32-SignalK" or your configured name
4. Connect and inspect services/characteristics

### Serial Monitor

```powershell
# Using Thonny IDE (easiest)
# Or using screen/putty/minicom

# Windows (PowerShell):
python -m serial.tools.miniterm COM3 115200

# View ESP32 output for debugging
```

### Configuration

Edit `esp32/config.py` to customize:
- Device name
- BLE UUIDs
- Sensor types
- Update intervals
- Debug output

## 📚 Documentation

- **[scope.md](scope.md)** - Project goals and roadmap
- **[architecture.md](architecture.md)** - System design
- **[development_diary.md](development_diary.md)** - Dev log
- **[social_media_overview.md](social_media_overview.md)** - Share the project!

## 🐛 Troubleshooting

### ESP32 won't connect
- Check BLE is enabled on Raspberry Pi: `sudo systemctl status bluetooth`
- Verify ESP32 is advertising: Use nRF Connect app
- Check Raspberry Pi can see device: `sudo hcitool lescan`

### No data in SignalK
- Check plugin is enabled in SignalK
- Verify BLE UUIDs match between ESP32 and plugin config
- Check SignalK logs for errors

### ESP32 keeps rebooting
- Check power supply (USB cable quality)
- Look for exceptions in serial output
- Verify sensor connections

See [docs/troubleshooting.md](docs/troubleshooting.md) for more solutions.

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional sensor support
- Power optimization
- Better error handling
- Documentation improvements

## 📝 License

[Your License Here]

## 🔗 Links

- **SignalK Plugin:** https://github.com/naugehyde/bt-sensors-plugin-sk
- **SignalK:** https://signalk.org
- **MicroPython:** https://micropython.org
- **ESP32 Docs:** https://docs.espressif.com/

## 📊 Project Status

**Current Phase:** Phase 1 - Foundation & BLE Setup  
**Last Updated:** December 5, 2025

See [scope.md](scope.md) for detailed roadmap.
