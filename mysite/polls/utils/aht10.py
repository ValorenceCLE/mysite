import logging
import time
from django.utils import timezone
import smbus2
import sys
import os
import django
from .pi_info import get_raspberry_pi_id

logging.basicConfig(level=logging.INFO)
#sys.path.append('/home/admin/project/mysite/mysite')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')


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
        temperature_f = temperature_c * 9 / 5 + 32
        return round(temperature_f, 1)


def collect_and_insert_aht10_data(sensor_id_aht10, batch_interval=60, sleep_duration=3):
    from polls.models import Environmental
    sensor = AHT10()
    raspberry_pi_id = get_raspberry_pi_id()
    if raspberry_pi_id is None:
        logging.error("Raspberry Pi ID not found. Terminating")
        return

    timezone.activate('America/Denver')

    while True:
        batch_start_time = time.time()
        data_points = []

        while time.time() - batch_start_time < batch_interval:
            humidity = sensor.read_humidity()
            temperature = sensor.read_temperature()
            data_point = {
                'Date_Time': timezone.localtime().replace(microsecond=0),
                'Temperature':temperature,
                'Humidity': humidity,
                'SensorID': sensor_id_aht10,
                'raspberry_pi_id': raspberry_pi_id,
            }
            data_points.append(data_point)
            time.sleep(sleep_duration)

        if data_points:
            Environmental.objects.bulk_create([Environmental(**dp) for dp in data_points])
            logging.info(f"Inserted batch of {len(data_points)} data points into the database")
