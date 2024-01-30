
import time

fan_status = 'off'

def turn_fan_on():
    global fan_status
    fan_status = 'on'
    print("Fan is ON")

def turn_fan_off():
    global fan_status
    fan_status = 'off'
    print("Fan is OFF")

def get_fan_status():
    global fan_status
    return fan_status

def run_fan_for_5_minutes():
    global fan_status
    if fan_status == 'on':
        print("Fan is running for 5 minutes")
        time.sleep(300)  # Sleep for 5 minutes (300 seconds)
        print("Fan stopped")
        fan_status = 'off'
