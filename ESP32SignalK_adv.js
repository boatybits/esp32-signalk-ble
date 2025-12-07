const BTSensor = require("../BTSensor");

class ESP32SignalK extends BTSensor {
    static manufacturerID = 0xFFFF;
    static Domain = BTSensor.SensorDomains.environmental;
    static Manufacturer = "ESP32";

    static async identify(device) {
        // Identify by manufacturer ID to avoid GATT connection
        if (await this.getManufacturerID(device) == this.manufacturerID) {
            return this;
        }
        return null;
    }

    hasGATT() {
        return false;  // Using advertisements, not GATT
    }

    usingGATT() {
        return false;
    }

    initSchema() {
        super.initSchema();
        this.addDefaultParam("zone");

        // Get manufacturer data buffer
        const md = this.valueIfVariant(this.getManufacturerData(this.constructor.manufacturerID));
        
        if (!md || md.length < 10) {
            throw new Error("ESP32-SK: Invalid or missing manufacturer data");
        }

        // Temperature: sint16, units of 0.01°C, convert to Kelvin  
        // Buffer: [0:Ver][1-2:Temp][3-4:Humid][5-8:Press][9:Batt]
        this.addDefaultPath("temperature", "environment.temperature")
        .read=(buffer)=> buffer && buffer.length >= 3 ? parseFloat((273.15 + buffer.readInt16LE(1)/100.0).toFixed(2)) : null

        // Humidity: uint16, units of 0.01%, convert to ratio (0-1)
        this.addDefaultPath("humidity", "environment.humidity")
        .read=(buffer)=> buffer && buffer.length >= 5 ? parseFloat((buffer.readUInt16LE(3)/10000.0).toFixed(4)) : null

        // Pressure: uint32, units of 0.1 Pa
        this.addDefaultPath("pressure", "environment.pressure")
        .read=(buffer)=> buffer && buffer.length >= 9 ? parseFloat((buffer.readUInt32LE(5)/10.0).toFixed(1)) : null

        return this;
    }

    propertiesChanged(props) {
        super.propertiesChanged(props);
        if (props.ManufacturerData) {
            this.emitValuesFrom(this.getManufacturerData(this.constructor.manufacturerID));
        }
    }
}

module.exports = ESP32SignalK;
