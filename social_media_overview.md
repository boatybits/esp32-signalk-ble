# 🚢 ESP32 to SignalK via BLE - Social Media Overview

## Project Summary

**Transform your ESP32 into a wireless marine sensor hub!** Send sensor data directly to SignalK using Bluetooth Low Energy - no WiFi needed.

---

## 🎯 What Does It Do?

This project enables an **ESP32 microcontroller** running **MicroPython** to transmit sensor data (temperature, pressure, humidity, etc.) to a **SignalK server** via **Bluetooth Low Energy (BLE)**.

Perfect for:
- ⛵ Marine sensor networks on boats
- 🔋 Battery-powered remote sensors
- 🌡️ Environmental monitoring
- 📊 Real-time data visualization in SignalK

---

## 🏗️ System Architecture

```
ESP32 (MicroPython) 
    ↓ BLE
Raspberry Pi 5 (BT Sensors Plugin)
    ↓ Network
SignalK Server
    ↓ WebSocket/HTTP
Your Apps & Displays
```

---

## ✨ Key Features

- **📡 Wireless:** BLE advertisements - no cables, no WiFi, no connection needed!
- **🔋 Ultra Low Power:** Advertisement-only protocol for maximum battery life
- **🐍 MicroPython:** Easy to code and modify
- **🌊 SignalK Native:** Direct integration with marine data standard
- **📱 Multi-Device:** One Raspberry Pi can handle dozens of ESP32 sensors simultaneously
- **🔓 Open Source:** Based on [bt-sensors-plugin-sk](https://github.com/naugehyde/bt-sensors-plugin-sk)
- **✅ Tested & Working:** Hardware validated with real ESP32 devices

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Microcontroller** | ESP32-S3 |
| **Language** | MicroPython |
| **Protocol** | Bluetooth Low Energy (BLE/GATT) |
| **Gateway** | Raspberry Pi 5 |
| **Server** | SignalK |
| **Plugin** | bt-sensors-plugin-sk |

---

## 🚀 Quick Overview

1. **ESP32** reads sensor data (I2C/SPI sensors)
2. **BLE Advertisements** broadcast data via Bluetooth (no connection needed!)
3. **Raspberry Pi** receives BLE data using BlueZ
4. **SignalK Plugin** converts BLE to SignalK format with custom sensor class
5. **SignalK Server** distributes data to all clients

---

## 📊 Use Cases

### Marine Applications
- Engine room temperature monitoring
- Battery voltage tracking
- Bilge water level sensors
- Environmental sensors (temp, humidity, pressure)

### General IoT
- Home automation sensors
- Weather stations
- Greenhouse monitoring
- Remote sensor networks

---

## 🎓 What You'll Learn

- MicroPython BLE programming
- GATT server/client architecture
- SignalK data format and integration
- ESP32 sensor interfacing
- Raspberry Pi IoT gateway setup

---

## 📦 Project Structure

```
ble/
├── esp32/              # MicroPython code for ESP32
├── docs/               # Technical documentation
├── tests/              # Testing utilities
└── tools/              # Development scripts
```

---

## 🔗 Links & Resources

- **Repository:** [Your GitHub Repo]
- **SignalK Plugin:** [naugehyde/bt-sensors-plugin-sk](https://github.com/naugehyde/bt-sensors-plugin-sk)
- **SignalK:** [signalk.org](https://signalk.org)
- **MicroPython:** [micropython.org](https://micropython.org)

---

## 🤝 Contributing

Contributions welcome! This project is perfect for:
- Adding new sensor support
- Improving power efficiency
- Enhancing documentation
- Creating examples

---

## 📝 License

[Your License Here]

---

## 🏷️ Tags

`#ESP32` `#MicroPython` `#BLE` `#Bluetooth` `#SignalK` `#Marine` `#IoT` `#RaspberryPi` `#Sensors` `#OpenSource` `#Python` `#Maker` `#BoatElectronics` `#SmartBoat`

---

## 📸 Visual Summary (Placeholder for Images)

**Add images here:**
- System diagram
- ESP32 with sensors
- SignalK dashboard screenshot
- Mobile app showing data
- Hardware setup photo

---

## 💬 Short Descriptions for Different Platforms

### Twitter/X (280 chars)
🚢 New project: ESP32 → SignalK via BLE! Send sensor data from MicroPython to SignalK server using Bluetooth. Perfect for marine sensors & IoT. No WiFi needed! 📡🔋 #ESP32 #SignalK #MicroPython #IoT

### LinkedIn (Brief)
Excited to share my latest marine IoT project: ESP32 to SignalK Bridge via BLE. This solution enables wireless sensor networks for boats using MicroPython, Bluetooth Low Energy, and SignalK. Perfect for battery-powered remote sensing applications.

### Reddit (r/esp32, r/micropython)
I built a BLE bridge to send ESP32 sensor data to SignalK! Using MicroPython and a Raspberry Pi gateway, this setup is perfect for wireless marine sensors. Check out the architecture and let me know what you think!

### YouTube Description
Learn how to connect ESP32 sensors to SignalK using Bluetooth Low Energy! This tutorial covers MicroPython BLE programming, Raspberry Pi gateway setup, and SignalK integration. Perfect for marine applications and IoT projects.

---

## 📊 Project Status

**Current Phase:** Phase 4-5 - Raspberry Pi Integration & End-to-End Testing  
**Status:** ✅ ESP32 firmware working | ✅ SignalK sensor class created | 🧪 Testing in progress  
**Last Updated:** December 6, 2025

### Recent Achievements:
- ✅ ESP32 MicroPython firmware complete and tested
- ✅ BLE advertisement protocol implemented (no GATT connection needed)
- ✅ Custom SignalK sensor class (`ESP32SignalK_adv.js`) created
- ✅ Manufacturer data format designed and validated
- 🧪 Currently testing end-to-end data flow to SignalK

See [scope.md](scope.md) for detailed roadmap and [development_diary.md](development_diary.md) for progress updates.

---

**Difficulty:** 🟡 Intermediate  
**Time to Build:** 2-4 hours  
**Cost:** ~$20-40 (ESP32 + sensors)
