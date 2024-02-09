# aht10_sensor.py
import smbus2
import time

class AHT10:
    def __init__(self, i2c_bus=1, address=0x38):
        self.bus = smbus2.SMBus(i2c_bus)
        self.address = address
        self.init_sensor()

    def init_sensor(self):
        self.bus.write_i2c_block_data(self.address, 0xE1, [0x08, 0x00])
        time.sleep(0.02)

    def _read_raw_data(self):
        self.bus.write_i2c_block_data(self.address, 0xAC, [0x33, 0x00])
        time.sleep(0.5)
        return self.bus.read_i2c_block_data(self.address, 0x00, 6)

    def read_humidity(self):
        data = self._read_raw_data()
        humidity = round(((data[1] << 12) | (data[2] << 4) | (data[3] >> 4)) * 100 / 1048576, 1)
        return humidity

    def read_temperature(self):
        data = self._read_raw_data()
        temperature_c = (((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]) * 200 / 1048576 - 50
        temperature_f = temperature_c * 9/5 + 32
        return round(temperature_f, 1)

if __name__ == "__main__":
    sensor = AHT10()
    try:
        while True:
            humidity = sensor.read_humidity()
            temperature = sensor.read_temperature()
            print(f"Humidity: {humidity}% Temperature: {temperature}°F")
            time.sleep(3)
    except KeyboardInterrupt:
        print("Program terminated by user.")
        sensor.bus.close()
