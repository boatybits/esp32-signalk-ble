# ESP32 to SignalK BLE Bridge - Project Architecture

## Project Overview
A MicroPython-based solution for ESP32 to transmit sensor data to SignalK via Bluetooth Low Energy (BLE), received by a Raspberry Pi 5 running the SignalK Bluetooth Sensors plugin.

## System Architecture

```
┌─────────────────┐         BLE          ┌─────────────────┐      Network       ┌─────────────────┐
│   ESP32-S3      │ ────────────────►   │  Raspberry Pi 5  │ ◄─────────────────► │   SignalK       │
│  (MicroPython)  │  Advertisements      │  (10.42.0.1)    │    HTTP/WebSocket   │    Server       │
└─────────────────┘  (No connection!)    └─────────────────┘                     └─────────────────┘
        │                                          │
        ▼                                          ▼
   Sensor Data                         BT Sensors Plugin + Custom Sensor Class
   (Temperature,                      (naugehyde/bt-sensors-plugin-sk)
    Pressure, etc.)                         (ESP32SignalK_adv.js)
```

## Component Breakdown

### 1. ESP32 Device Layer
**Location:** `/ble/esp32/`
- **main_adv.py** - Main application loop (advertisement mode)
- **ble_advertiser.py** - BLE advertisement broadcaster
- **sensor_handler.py** - Sensor data acquisition and formatting
- **config.py** - Configuration management
- **main.py** / **ble_server.py** - Legacy GATT implementation (deprecated)

### 2. Data Transport Layer
**Protocol:** Bluetooth Low Energy (BLE) Advertisements
- **Transport:** Advertisement packets (manufacturer-specific data)
- **Format:** Custom 12-byte payload with Company ID 0xFFFF
- **Data:** Temperature (sint16), Humidity (uint16), Pressure (uint32), Battery (uint8)
- **Advantages:** No connection needed, ultra-low power, multi-device support

### 3. Raspberry Pi 5 Receiver
**Network:** 10.42.0.1 (open network)
- **OS:** Raspberry Pi OS / Linux
- **BLE Stack:** BlueZ
- **SignalK Plugin:** [bt-sensors-plugin-sk](https://github.com/naugehyde/bt-sensors-plugin-sk)

### 4. SignalK Integration
- **Custom Sensor Class:** ESP32SignalK_adv.js (parses manufacturer data)
- **Data Format:** SignalK delta messages
- **API:** REST and WebSocket
- **Paths:** Standard SignalK sensor paths (e.g., environment.temperature)
- **Plugin:** bt-sensors-plugin-sk with custom sensor class installed

## File Structure

```
ble/
├── README.md                    # Quick start and setup guide
├── scope.md                     # Project scope and roadmap
├── architecture.md              # This file - technical architecture
├── development_diary.md         # Development history and decisions
├── social_media_overview.md     # Shareable project summary
│
├── esp32/                       # ESP32 MicroPython code
│   ├── main_adv.py              # Entry point (advertisement mode)
│   ├── ble_advertiser.py        # BLE advertisement broadcaster
│   ├── sensor_handler.py        # Sensor data management
│   ├── config.py                # Configuration constants
│   ├── main.py                  # Legacy GATT mode (deprecated)
│   ├── ble_server.py            # Legacy GATT server (deprecated)
│   └── lib/                     # External libraries
│       └── requirements.txt     # MicroPython dependencies
│
├── ESP32SignalK_adv.js          # SignalK custom sensor class
│
├── tests/                       # Testing utilities
│   ├── ble_scanner.py           # BLE scanner/debugger
│   └── mock_server.py           # Testing without hardware
│
├── docs/                        # Additional documentation
│   ├── ble_protocol.md          # BLE protocol specification
│   ├── signalk_mapping.md       # Sensor to SignalK path mapping
│   └── troubleshooting.md       # Common issues and solutions
│
└── tools/                       # Development tools
    ├── flash_esp32.sh           # Flashing script
    └── monitor.py               # Serial monitor utility
```

## Data Flow

1. **Sensor Reading** (ESP32)
   - Sensors provide raw data (I2C, SPI, analog, or mock data)
   - Data normalized and packaged

2. **BLE Advertising** (ESP32)
   - ESP32 broadcasts advertisement packets continuously
   - No connection required - one-way broadcast
   - Data embedded in manufacturer-specific data field

3. **Data Reception** (BLE)
   - Raspberry Pi passively scans for advertisements
   - No connection establishment needed
   - Multiple ESP32 devices can broadcast simultaneously

4. **Plugin Processing** (Raspberry Pi)
   - bt-sensors-plugin-sk receives BLE data
   - Converts to SignalK delta format
   - Publishes to SignalK server

5. **SignalK Distribution**
   - Data available via SignalK API
   - Other applications can subscribe
   - Historical data logging

## Technology Stack

### ESP32 Side
- **Platform:** ESP32-S3 (or similar)
- **Language:** MicroPython
- **BLE Stack:** Built-in ESP32 BLE (using `ubluetooth`)
- **Sensors:** I2C/SPI based sensors (BME280, DS18B20, etc.)

### Raspberry Pi Side
- **OS:** Linux (Raspberry Pi OS)
- **Runtime:** Node.js (for SignalK)
- **BLE:** BlueZ stack
- **Plugin:** bt-sensors-plugin-sk (Node.js)

## Key Technical Decisions

### Why BLE Advertisements?
- **Ultra-low power** consumption - years on battery possible
- Sufficient range for boat/marine applications (10-30m)
- Native support on ESP32 and Raspberry Pi
- No WiFi credentials needed
- **No connection management** - just broadcast and forget
- **Scalable** - one Pi can receive from dozens of sensors
- **Simple** - no pairing, bonding, or connection state

### Why MicroPython?
- Rapid prototyping and development
- Easy sensor integration
- Built-in BLE support
- Interactive REPL for debugging

### SignalK Integration Benefits
- Standard marine data format
- Ecosystem of compatible apps
- Historical data logging
- Multiple client support

## Security Considerations

- **BLE Pairing:** Consider implementing pairing for secure connection
- **Data Validation:** Validate sensor data before transmission
- **Network Security:** SignalK server should be on trusted network
- **Update Mechanism:** OTA updates for ESP32 firmware

## Performance Targets

- **BLE Connection:** < 5 seconds to establish
- **Data Update Rate:** 1-10 Hz (configurable)
- **Battery Life:** > 24 hours (with periodic updates)
- **Range:** 10-30 meters (typical BLE range)

## Future Enhancements

- Multiple sensor support
- OTA firmware updates
- Battery monitoring and reporting
- Configuration via BLE (no code changes)
- Deep sleep between readings
- Support for multiple ESP32 devices
