"""
Sensor Handler
==============
Manages sensor reading, data validation, and mock data generation.
"""

import time
import random
from machine import Pin, I2C

import config

class SensorHandler:
    """Handles sensor data acquisition and processing"""
    
    def __init__(self):
        self.use_mock = config.USE_MOCK_SENSORS
        self.i2c = None
        self.sensors = {}
        
        if not self.use_mock:
            self._init_real_sensors()
        
        if config.DEBUG_SENSORS:
            mode = "MOCK" if self.use_mock else "REAL"
            print(f"[SENSOR] Handler initialized ({mode} mode)")
    
    def _init_real_sensors(self):
        """Initialize real hardware sensors"""
        try:
            # Initialize I2C bus
            self.i2c = I2C(0, 
                          scl=Pin(config.I2C_SCL_PIN), 
                          sda=Pin(config.I2C_SDA_PIN),
                          freq=config.I2C_FREQ)
            
            # Scan for devices
            devices = self.i2c.scan()
            if config.DEBUG_SENSORS:
                print(f"[SENSOR] I2C devices found: {[hex(d) for d in devices]}")
            
            # Initialize specific sensors
            # TODO: Add actual sensor initialization here
            # Example: self.sensors['bme280'] = BME280(self.i2c)
            
            if not devices:
                print("[SENSOR] WARNING: No I2C devices found, falling back to mock mode")
                self.use_mock = True
                
        except Exception as e:
            print(f"[SENSOR] ERROR initializing sensors: {e}")
            print("[SENSOR] Falling back to mock mode")
            self.use_mock = True
    
    def read_temperature(self):
        """Read temperature from sensor or generate mock data
        
        Returns:
            float: Temperature in Celsius
        """
        try:
            if self.use_mock:
                # Generate mock temperature
                min_temp, max_temp = config.MOCK_TEMPERATURE_RANGE
                temp = random.uniform(min_temp, max_temp)
            else:
                # TODO: Read from actual sensor
                # Example: temp = self.sensors['bme280'].temperature
                temp = 22.0  # Placeholder
            
            # Apply calibration offset
            temp += config.TEMPERATURE_OFFSET
            
            # Apply precision formatting
            temp = round(temp, config.TEMPERATURE_PRECISION)
            
            return temp
            
        except Exception as e:
            print(f"[SENSOR] ERROR reading temperature: {e}")
            return None
    
    def read_humidity(self):
        """Read humidity from sensor or generate mock data
        
        Returns:
            float: Relative humidity (0-100%)
        """
        try:
            if self.use_mock:
                # Generate mock humidity
                min_hum, max_hum = config.MOCK_HUMIDITY_RANGE
                humidity = random.uniform(min_hum, max_hum)
            else:
                # TODO: Read from actual sensor
                # Example: humidity = self.sensors['bme280'].humidity
                humidity = 50.0  # Placeholder
            
            # Apply calibration offset
            humidity += config.HUMIDITY_OFFSET
            
            # Clamp to valid range
            humidity = max(0.0, min(100.0, humidity))
            
            # Apply precision formatting
            humidity = round(humidity, config.HUMIDITY_PRECISION)
            
            return humidity
            
        except Exception as e:
            print(f"[SENSOR] ERROR reading humidity: {e}")
            return None
    
    def read_pressure(self):
        """Read pressure from sensor or generate mock data
        
        Returns:
            float: Pressure in Pascals
        """
        try:
            if self.use_mock:
                # Generate mock pressure (in hPa, then convert to Pa)
                min_press, max_press = config.MOCK_PRESSURE_RANGE
                pressure_hpa = random.uniform(min_press, max_press)
                pressure_pa = pressure_hpa * 100  # Convert hPa to Pa
            else:
                # TODO: Read from actual sensor
                # Example: pressure_pa = self.sensors['bme280'].pressure
                pressure_pa = 101325.0  # Placeholder (standard atmosphere)
            
            # Apply calibration offset (in Pa)
            pressure_pa += (config.PRESSURE_OFFSET * 100)
            
            # Apply precision formatting
            pressure_pa = round(pressure_pa, config.PRESSURE_PRECISION)
            
            return pressure_pa
            
        except Exception as e:
            print(f"[SENSOR] ERROR reading pressure: {e}")
            return None
    
    def read_all(self):
        """Read all enabled sensors
        
        Returns:
            dict: Dictionary with sensor readings
        """
        readings = {}
        
        if config.SENSOR_TYPES.get('temperature', False):
            readings['temperature'] = self.read_temperature()
        
        if config.SENSOR_TYPES.get('humidity', False):
            readings['humidity'] = self.read_humidity()
        
        if config.SENSOR_TYPES.get('pressure', False):
            readings['pressure'] = self.read_pressure()
        
        if config.DEBUG_SENSORS:
            print(f"[SENSOR] Readings: {readings}")
        
        return readings
    
    def validate_reading(self, value, min_val, max_val):
        """Validate sensor reading is within expected range
        
        Args:
            value: Reading value
            min_val: Minimum valid value
            max_val: Maximum valid value
            
        Returns:
            bool: True if valid, False otherwise
        """
        if value is None:
            return False
        return min_val <= value <= max_val
    
    def validate_all_readings(self, readings):
        """Validate all sensor readings
        
        Args:
            readings: Dictionary of sensor readings
            
        Returns:
            bool: True if all readings valid
        """
        valid = True
        
        if 'temperature' in readings:
            # Valid temperature range: -40°C to 85°C (typical sensor range)
            if not self.validate_reading(readings['temperature'], -40, 85):
                print(f"[SENSOR] WARNING: Invalid temperature: {readings['temperature']}")
                valid = False
        
        if 'humidity' in readings:
            # Valid humidity range: 0-100%
            if not self.validate_reading(readings['humidity'], 0, 100):
                print(f"[SENSOR] WARNING: Invalid humidity: {readings['humidity']}")
                valid = False
        
        if 'pressure' in readings:
            # Valid pressure range: 30000-110000 Pa (300-1100 hPa)
            if not self.validate_reading(readings['pressure'], 30000, 110000):
                print(f"[SENSOR] WARNING: Invalid pressure: {readings['pressure']}")
                valid = False
        
        return valid


# Sensor driver examples (to be implemented when real sensors are added)

class BME280:
    """BME280 Temperature, Humidity, Pressure sensor driver
    TODO: Implement actual BME280 driver or import library
    """
    def __init__(self, i2c, addr=0x76):
        self.i2c = i2c
        self.addr = addr
        # TODO: Initialize sensor
    
    @property
    def temperature(self):
        # TODO: Read temperature
        return 22.0
    
    @property
    def humidity(self):
        # TODO: Read humidity
        return 50.0
    
    @property
    def pressure(self):
        # TODO: Read pressure (in Pa)
        return 101325.0


class DS18B20:
    """DS18B20 Temperature sensor driver
    TODO: Implement actual DS18B20 driver or import library
    """
    def __init__(self, pin):
        self.pin = pin
        # TODO: Initialize sensor
    
    def read_temp(self):
        # TODO: Read temperature
        return 22.0
