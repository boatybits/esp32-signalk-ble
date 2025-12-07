# Commands to Run on Raspberry Pi

## Copy the sensor class file and restart SignalK:

```bash
# Copy file to sensor_classes directory
sudo cp ~/ESP32SignalK.js ~/.signalk/node_modules/bt-sensors-plugin-sk/sensor_classes/ESP32SignalK.js

# Restart SignalK
sudo systemctl restart signalk
```

## Wait about 30 seconds for SignalK to restart, then:

1. Go back to the BT Sensors plugin configuration
2. The "ESP32SignalK (unknown)" error should be gone
3. You should see proper configuration fields for temperature, humidity, pressure
4. Configure the paths and save
5. Check the Data Browser for incoming sensor data

## If you need to check SignalK logs:
```bash
sudo journalctl -u signalk -f
```
