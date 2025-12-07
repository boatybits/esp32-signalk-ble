# BLE Scanner - Testing Tool

A Python utility to scan for BLE devices and inspect their services/characteristics.
Useful for debugging ESP32 BLE implementation without needing the full SignalK stack.

## Requirements

```bash
pip install bleak
```

## Usage

```bash
python ble_scanner.py
```

## Features

- Scans for nearby BLE devices
- Lists device name, MAC address, and RSSI
- Can connect to devices and list services
- Inspect characteristics and their properties
- Read characteristic values

## Code

```python
"""
BLE Scanner - Testing Tool for ESP32 SignalK Bridge
===================================================
Scans for BLE devices and inspects GATT services/characteristics
"""

import asyncio
from bleak import BleakScanner, BleakClient

async def scan_devices(duration=10):
    """Scan for BLE devices"""
    print(f"Scanning for BLE devices for {duration} seconds...")
    devices = await BleakScanner.discover(timeout=duration)
    
    print(f"\nFound {len(devices)} devices:")
    print("-" * 80)
    
    for device in devices:
        print(f"Name: {device.name or 'Unknown'}")
        print(f"Address: {device.address}")
        print(f"RSSI: {device.rssi} dBm")
        print(f"Metadata: {device.metadata}")
        print("-" * 80)
    
    return devices

async def inspect_device(address):
    """Connect to device and list services/characteristics"""
    print(f"\nConnecting to {address}...")
    
    async with BleakClient(address) as client:
        print(f"Connected: {client.is_connected}")
        
        print("\nServices:")
        for service in client.services:
            print(f"  Service: {service.uuid}")
            print(f"    Description: {service.description}")
            
            for char in service.characteristics:
                print(f"    Characteristic: {char.uuid}")
                print(f"      Properties: {char.properties}")
                
                # Try to read if readable
                if "read" in char.properties:
                    try:
                        value = await client.read_gatt_char(char.uuid)
                        print(f"      Value: {value.hex()}")
                    except Exception as e:
                        print(f"      Could not read: {e}")

async def main():
    """Main function"""
    # Scan for devices
    devices = await scan_devices(10)
    
    # Look for ESP32-SignalK device
    esp32_device = None
    for device in devices:
        if device.name and "ESP32" in device.name:
            esp32_device = device
            break
    
    if esp32_device:
        print(f"\n\nFound ESP32 device: {esp32_device.name}")
        choice = input("Inspect this device? (y/n): ")
        if choice.lower() == 'y':
            await inspect_device(esp32_device.address)
    else:
        print("\n\nNo ESP32-SignalK device found")
        print("Available devices:")
        for i, device in enumerate(devices):
            print(f"{i}: {device.name or 'Unknown'} ({device.address})")
        
        choice = input("\nEnter device number to inspect (or 'q' to quit): ")
        if choice != 'q':
            try:
                idx = int(choice)
                await inspect_device(devices[idx].address)
            except (ValueError, IndexError):
                print("Invalid selection")

if __name__ == "__main__":
    asyncio.run(main())
```

## Example Output

```
Scanning for BLE devices for 10 seconds...

Found 3 devices:
--------------------------------------------------------------------------------
Name: ESP32-SignalK
Address: 24:6F:28:XX:XX:XX
RSSI: -45 dBm
Metadata: {}
--------------------------------------------------------------------------------

Connecting to 24:6F:28:XX:XX:XX...
Connected: True

Services:
  Service: 0000181a-0000-1000-8000-00805f9b34fb
    Description: Environmental Sensing
    Characteristic: 00002a6e-0000-1000-8000-00805f9b34fb
      Properties: ['read', 'notify']
      Value: d208
    Characteristic: 00002a6f-0000-1000-8000-00805f9b34fb
      Properties: ['read', 'notify']
      Value: ae15
    Characteristic: 00002a6d-0000-1000-8000-00805f9b34fb
      Properties: ['read', 'notify']
      Value: f2750f00
```
