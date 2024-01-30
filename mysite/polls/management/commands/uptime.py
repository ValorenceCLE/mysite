from pysnmp.hlapi import *
import json
from django.http import JsonResponse

# IMPORTANT: MAKE SURE BOTH THE ROUTER AND CAMERA ARE CONFIGURED TO ACCEPT SNMP!

# Define SNMP parameters for the Router
router_snmp_target = '192.168.1.1'  # Replace with the IP address of your router
router_snmp_community = 'public'    # Replace with your SNMP community string
router_snmp_port = 161
timeout = 5
retries = 1

# Define SNMP parameters for the Camera
camera_snmp_target = '192.168.1.3'  # Replace with the IP address of your camera
camera_snmp_community = 'public'    # Replace with your SNMP community string
camera_snmp_port = 161

# Define the OIDs for sysUpTime (device uptime)
router_uptime_oid = ObjectIdentity('SNMPv2-MIB', 'sysUpTime', 0)
camera_uptime_oid = ObjectIdentity('SNMPv2-MIB', 'sysUpTime', 0)

# Function to convert uptime in hundredths of a second to human-readable format
def convert_uptime(uptime_ticks):
    uptime_seconds = uptime_ticks / 100
    uptime_minutes, uptime_seconds = divmod(uptime_seconds, 60)
    uptime_hours, uptime_minutes = divmod(uptime_minutes, 60)
    uptime_days, uptime_hours = divmod(uptime_hours, 24)
    return uptime_days, uptime_hours, uptime_minutes, uptime_seconds

def get_uptime(request, device):
    if device == "router":
        snmp_target = router_snmp_target
        snmp_community = router_snmp_community
        snmp_port = router_snmp_port
        uptime_oid = router_uptime_oid
    elif device == "camera":
        snmp_target = camera_snmp_target
        snmp_community = camera_snmp_community
        snmp_port = camera_snmp_port
        uptime_oid = camera_uptime_oid
    else:
        return JsonResponse({"error": "Invalid device specified"})

    # Create SNMP GET request
    snmp_request = getCmd(
        SnmpEngine(),
        CommunityData(snmp_community),
        UdpTransportTarget((snmp_target, snmp_port), timeout=timeout, retries=retries),
        ContextData(),
        ObjectType(uptime_oid)
    )

    # Send SNMP request and retrieve response
    error_indication, error_status, error_index, var_binds = next(snmp_request)

    uptime_data = {}
    if not error_indication and not error_status:
        uptime_ticks = int(var_binds[0][1])
        uptime_days, uptime_hours, uptime_minutes, uptime_seconds = convert_uptime(uptime_ticks)
        uptime_data = {
            "days": uptime_days,
            "hours": uptime_hours,
            "minutes": uptime_minutes,
            "seconds": uptime_seconds
        }

    response_data = {"output": uptime_data}
    return JsonResponse(response_data)

# Example usage in views.py:
# from django.http import JsonResponse
# def trigger_router_uptime_script(request):
#     return get_uptime(request, "router")

# def trigger_camera_uptime_script(request):
#     return get_uptime(request, "camera")
