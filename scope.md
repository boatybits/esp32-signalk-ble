# ESP32 to SignalK BLE Bridge - Project Scope

## Project Overview

**Goal:** Create a wireless sensor data bridge from ESP32 microcontroller to SignalK server using Bluetooth Low Energy (BLE).

**Hardware:**
- ESP32 microcontroller running MicroPython
- Raspberry Pi 5 (network: 10.42.0.1, open network)
- Various sensors (temperature, pressure, humidity, etc.)

**Software:**
- MicroPython firmware on ESP32
- SignalK Bluetooth Sensors Plugin: [bt-sensors-plugin-sk](https://github.com/naugehyde/bt-sensors-plugin-sk)
- SignalK server on Raspberry Pi

---

## Core Requirements

### Functional Requirements
1. **BLE Communication**
   - ESP32 advertises as BLE GATT server
   - Raspberry Pi connects as BLE client
   - Reliable data transmission via BLE characteristics

2. **Sensor Data Collection**
   - Read data from various sensors (I2C, SPI, analog)
   - Format data appropriately for transmission
   - Handle sensor errors gracefully

3. **SignalK Integration**
   - Data received by bt-sensors-plugin-sk on Raspberry Pi
   - Automatic conversion to SignalK delta format
   - Proper SignalK path mapping (e.g., environment.inside.temperature)

4. **Configuration**
   - Easy configuration of sensor types and parameters
   - BLE service and characteristic UUIDs configurable
   - Update intervals adjustable

### Non-Functional Requirements
1. **Reliability**
   - Automatic reconnection on connection loss
   - Error handling and recovery
   - Graceful degradation

2. **Performance**
   - Data update rate: 1-10 Hz (configurable)
   - BLE connection establishment: < 5 seconds
   - Low latency: < 100ms for data updates

3. **Power Efficiency**
   - Optimized for battery operation
   - Deep sleep between readings (optional)
   - Target: > 24 hours on battery

4. **Maintainability**
   - Clean, documented code
   - Modular architecture
   - Easy to extend with new sensors

---

## Project Roadmap

### Phase 1: Foundation & BLE Setup ⏳
**Timeline:** Week 1-2  
**Status:** Not Started

**Objectives:**
- [ ] Set up ESP32 development environment
- [ ] Install MicroPython on ESP32
- [ ] Research bt-sensors-plugin-sk requirements
- [ ] Understand required BLE GATT structure

**Deliverables:**
- Working MicroPython installation
- Documentation of BLE protocol requirements
- Basic BLE advertising test

---

### Phase 2: BLE GATT Server Implementation ⏳
**Timeline:** Week 2-3  
**Status:** Not Started

**Objectives:**
- [ ] Implement BLE GATT server on ESP32
- [ ] Create service and characteristic definitions
- [ ] Handle connection/disconnection events
- [ ] Test BLE advertising and connection

**Deliverables:**
- Functional BLE GATT server
- BLE scanner can detect and connect to ESP32
- Basic characteristic read/write/notify working

**Technical Tasks:**
```python
# Key components to implement:
- BLE initialization and advertising
- GATT service definition
- Characteristic handlers (read, write, notify)
- Connection state management
```

---

### Phase 3: Sensor Integration 🔧
**Timeline:** Week 3-4  
**Status:** Not Started

**Objectives:**
- [ ] Implement sensor reading functions
- [ ] Format sensor data for BLE transmission
- [ ] Handle multiple sensor types
- [ ] Error handling for sensor failures

**Deliverables:**
- Working sensor data acquisition
- Data formatting and validation
- Mock sensor option for testing

**Supported Sensors (Initial):**
- Temperature sensors (DS18B20, BME280)
- Pressure sensors (BME280, BMP280)
- Humidity sensors (BME280, DHT22)
- Analog sensors (voltage, current)

---

### Phase 4: Raspberry Pi & SignalK Setup 🖥️
**Timeline:** Week 4-5  
**Status:** Not Started

**Objectives:**
- [ ] Install bt-sensors-plugin-sk on Raspberry Pi
- [ ] Configure SignalK server
- [ ] Set up BLE scanning and connection
- [ ] Test data reception from ESP32

**Deliverables:**
- Working SignalK installation
- Plugin configured and receiving BLE data
- Data visible in SignalK dashboard

**Configuration Steps:**
1. Install SignalK on Raspberry Pi
2. Install bt-sensors-plugin-sk plugin
3. Configure plugin settings (BLE UUIDs, device filters)
4. Map BLE characteristics to SignalK paths

---

### Phase 5: End-to-End Integration 🔗
**Timeline:** Week 5-6  
**Status:** Not Started

**Objectives:**
- [ ] Connect all components
- [ ] Verify complete data flow: ESP32 → Pi → SignalK
- [ ] Test with real sensors
- [ ] Optimize performance and reliability

**Deliverables:**
- Working end-to-end system
- Stable BLE connection
- Real sensor data in SignalK

**Testing Checklist:**
- [ ] BLE connection stability
- [ ] Data accuracy
- [ ] Update rate consistency
- [ ] Reconnection after interruption
- [ ] Multiple sensor support

---

### Phase 6: Optimization & Polish ✨
**Timeline:** Week 6-7  
**Status:** Not Started

**Objectives:**
- [ ] Power optimization (deep sleep, duty cycling)
- [ ] Error recovery improvements
- [ ] Configuration management (JSON config file)
- [ ] OTA update capability (optional)

**Deliverables:**
- Optimized power consumption
- Robust error handling
- Easy configuration mechanism

**Optimization Targets:**
- Battery life: > 24 hours with 1Hz updates
- Range: 10-30 meters
- CPU usage: < 10% average

---

### Phase 7: Documentation & Examples 📚
**Timeline:** Week 7-8  
**Status:** Not Started

**Objectives:**
- [ ] Complete README with setup instructions
- [ ] Code documentation and comments
- [ ] Troubleshooting guide
- [ ] Example configurations for common sensors

**Deliverables:**
- Comprehensive documentation
- Quick start guide
- Example projects
- Video tutorial (optional)

**Documentation Structure:**
- `/docs/setup_guide.md` - Step-by-step setup
- `/docs/troubleshooting.md` - Common issues
- `/docs/ble_protocol.md` - Technical protocol details
- `/docs/examples/` - Example configurations

---

## Success Criteria

### Minimum Viable Product (MVP)
- [ ] ESP32 successfully transmits sensor data via BLE
- [ ] Raspberry Pi receives data via bt-sensors-plugin-sk
- [ ] Data visible in SignalK server
- [ ] At least one sensor type fully supported
- [ ] Basic documentation available

### Full Release
- [ ] Multiple sensor types supported
- [ ] Battery-powered operation viable (> 24hr)
- [ ] Automatic reconnection works reliably
- [ ] Complete documentation
- [ ] Example projects available
- [ ] Tested on multiple ESP32 variants

---

## Technical Decisions

### Why MicroPython?
✅ **Pros:**
- Rapid development and prototyping
- Interactive REPL for debugging
- Built-in BLE library (`ubluetooth`)
- Easy sensor integration
- Large community and libraries

⚠️ **Cons:**
- Slightly higher power consumption vs C/C++
- Larger firmware size
- May need optimization for battery life

**Decision:** Use MicroPython for initial development, consider C/C++ port if power consumption is critical.

### Why BLE over WiFi?
✅ **Pros:**
- Lower power consumption
- No WiFi credentials needed
- Good range for marine/boat applications
- Native support on ESP32 and Raspberry Pi
- Works in offline environments

⚠️ **Cons:**
- Limited to one-to-one connections (without mesh)
- Shorter range than WiFi
- More complex protocol than HTTP

**Decision:** BLE is the best fit for wireless sensor applications where power and simplicity matter.

---

## Risks & Mitigation

### Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| BLE compatibility issues with bt-sensors-plugin-sk | High | Medium | Study plugin source code early; test frequently |
| BLE connection instability | High | Medium | Implement robust reconnection logic |
| Power consumption too high | Medium | Low | Implement deep sleep; optimize update rates |
| Sensor errors causing crashes | Medium | Medium | Comprehensive error handling |
| Limited BLE range | Low | Low | Use external antenna if needed |

### Project Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| bt-sensors-plugin-sk not maintained | High | Low | Fork plugin if necessary; document protocol |
| SignalK API changes | Medium | Low | Pin SignalK version; monitor releases |
| Hardware availability | Low | Low | Support multiple ESP32 variants |

---

## Resources & References

### Documentation
- [bt-sensors-plugin-sk](https://github.com/naugehyde/bt-sensors-plugin-sk) - SignalK BLE plugin
- [MicroPython BLE Documentation](https://docs.micropython.org/en/latest/library/bluetooth.html)
- [SignalK Documentation](https://signalk.org/)
- [BLE GATT Specification](https://www.bluetooth.com/specifications/gatt/)

### Tools
- [nRF Connect](https://www.nordicsemi.com/Products/Development-tools/nrf-connect-for-mobile) - BLE debugging app
- [Thonny](https://thonny.org/) - MicroPython IDE
- [esptool](https://github.com/espressif/esptool) - ESP32 flashing tool

### Related Projects
- Look for existing BLE sensor implementations
- SignalK community examples
- MicroPython BLE examples

---

## Project Files

📁 **Documentation:**
- `architecture.md` - Technical architecture and system design
- `social_media_overview.md` - Project summary for sharing
- `development_diary.md` - Development log and decisions
- `scope.md` - This file

📁 **Code:**
- `esp32/` - ESP32 MicroPython implementation
- `tests/` - Testing utilities
- `tools/` - Development scripts
- `docs/` - Additional technical documentation

---

## Next Immediate Steps

1. **Research** bt-sensors-plugin-sk source code to understand exact BLE requirements
2. **Set up** ESP32 development environment with MicroPython
3. **Create** basic BLE GATT server example
4. **Test** BLE advertising and connection with nRF Connect app
5. **Begin** Phase 2 implementation

---

**Project Start Date:** December 5, 2025  
**Target Completion:** February 2026 (8 weeks)  
**Current Phase:** Phase 4-5 - Raspberry Pi Integration & End-to-End Testing  
**Last Updated:** December 6, 2025

**Status:** ✅ ESP32 firmware complete | ✅ Advertisement protocol working | 🧪 SignalK integration testing

