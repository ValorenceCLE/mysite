import time
import board
import adafruit_ina260
import logging
from django.utils import timezone
import os
import sys
import json
import django
from .pi_info import get_raspberry_pi_id, get_serial_number

FILE_PATH = '/home/admin/mysite/mysite/polls/project_data/system_models.json'
router_model_cache = None

logging.basicConfig(level=logging.INFO)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')


class INA260Router:
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


def load_router_model():
    global router_model_cache
    if router_model_cache is not None:
        return router_model_cache

    try:
        with open(FILE_PATH, 'r') as file:
            devices = json.load(file)
            router_info = devices.get("router_192.168.1.1", {})
            router_model_cache = router_info.get('model', "")
    except Exception as e:
        print(f"Failed to load router model: {e}")
        router_model_cache = "Unknown"
    return router_model_cache


def collect_and_insert_router_power_data(sensor_id_router, batch_interval=60, sleep_duration=3):
    from polls.models import Router_Power
    sensor = INA260Router()
    raspberry_pi_id = get_raspberry_pi_id()
    if raspberry_pi_id is None:
        logging.error("Raspberry Pi ID not found. Terminating")
        return

    router_model = load_router_model()
    timezone.activate('America/Denver')

    while True:
        batch_start_time = time.time()
        data_points = []

        while time.time() - batch_start_time < batch_interval:
            volts = sensor.get_voltage_volts()
            watts = sensor.get_power_watts()
            amps = sensor.get_current_amps()
            data_point = {
                'Date_Time': timezone.localtime().replace(microsecond=0),
                'Volts': volts,
                'Watts': watts,
                'Amps': amps,
                'Sensor_ID': sensor_id_router,
                'Router_Model': router_model,
            }
            data_points.append(data_point)
            time.sleep(sleep_duration)

        if data_points:
            Router_Power.objects.bulk_create([Router_Power(**dp) for dp in data_points])
            logging.info(f"Inserted batch of {len(data_points)} Router Power data points into the database")

