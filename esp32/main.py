"""
ESP32 to SignalK BLE Bridge - Main Entry Point
===============================================
Orchestrates BLE server and sensor data transmission.
"""

import time
from machine import Pin
import gc

# Import project modules
import config
from ble_server import BLEServer
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

def led_pattern(pattern):
    """Display LED pattern based on connection state"""
    if led is None:
        return
    
    if pattern == 'slow_blink':
        led.on()
        time.sleep_ms(1000)
        led.off()
    elif pattern == 'fast_blink':
        led.on()
        time.sleep_ms(200)
        led.off()
    elif pattern == 'on':
        led.on()
    elif pattern == 'off':
        led.off()

def main():
    """Main application loop"""
    
    # Print configuration
    print("\n" + "="*50)
    print("ESP32 to SignalK BLE Bridge")
    print("="*50)
    config.print_config()
    
    # Startup blink
    blink_led(3, 200)
    
    # Initialize components
    print("[MAIN] Initializing BLE server...")
    ble_server = BLEServer()
    
    print("[MAIN] Initializing sensor handler...")
    sensor_handler = SensorHandler()
    
    # Start BLE advertising
    print("[MAIN] Starting BLE advertising...")
    ble_server.start_advertising()
    
    print("[MAIN] System ready! Waiting for connection...")
    print("="*50 + "\n")
    
    # Main loop
    last_update = time.ticks_ms()
    connection_reported = False
    
    try:
        while True:
            current_time = time.ticks_ms()
            
            # Check connection status
            if ble_server.is_connected():
                if not connection_reported:
                    print("[MAIN] BLE client connected!")
                    connection_reported = True
                    blink_led(2, 100)
                
                # LED pattern for connected state
                if config.LED_ENABLED:
                    led_pattern(config.LED_BLE_CONNECTED_PATTERN)
            else:
                if connection_reported:
                    print("[MAIN] BLE client disconnected")
                    connection_reported = False
                
                # LED pattern for disconnected state
                if config.LED_ENABLED:
                    led_pattern(config.LED_BLE_DISCONNECTED_PATTERN)
            
            # Update sensor data at configured interval
            if time.ticks_diff(current_time, last_update) >= config.SENSOR_UPDATE_INTERVAL_MS:
                last_update = current_time
                
                # Read all sensors
                readings = sensor_handler.read_all()
                
                # Validate readings
                if not sensor_handler.validate_all_readings(readings):
                    print("[MAIN] WARNING: Some sensor readings are out of range")
                
                # Update BLE characteristics
                if 'temperature' in readings and readings['temperature'] is not None:
                    ble_server.update_temperature(readings['temperature'])
                
                if 'humidity' in readings and readings['humidity'] is not None:
                    ble_server.update_humidity(readings['humidity'])
                
                if 'pressure' in readings and readings['pressure'] is not None:
                    ble_server.update_pressure(readings['pressure'])
                
                # Garbage collection to prevent memory issues
                gc.collect()
                
                if config.DEBUG:
                    print(f"[MAIN] Free memory: {gc.mem_free()} bytes")
            
            # Small delay to prevent busy waiting
            time.sleep_ms(10)
            
    except KeyboardInterrupt:
        print("\n[MAIN] Keyboard interrupt - shutting down...")
    except Exception as e:
        print(f"[MAIN] ERROR: {e}")
        import sys
        sys.print_exception(e)
    finally:
        # Cleanup
        print("[MAIN] Cleaning up...")
        ble_server.deinit()
        if led:
            led.off()
        print("[MAIN] Shutdown complete")

# Run main program
if __name__ == "__main__":
    main()
