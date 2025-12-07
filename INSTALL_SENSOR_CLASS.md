# Installing Custom Sensor Class for bt-sensors-plugin-sk

## Option 1: Via SSH to Raspberry Pi

1. **SSH to your Raspberry Pi:**
   ```bash
   ssh pi@10.42.0.1
   ```

2. **Navigate to sensor_classes directory:**
   ```bash
   cd ~/.signalk/node_modules/bt-sensors-plugin-sk/sensor_classes/
   ```

3. **Create the ESP32SignalK.js file:**
   ```bash
   nano ESP32SignalK.js
   ```

4. **Copy the contents from the ESP32SignalK.js file we created**

5. **Save and exit** (Ctrl+X, Y, Enter)

6. **Restart SignalK:**
   ```bash
   sudo systemctl restart signalk
   ```

## Option 2: Via File Transfer

1. **Copy ESP32SignalK.js to Raspberry Pi:**
   ```powershell
   scp ESP32SignalK.js pi@10.42.0.1:~/
   ```

2. **SSH to Pi and move file:**
   ```bash
   ssh pi@10.42.0.1
   sudo mv ~/ESP32SignalK.js ~/.signalk/node_modules/bt-sensors-plugin-sk/sensor_classes/
   sudo systemctl restart signalk
   ```

## Option 3: Manual - Edit on Pi

SSH to Pi and create the file manually using the content from ESP32SignalK.js

## After Installation

1. Restart SignalK server
2. Open plugin configuration
3. You should now see "ESP32SignalK" in the sensor class dropdown
4. Select it for your device
5. Configure paths and save

## Simpler Alternative: Don't Use Sensor Class

Since you selected **RuuviTag**, try this instead:

### Change Sensor Class to "None" or Remove It
1. In the plugin config, scroll to "Sensor Class"
2. Clear or deselect RuuviTag
3. Keep "Use GATT connection" checked
4. Keep your paths as-is
5. Save

The plugin may work better reading raw GATT characteristics without trying to match RuuviTag's data format.
