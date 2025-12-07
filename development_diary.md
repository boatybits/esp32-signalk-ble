# Development Diary - ESP32 to SignalK BLE Bridge

## Purpose
This diary tracks development progress, decisions, challenges, and solutions throughout the project lifecycle. It serves as a reference for future development and helps maintain project continuity.

---

## Format
Each entry should include:
- **Date:** When the work was done
- **Status:** Planning / In Progress / Completed / Blocked
- **Work Done:** What was accomplished
- **Decisions Made:** Key technical or design decisions
- **Challenges:** Problems encountered
- **Solutions:** How challenges were resolved
- **Next Steps:** What needs to happen next

---

## Development Log

### Entry 001 - December 5, 2025
**Status:** Planning / Initial Setup

**Work Done:**
- Created initial project scope
- Identified core requirements:
  - ESP32 with MicroPython
  - BLE communication to Raspberry Pi 5 (10.42.0.1)
  - Integration with SignalK via bt-sensors-plugin-sk
- Established project documentation structure

**Decisions Made:**
- **Technology Stack:**
  - MicroPython for ESP32 (ease of development, built-in BLE support)
  - BLE GATT protocol for sensor data transmission
  - SignalK plugin: [naugehyde/bt-sensors-plugin-sk](https://github.com/naugehyde/bt-sensors-plugin-sk)
  - Raspberry Pi 5 as BLE gateway

- **Architecture:**
  - Three-tier architecture: ESP32 → Raspberry Pi → SignalK
  - BLE used for ESP32 to Pi communication (wireless, low power)
  - Network communication for Pi to SignalK (HTTP/WebSocket)

- **Project Structure:**
  - Modular file organization with separate directories for ESP32 code, docs, tests, tools
  - Clear separation of concerns (BLE server, sensor handling, configuration)

**Documentation Created:**
- `architecture.md` - Technical architecture and system design
- `social_media_overview.md` - Public-facing project summary
- `development_diary.md` - This file

**Challenges:**
- None yet - initial planning phase

**Next Steps:**
1. Research bt-sensors-plugin-sk requirements and supported BLE characteristics
2. Set up ESP32 development environment
3. Create basic BLE GATT server on ESP32
4. Test BLE connection between ESP32 and Raspberry Pi
5. Implement sensor data reading and formatting
6. Configure SignalK plugin to receive data
7. End-to-end testing

**Notes:**
- Need to determine specific BLE UUIDs and characteristics required by bt-sensors-plugin-sk
- May need to examine plugin source code for exact protocol requirements
- Open network at 10.42.0.1 simplifies initial setup

---

### Entry 002 - December 5, 2025
**Status:** In Progress

**Work Done:**
- Completed Phase 1 setup and foundation work
- Created complete project directory structure
- Implemented core ESP32 MicroPython code:
  - `config.py` - Comprehensive configuration management
  - `ble_server.py` - Full BLE GATT server implementation
  - `sensor_handler.py` - Sensor reading with mock data support
  - `main.py` - Main orchestration loop
- Created comprehensive documentation:
  - `README.md` - Complete setup guide
  - `docs/ble_protocol.md` - Detailed BLE protocol specification
- Created development tools:
  - `tools/flash_esp32.ps1` - PowerShell script for flashing
  - `tools/upload_code.ps1` - PowerShell script for code upload
- Created testing utilities:
  - `tests/ble_scanner.py` - Python BLE scanner for debugging

**Research Findings:**
- bt-sensors-plugin-sk supports both Advertisement and GATT connection methods
- Plugin has 90+ supported sensor types including many BMS and environmental sensors
- Standard BLE Environmental Sensing Service (0x181A) is well-supported
- Standard characteristics for Temperature (0x2A6E), Humidity (0x2A6F), Pressure (0x2A6D)
- Plugin allows manual sensor class selection for unknown devices
- GATT connections can be problematic on RPi with onboard WiFi (interference)
- Recommendation: Use external USB BT 5.3 adapter for better range/stability

**Decisions Made:**
- **Use Standard BLE GATT Services:** Implement Environmental Sensing Service (0x181A) with standard characteristics
- **Mock Sensor Mode:** Implemented mock sensor data generation for testing without hardware
- **Modular Code Structure:** Separated concerns (config, BLE, sensors, main loop)
- **PowerShell Scripts:** Created Windows-friendly automation scripts
- **LED Status Indicators:** Added optional LED patterns for connection status

**Implementation Details:**
- BLE server implements proper GATT service registration
- Characteristics support both Read and Notify operations
- Data formatting follows BLE specifications exactly:
  - Temperature: sint16 in 0.01°C units
  - Humidity: uint16 in 0.01% units
  - Pressure: uint32 in 0.1 Pa units
- Main loop handles connection state and periodic sensor updates
- Comprehensive error handling and debug output
- Memory management with garbage collection

**Challenges:**
- MicroPython import warnings in VS Code (expected - libraries only available on ESP32)
- Need to test actual BLE connection with bt-sensors-plugin-sk
- Unknown if plugin will auto-detect or require manual sensor class selection

**Solutions:**
- Import warnings are cosmetic - code will work on ESP32
- Created BLE scanner tool for intermediate testing
- Documented manual sensor class selection process

**Next Steps:**
1. Flash MicroPython firmware to ESP32 hardware
2. Upload code to ESP32
3. Test BLE advertising with nRF Connect app
4. Verify GATT services and characteristics
5. Begin Phase 2: Raspberry Pi integration
6. Test connection with bt-sensors-plugin-sk
7. Add real sensor support (BME280 or similar)

**Notes:**
- All Phase 1 objectives completed ahead of schedule
- Code is ready for hardware testing
- Mock sensor mode allows testing without physical sensors
- Documentation is comprehensive and ready for sharing
- Project is well-positioned to move into Phase 2

**Files Created:**
- 📁 `esp32/` - Complete MicroPython implementation (4 files)
- 📄 `README.md` - Full setup instructions
- 📄 `docs/ble_protocol.md` - BLE protocol specification
- 🔧 `tools/flash_esp32.ps1` - Flashing automation
- 🔧 `tools/upload_code.ps1` - Upload automation
- 🧪 `tests/ble_scanner.py` - BLE debugging tool

---

### Entry 003 - December 5, 2025
**Status:** In Progress / Debugging

**Work Done:**
- Successfully flashed MicroPython v1.24.1 to ESP32 (ESP32-D0WDQ6)
- Uploaded all project files to ESP32 (config.py, ble_server.py, sensor_handler.py, main.py)
- ESP32 running and advertising as "ESP32-SignalK"
- Verified with nRF Connect app - Environmental Sensing Service visible
- ESP32 visible in SignalK bt-sensors-plugin with strong RSSI (-36 dB)
- Raspberry Pi can see and scan ESP32 device

**Challenges:**
- bt-sensors-plugin-sk sensor class integration proving difficult
- Multiple attempts to create custom sensor class:
  - First attempt: Complex class-based approach failed
  - Second attempt: Module.exports approach - initialization loop
- Plugin architecture not well documented for custom sensors
- Without sensor class, only RSSI visible (no temperature/humidity/pressure data)
- Plugin initialization gets stuck when custom sensor class has errors

**Attempts Made:**
1. Tried using RuuviTag sensor class - Bad Request (400) error
2. Tried no sensor class - only RSSI visible
3. Created custom ESP32SignalK.js class-based - plugin won't initialize
4. Created simplified module.exports version - still initialization loop

**Technical Issues:**
- bt-sensors-plugin-sk expects specific format/API for sensor classes
- Limited documentation on sensor class development
- Need to study existing sensor classes more carefully
- May need to examine plugin source code directly

**Current Status:**
- ESP32 hardware: ✅ Working perfectly
- BLE advertising: ✅ Working
- GATT characteristics: ✅ Accessible via nRF Connect
- SignalK detection: ✅ Device visible
- Data integration: ❌ Blocked on sensor class

**Next Steps:**
1. Study bt-sensors-plugin-sk sensor class examples more carefully
2. May need simpler approach - possibly modify ESP32 to match existing sensor format
3. Consider alternative: Modify ESP32 to emulate RuuviTag format
4. Or: Find plugin configuration for raw GATT characteristic mapping
5. Last resort: Fork bt-sensors-plugin-sk and modify for our needs

**Notes:**
- Core ESP32 implementation is solid and well-structured
- Problem is purely integration with SignalK plugin
- May be faster to adapt ESP32 output format than fix sensor class
- Consider if Advertisement protocol (like Ruuvi) would be easier than GATT

---

### Entry Template (Copy for new entries)

### Entry XXX - [Date]
**Status:** [Planning / In Progress / Completed / Blocked]

**Work Done:**
- 

**Decisions Made:**
- 

**Challenges:**
- 

**Solutions:**
- 

**Next Steps:**
- 

**Notes:**
- 

---

## Quick Reference

### Important Links
- bt-sensors-plugin-sk: https://github.com/naugehyde/bt-sensors-plugin-sk
- SignalK Documentation: https://signalk.org/
- MicroPython BLE docs: https://docs.micropython.org/en/latest/library/bluetooth.html
- ESP32 MicroPython: https://micropython.org/download/ESP32_GENERIC/

### Key Configuration
- **Raspberry Pi Network:** 10.42.0.1
- **Protocol:** BLE GATT
- **Target Platform:** ESP32 with MicroPython
- **Gateway:** Raspberry Pi 5

### Development Environment
- **IDE:** [TBD - VS Code, Thonny, etc.]
- **Serial Tool:** [TBD]
- **BLE Scanner:** [TBD - nRF Connect, etc.]

---

## Milestone Tracker

- [x] **Milestone 1:** BLE GATT Server Implementation
  - [x] Basic BLE advertising
  - [x] GATT service creation
  - [x] Characteristic definition
  - [x] Connection handling

- [x] **Milestone 2:** Sensor Integration
  - [x] Sensor driver implementation (mock mode)
  - [x] Data formatting
  - [x] Error handling

- [ ] **Milestone 3:** Raspberry Pi Integration
  - [ ] BLE connection from Pi
  - [ ] Plugin configuration
  - [ ] Data reception verification

- [ ] **Milestone 4:** SignalK Integration
  - [ ] Delta message format
  - [ ] SignalK path mapping
  - [ ] WebSocket/REST API verification

- [ ] **Milestone 5:** Testing & Optimization
  - [ ] Connection stability testing
  - [ ] Power consumption optimization
  - [ ] Range testing
  - [ ] Error recovery

- [ ] **Milestone 6:** Documentation & Polish
  - [ ] Setup guide
  - [ ] Troubleshooting guide
  - [ ] Code documentation
  - [ ] Example configurations

---

## Lessons Learned

*This section will be populated as the project progresses*

---

## Resources & References

*Links to helpful resources discovered during development*

---

**Last Updated:** December 5, 2025
