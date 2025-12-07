"""
ESP32 to SignalK BLE Bridge - Configuration
============================================
Central configuration for BLE services, device settings, and sensor parameters.
"""

# Device Information
DEVICE_NAME = "ESP32-SK"  # Shortened to fit in 31-byte BLE advertisement limit
DEVICE_VERSION = "0.1.0"

# BLE Configuration
# Note: These UUIDs should match the bt-sensors-plugin-sk requirements
# TODO: Research exact UUIDs required by the plugin

# Generic Environmental Sensing Service UUID (standard)
ENV_SENSING_SERVICE_UUID = 0x181A  # Environmental Sensing Service

# Standard BLE Characteristic UUIDs
TEMPERATURE_CHAR_UUID = 0x2A6E     # Temperature
HUMIDITY_CHAR_UUID = 0x2A6F        # Humidity  
PRESSURE_CHAR_UUID = 0x2A6D        # Pressure

# Custom UUIDs (if needed)
# Generate your own: https://www.uuidgenerator.net/
CUSTOM_SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CUSTOM_DATA_CHAR_UUID = "12345678-1234-5678-1234-56789abcdef1"

# BLE Settings
BLE_ADVERTISING_INTERVAL_MS = 100  # Milliseconds between advertisements
BLE_CONNECTION_INTERVAL_MS = 50    # Preferred connection interval
BLE_MTU = 23                        # Maximum Transmission Unit (default BLE is 23)

# Sensor Configuration
SENSOR_UPDATE_INTERVAL_MS = 1000   # How often to read sensors (milliseconds)
SENSOR_TYPES = {
    'temperature': True,            # Enable temperature sensor
    'humidity': True,               # Enable humidity sensor
    'pressure': True,               # Enable pressure sensor
    'voltage': False,               # Enable voltage monitoring
}

# I2C Configuration (for sensors like BME280)
I2C_SCL_PIN = 22                   # I2C Clock pin
I2C_SDA_PIN = 21                   # I2C Data pin
I2C_FREQ = 400000                  # I2C frequency (Hz)

# Sensor Calibration
TEMPERATURE_OFFSET = 0.0           # Degrees Celsius to add/subtract
PRESSURE_OFFSET = 0.0              # hPa to add/subtract
HUMIDITY_OFFSET = 0.0              # Percentage to add/subtract

# Power Management
DEEP_SLEEP_ENABLED = False         # Enable deep sleep between readings
DEEP_SLEEP_DURATION_MS = 60000     # Deep sleep duration (if enabled)
LOW_POWER_MODE = False             # Reduce CPU frequency to save power

# Debug Settings
DEBUG = True                       # Enable debug output
DEBUG_BLE = True                   # Extra verbose BLE debugging
DEBUG_SENSORS = True               # Extra verbose sensor debugging

# SignalK Mapping (for reference - handled by plugin)
# These show where data will appear in SignalK
SIGNALK_PATHS = {
    'temperature': 'environment.inside.temperature',
    'humidity': 'environment.inside.humidity',
    'pressure': 'environment.outside.pressure',
    'voltage': 'electrical.batteries.house.voltage',
}

# Connection Settings
MAX_RECONNECT_ATTEMPTS = 10        # Max attempts before giving up
RECONNECT_DELAY_MS = 5000          # Delay between reconnect attempts

# LED Indicators (optional - if you have LEDs)
LED_PIN = 2                        # Built-in LED pin (ESP32 usually pin 2)
LED_ENABLED = True                 # Enable LED status indicators
LED_BLE_CONNECTED_PATTERN = 'slow_blink'   # LED pattern when BLE connected
LED_BLE_DISCONNECTED_PATTERN = 'fast_blink' # LED pattern when disconnected

# Error Handling
SENSOR_ERROR_RETRY_COUNT = 3       # Retry sensor reading on error
HALT_ON_CRITICAL_ERROR = False     # Stop execution on critical errors

# Data Formatting
TEMPERATURE_PRECISION = 2          # Decimal places for temperature
HUMIDITY_PRECISION = 1             # Decimal places for humidity
PRESSURE_PRECISION = 1             # Decimal places for pressure
VOLTAGE_PRECISION = 2              # Decimal places for voltage

# Mock Data (for testing without real sensors)
USE_MOCK_SENSORS = False           # Use simulated sensor data
MOCK_TEMPERATURE_RANGE = (20.0, 25.0)  # Min, Max for random temp
MOCK_HUMIDITY_RANGE = (40.0, 60.0)     # Min, Max for random humidity
MOCK_PRESSURE_RANGE = (1010.0, 1020.0) # Min, Max for random pressure

def print_config():
    """Print current configuration (for debugging)"""
    if not DEBUG:
        return
        
    print("=" * 50)
    print("ESP32-SignalK BLE Bridge Configuration")
    print("=" * 50)
    print(f"Device Name: {DEVICE_NAME}")
    print(f"Version: {DEVICE_VERSION}")
    print(f"BLE Advertising Interval: {BLE_ADVERTISING_INTERVAL_MS}ms")
    print(f"Sensor Update Interval: {SENSOR_UPDATE_INTERVAL_MS}ms")
    print(f"Enabled Sensors: {[k for k, v in SENSOR_TYPES.items() if v]}")
    print(f"Mock Sensors: {USE_MOCK_SENSORS}")
    print(f"Debug Mode: {DEBUG}")
    print("=" * 50)
