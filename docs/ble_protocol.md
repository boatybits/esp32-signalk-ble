# BLE Protocol Specification for SignalK Integration

## Overview
The bt-sensors-plugin-sk listens for Bluetooth Low Energy (BLE) advertisements and can connect to GATT servers to receive sensor data and forward it to SignalK.

Based on research of the [bt-sensors-plugin-sk repository](https://github.com/naugehyde/bt-sensors-plugin-sk), this document outlines the BLE protocol requirements for compatibility.

---

## Two Data Transmission Methods

### Method 1: Advertisement Protocol (Recommended for Low Power)
**Description:** Sensor data is embedded in BLE advertisement packets. No connection required.

**Advantages:**
- Very low power consumption
- No connection management needed
- Can support many sensors simultaneously
- Battery-friendly (years of operation)

**Disadvantages:**
- Limited data payload (~27 bytes)
- One-way communication only
- Less secure (unencrypted by default)

**Examples:** Xiaomi sensors, Ruuvi tags, SwitchBot sensors

### Method 2: GATT Connection (More Data, More Power)
**Description:** Establishes a full BLE GATT connection to read/notify characteristics.

**Advantages:**
- More data can be transmitted
- Bidirectional communication
- Can be encrypted
- Request-response patterns

**Disadvantages:**
- Higher power consumption
- Limited to ~7 simultaneous connections
- Connection management complexity
- Battery drains faster

**Examples:** Victron devices (newer ones use encrypted ads), Renogy batteries, JBD BMS

---

## Standard BLE GATT Service for Environmental Sensing

For our ESP32 implementation, we'll use **Standard BLE GATT Services** which are widely supported.

### Environmental Sensing Service (ESS)
**Service UUID:** `0x181A` (16-bit) or `00001800-0000-1000-8000-00805f9b34fb` (128-bit)

This is a standard Bluetooth SIG service for environmental sensors.

### Standard Characteristics

| Characteristic | UUID (16-bit) | UUID (128-bit) | Data Type | Description |
|----------------|---------------|----------------|-----------|-------------|
| **Temperature** | `0x2A6E` | `00002a6e-0000-1000-8000-00805f9b34fb` | sint16 | Temperature in 0.01°C units |
| **Humidity** | `0x2A6F` | `00002a6f-0000-1000-8000-00805f9b34fb` | uint16 | Humidity in 0.01% units |
| **Pressure** | `0x2A6D` | `00002a6d-0000-1000-8000-00805f9b34fb` | uint32 | Pressure in 0.1 Pa units |

### Data Formats

#### Temperature (0x2A6E)
- **Format:** Signed 16-bit integer (little-endian)
- **Unit:** 0.01 degrees Celsius
- **Example:** 
  - 22.5°C → `2250` → `0xD2 0x08`
  - -5.0°C → `-500` → `0x0C 0xFE`

```python
# Encoding
temp_celsius = 22.5
temp_int = int(temp_celsius * 100)  # 2250
data = struct.pack('<h', temp_int)  # b'\xd2\x08'

# Decoding
temp_int = struct.unpack('<h', data)[0]
temp_celsius = temp_int / 100.0
```

#### Humidity (0x2A6F)
- **Format:** Unsigned 16-bit integer (little-endian)
- **Unit:** 0.01 percent
- **Range:** 0-10000 (0-100%)
- **Example:** 
  - 55.5% → `5550` → `0xAE 0x15`

```python
# Encoding
humidity_percent = 55.5
humidity_int = int(humidity_percent * 100)  # 5550
data = struct.pack('<H', humidity_int)  # b'\xae\x15'

# Decoding
humidity_int = struct.unpack('<H', data)[0]
humidity_percent = humidity_int / 100.0
```

#### Pressure (0x2A6D)
- **Format:** Unsigned 32-bit integer (little-endian)
- **Unit:** 0.1 Pascal
- **Example:** 
  - 101325 Pa (1 atm) → `1013250` → `0xF2 0x75 0x0F 0x00`
  - 1013.25 hPa → 101325 Pa → `1013250`

```python
# Encoding
pressure_hpa = 1013.25  # hPa
pressure_pa = pressure_hpa * 100  # Convert to Pa
pressure_int = int(pressure_pa * 10)  # 1013250
data = struct.pack('<I', pressure_int)  # b'\xf2\x75\x0f\x00'

# Decoding
pressure_int = struct.unpack('<I', data)[0]
pressure_pa = pressure_int / 10.0
pressure_hpa = pressure_pa / 100.0
```

---

## Characteristic Properties

Each characteristic should support:

1. **Read** - Central can read current value
2. **Notify** - Peripheral can push updates to central
3. **Indicate** - Similar to notify, but with acknowledgment (optional)

### Recommended: Read + Notify

```python
# Flags for characteristic properties
_FLAG_READ = 0x0002
_FLAG_NOTIFY = 0x0010

# Define characteristic
(TEMP_UUID, _FLAG_READ | _FLAG_NOTIFY)
```

---

## BLE Advertisement Structure

When advertising, include:

### Required Advertisement Data
1. **Flags** (0x01)
   - General discoverable mode
   - BR/EDR not supported

2. **Complete Local Name** (0x09)
   - Example: "ESP32-SignalK"

3. **Complete List of 16-bit Service UUIDs** (0x03)
   - Include: `0x181A` (Environmental Sensing)

### Example Advertisement Payload
```python
adv_data = bytearray()

# Flags
adv_data.extend([0x02, 0x01, 0x06])  # Length=2, Type=Flags, Data=0x06

# Complete Name
name = b"ESP32-SignalK"
adv_data.extend([len(name)+1, 0x09])
adv_data.extend(name)

# 16-bit Service UUID
adv_data.extend([0x03, 0x03, 0x1A, 0x18])  # Length=3, Type=UUID16, UUID=0x181A
```

---

## bt-sensors-plugin-sk Integration

### How the Plugin Works

1. **Device Discovery**
   - Plugin scans for BLE devices
   - Devices appear in configuration UI
   - User selects device and assigns "Sensor Class"

2. **Sensor Class Selection**
   - For unknown devices, manually select sensor class
   - Plugin looks for specific service/characteristic UUIDs
   - Maps characteristic values to SignalK paths

3. **Data Flow**
   - Plugin reads BLE characteristics (via GATT)
   - Converts to SignalK delta format
   - Publishes to SignalK server

### What We Need to Do

**For our ESP32 to be compatible:**

1. ✅ Advertise with recognizable name
2. ✅ Implement standard Environmental Sensing Service (0x181A)
3. ✅ Use standard characteristic UUIDs (0x2A6E, 0x2A6F, 0x2A6D)
4. ✅ Format data according to BLE specifications
5. ⚠️ May need to create a custom sensor class in the plugin (advanced)

---

## Custom Sensor Class (Optional Future Enhancement)

If standard characteristics don't meet needs, we can create a custom sensor class:

### Location
`bt-sensors-plugin-sk/sensor_classes/`

### Basic Structure
```javascript
// ESP32SignalK.js
class ESP32SignalK extends BTSensor {
  static matchProfile(profile) {
    return profile.name && profile.name.includes('ESP32-SignalK');
  }
  
  initSchema() {
    return {
      temperature: 'environment.inside.temperature',
      humidity: 'environment.inside.humidity',
      pressure: 'environment.outside.pressure'
    };
  }
  
  async getData() {
    // Read GATT characteristics
    const temp = await this.readCharacteristic('2A6E');
    const humidity = await this.readCharacteristic('2A6F');
    const pressure = await this.readCharacteristic('2A6D');
    
    return {
      temperature: this.parseTemperature(temp),
      humidity: this.parseHumidity(humidity),
      pressure: this.parsePressure(pressure)
    };
  }
}
```

**For now:** Use standard UUIDs and the plugin will auto-detect or allow manual sensor class assignment.

---

## Testing & Debugging

### Tools for BLE Development

1. **nRF Connect** (Mobile App)
   - Scan for BLE devices
   - Connect and inspect services
   - Read/write characteristics
   - Best debugging tool for BLE

2. **bluetoothctl** (Linux Command Line)
   ```bash
   sudo bluetoothctl
   scan on
   devices
   connect [MAC_ADDRESS]
   ```

3. **hcitool** (Linux)
   ```bash
   sudo hcitool lescan
   sudo hcitool lecc [MAC_ADDRESS]
   ```

### Verification Steps

1. **Advertisement Check**
   - Use nRF Connect to scan
   - Verify device name appears
   - Check advertised services

2. **GATT Service Check**
   - Connect with nRF Connect
   - Browse services
   - Verify UUID `0x181A` present
   - Verify characteristics present

3. **Data Validation**
   - Read each characteristic
   - Verify data format
   - Check value ranges

4. **SignalK Plugin Integration**
   - Device appears in plugin UI
   - Can select/configure device
   - Data flows to SignalK paths
   - Values update in real-time

---

## Connection Parameters

### Recommended Settings

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Advertising Interval** | 100-1000 ms | Balance between responsiveness and power |
| **Connection Interval** | 50-100 ms | Faster = more battery drain |
| **MTU** | 23 bytes (default) | Can negotiate larger if needed |
| **TX Power** | 0 dBm (default) | Increase for longer range |

---

## SignalK Path Mapping

The plugin will map sensor data to SignalK paths:

### Temperature
```
environment.inside.temperature
environment.outside.temperature
environment.inside.refrigerator.temperature
```

### Humidity
```
environment.inside.humidity
environment.outside.humidity
```

### Pressure
```
environment.outside.pressure
```

### Configuration in Plugin
User can customize paths in the plugin configuration UI to match their boat's schema.

---

## Summary

**Our Implementation Strategy:**
1. ✅ Use standard BLE Environmental Sensing Service (0x181A)
2. ✅ Use standard characteristics (Temperature, Humidity, Pressure)
3. ✅ Follow BLE data format specifications
4. ✅ Advertise properly with device name and service UUID
5. ⚠️ Test with bt-sensors-plugin-sk
6. 📝 Document any custom sensor class if needed

**Next Steps:**
1. Flash MicroPython to ESP32
2. Upload our code
3. Test with nRF Connect app
4. Configure bt-sensors-plugin-sk on Raspberry Pi
5. Verify data flow to SignalK

---

## References

- [BLE GATT Services](https://www.bluetooth.com/specifications/gatt/services/)
- [Environmental Sensing Service](https://www.bluetooth.com/specifications/specs/environmental-sensing-service-1-0/)
- [bt-sensors-plugin-sk](https://github.com/naugehyde/bt-sensors-plugin-sk)
- [SignalK Specification](https://signalk.org/specification/latest/)
- [MicroPython BLE Documentation](https://docs.micropython.org/en/latest/library/bluetooth.html)

---

**Last Updated:** December 5, 2025  
**Status:** Phase 4 - Advertisement Protocol Implemented & Tested  
**Implementation:** Using Method 1 (Advertisement Protocol) with manufacturer-specific data (Company ID 0xFFFF)  
**Last Updated:** December 6, 2025
