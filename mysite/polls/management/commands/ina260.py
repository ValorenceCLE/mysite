import time
import board
import adafruit_ina260

class INA260Sensor:
    def __init__(self):
        i2c = board.I2C()  # Setup I2C connection
        self.ina260 = adafruit_ina260.INA260(i2c)  # Initialize INA260 sensor

    def get_current_amps(self):
        # Get current in Amps, with one decimal place
        return round(self.ina260.current / 1000, 1)  # Convert mA to A and round

    def get_voltage_volts(self):
        # Get voltage in Volts, with one decimal place
        return round(self.ina260.voltage, 1)

    def get_power_watts(self):
        # Get power in Watts, with one decimal place
        return round(self.ina260.power / 1000, 1)  # Convert mW to W and round

    def print_measurements(self):
        while True:
            try:
                current_A = self.get_current_amps()
                voltage_V = self.get_voltage_volts()
                power_W = self.get_power_watts()
                print(f"Current: {current_A} A, Voltage: {voltage_V} V, Power: {power_W} W")
                time.sleep(3)
            except OSError:
                print("Failed to read sensor data. Check the sensor connection.")
                break

if __name__ == "__main__":
    sensor = INA260Sensor()
    sensor.print_measurements()
