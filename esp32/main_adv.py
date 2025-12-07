"""
ESP32 to SignalK BLE Bridge - Main Entry Point (Advertisement Version)
======================================================================
Broadcasts sensor data via BLE advertisements instead of GATT.
"""

import time
from machine import Pin
import gc

# Import project modules
import config
from ble_advertiser import BLEAdvertiser
from sensor_handler import SensorHandler

# LED for status indication (if available)
led = None
if config.LED_ENABLED:
    try:
        led = Pin(config.LED_PIN, Pin.OUT)
    except:
        print("[MAIN] LED not available")
        led = None

def blink_led(times=1, delay_ms=100):
    """Blink LED for status indication"""
    if led is None:
        return
    for _ in range(times):
        led.on()
        time.sleep_ms(delay_ms)
        led.off()
        time.sleep_ms(delay_ms)

def main():
    """Main application loop"""
    
    # Print configuration
    print("\n" + "="*50)
    print("ESP32 to SignalK BLE Bridge (Advertisement Mode)")
    print("="*50)
    config.print_config()
    
    # Startup blink
    blink_led(3, 200)
    
    # Initialize components
    print("[MAIN] Initializing BLE advertiser...")
    ble_advertiser = BLEAdvertiser()
    
    print("[MAIN] Initializing sensor handler...")
    sensor_handler = SensorHandler()
    
    print("[MAIN] System ready! Broadcasting sensor data...")
    print("="*50 + "\n")
    
    # Main loop
    last_update = time.ticks_ms()
    
    try:
        while True:
            current_time = time.ticks_ms()
            
            # Update sensor data and advertisement at configured interval
            if time.ticks_diff(current_time, last_update) >= config.SENSOR_UPDATE_INTERVAL_MS:
                last_update = current_time
                
                # Read all sensors
                readings = sensor_handler.read_all()
                
                # Validate readings
                if not sensor_handler.validate_all_readings(readings):
                    print("[MAIN] WARNING: Some sensor readings are out of range")
                
                # Broadcast via BLE advertisements
                ble_advertiser.advertise_sensor_data(
                    temperature=readings.get('temperature'),
                    humidity=readings.get('humidity'),
                    pressure=readings.get('pressure')
                )
                
                # LED blink to show activity
                if led:
                    led.on()
                    time.sleep_ms(50)
                    led.off()
                
                # Garbage collection to prevent memory issues
                gc.collect()
                
                if config.DEBUG:
                    print(f"[MAIN] Free memory: {gc.mem_free()} bytes")
            
            # Small delay to prevent busy waiting
            time.sleep_ms(100)
            
    except KeyboardInterrupt:
        print("\n[MAIN] Keyboard interrupt - shutting down...")
    except Exception as e:
        print(f"[MAIN] ERROR: {e}")
        import sys
        sys.print_exception(e)
    finally:
        # Cleanup
        print("[MAIN] Cleaning up...")
        ble_advertiser.deinit()
        if led:
            led.off()
        print("[MAIN] Shutdown complete")

# Run main program
if __name__ == "__main__":
    main()
