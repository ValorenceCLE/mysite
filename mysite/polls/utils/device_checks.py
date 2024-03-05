import json
import os
from pysnmp.hlapi import *

MODEL_OID = '.1.3.6.1.2.1.1.1.0'
FILE_PATH = '/home/admin/mysite/mysite/polls/project_data/system_models.json'


def get_device_model(ip_address, community_string='public'):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community_string, mpModel=0),
        UdpTransportTarget((ip_address, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(MODEL_OID))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
    if errorIndication or errorStatus:
        print(f"Error: {errorIndication or errorStatus.prettyPrint()}")
        return None
    else:
        for varBind in varBinds:
            return varBind[1].prettyPrint()


def check_and_update_device_model(device_type, ip_address, community_string='public'):
    # Ensure directory exists
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

    try:
        with open(FILE_PATH, 'r') as file:
            devices = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        devices = {}

    unique_key = f"{device_type}_{ip_address}"
    current_model = get_device_model(ip_address, community_string)
    if not current_model:
        print(f"Failed to retrieve model for {device_type} at {ip_address}.")
        return

    if unique_key not in devices or devices[unique_key].get('model') != current_model:
        devices[unique_key] = {'type': device_type, 'ip': ip_address, 'model': current_model}
        with open(FILE_PATH, 'w') as file:
            json.dump(devices, file, indent=4)
        print(f"Updated model for {device_type} at {ip_address} to {current_model}.")
    else:
        print(f"Model for {device_type} at {ip_address} is unchanged.")


if __name__ == '__main__':
    devices_info = [
        {"type": "router", "ip_address": "192.168.1.1"},
        {"type": "camera", "ip_address": "192.168.1.3"}
    ]
    community_string = 'public'

    for device in devices_info:
        check_and_update_device_model(device["type"], device["ip_address"], community_string)
