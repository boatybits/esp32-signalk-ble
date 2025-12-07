"""
ESP32 BLE Advertisement Server - Simplified Version
====================================================
Broadcasts sensor data in BLE advertisements (no connection needed).
Uses a simple custom format that's easy to parse.
"""

import bluetooth
import struct
import time
from micropython import const

# Import configuration
import config

# BLE Event Constants
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)

# BLE Advertising Constants
_ADV_TYPE_FLAGS = const(0x01)
_ADV_TYPE_NAME = const(0x09)
_ADV_TYPE_MANUFACTURER = const(0xFF)

class BLEAdvertiser:
    """Simple BLE Advertiser for sensor data"""
    
    def __init__(self):
        self.ble = bluetooth.BLE()
        self.ble.active(True)
        self.ble.irq(self._irq_handler)
        
        if config.DEBUG_BLE:
            print("[BLE] Advertiser initialized")
    
    def _irq_handler(self, event, data):
        """Handle BLE events"""
        if event == _IRQ_CENTRAL_CONNECT:
            if config.DEBUG_BLE:
                print("[BLE] Device tried to connect (not accepting connections)")
        elif event == _IRQ_CENTRAL_DISCONNECT:
            # Resume advertising after disconnect
            pass
    
    def advertise_sensor_data(self, temperature=None, humidity=None, pressure=None):
        """
        Advertise sensor data in manufacturer-specific data format
        
        Format (12 bytes):
        - Bytes 0-1: Company ID (0xFFFF for testing/custom)
        - Byte 2: Data format version (0x01)
        - Bytes 3-4: Temperature in 0.01°C (sint16)
        - Bytes 5-6: Humidity in 0.01% (uint16)
        - Bytes 7-10: Pressure in 0.1 Pa (uint32)
        - Byte 11: Battery level 0-100% (uint8)
        """
        
        # Build manufacturer data
        mfg_data = bytearray()
        
        # Company ID (0xFFFF = test/custom)
        mfg_data.extend(struct.pack('<H', 0xFFFF))
        
        # Format version
        mfg_data.append(0x01)
        
        # Temperature (sint16, 0.01°C)
        if temperature is not None:
            temp_int = int(temperature * 100)
            mfg_data.extend(struct.pack('<h', temp_int))
        else:
            mfg_data.extend(b'\x00\x00')
        
        # Humidity (uint16, 0.01%)
        if humidity is not None:
            humid_int = int(humidity * 100)
            mfg_data.extend(struct.pack('<H', humid_int))
        else:
            mfg_data.extend(b'\x00\x00')
        
        # Pressure (uint32, 0.1 Pa)
        if pressure is not None:
            press_int = int(pressure * 10)
            mfg_data.extend(struct.pack('<I', press_int))
        else:
            mfg_data.extend(b'\x00\x00\x00\x00')
        
        # Battery level (placeholder - always 100% for now)
        mfg_data.append(100)
        
        # Build complete advertisement payload
        adv_data = bytearray()
        
        # Flags
        adv_data.extend(struct.pack('BBB', 2, _ADV_TYPE_FLAGS, 0x06))
        
        # Complete name
        name = config.DEVICE_NAME.encode('utf-8')
        adv_data.extend(struct.pack('BB', len(name) + 1, _ADV_TYPE_NAME))
        adv_data.extend(name)
        
        # Manufacturer data
        adv_data.extend(struct.pack('BB', len(mfg_data) + 1, _ADV_TYPE_MANUFACTURER))
        adv_data.extend(mfg_data)
        
        # Start advertising with data
        self.ble.gap_advertise(
            config.BLE_ADVERTISING_INTERVAL_MS * 1000,  # interval in microseconds
            adv_data=bytes(adv_data)
        )
        
        if config.DEBUG_BLE:
            print(f"[BLE] Advertising: T={temperature}°C H={humidity}% P={pressure/100:.1f}hPa")
    
    def stop_advertising(self):
        """Stop BLE advertising"""
        self.ble.gap_advertise(None)
        if config.DEBUG_BLE:
            print("[BLE] Advertising stopped")
    
    def deinit(self):
        """Cleanup and deactivate BLE"""
        self.stop_advertising()
        self.ble.active(False)
        if config.DEBUG_BLE:
            print("[BLE] Advertiser deactivated")
