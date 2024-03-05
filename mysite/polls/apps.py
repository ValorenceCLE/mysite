from django.apps import AppConfig
import threading
import os
import logging
from polls.utils.aht10 import collect_and_insert_aht10_data
from polls.utils.router_power import collect_and_insert_router_power_data
from polls.utils.pi_info import get_serial_number


class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'

    def ready(self):
        logging.info("Starting app polls")

        from .utils.device_checks import check_and_update_device_model
        devices_info = [
            {"type": "router", "ip_address": "192.168.1.1"},
            {"type": "camera", "ip_address": "192.168.1.3"}
        ]
        community_string = 'public'
        for device in devices_info:
            check_and_update_device_model(device["type"], device["ip_address"], community_string)

        if os.environ.get('RUN_MAIN') or os.environ.get('WERKZEUG_RUN_MAIN'):
            serial_number = get_serial_number()
            if serial_number:
                # Start AHT10 data collection thread
                sensor_id_aht10 = serial_number + 'aht10'
                threading.Thread(target=collect_and_insert_aht10_data, args=(sensor_id_aht10,),
                                 kwargs={'batch_interval': 60, 'sleep_duration': 3}, daemon=True).start()

                # Start Router_Power collection thread
                sensor_id_router = serial_number + 'INA260Router'
                threading.Thread(target=collect_and_insert_router_power_data, args=(sensor_id_router,),
                                 kwargs={'batch_interval': 60, 'sleep_duration': 3}, daemon=True).start()
