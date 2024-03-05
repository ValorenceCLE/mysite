import RPi.GPIO as GPIO
import time
import threading

GPIO.setwarnings(False)

# Define GPIO pins for your devices
CAMERA_PIN = 17
FAN_PIN = 27
STROBE_PIN = 5
ROUTER_PIN = 13

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(CAMERA_PIN, GPIO.OUT)
GPIO.setup(FAN_PIN, GPIO.OUT)
GPIO.setup(STROBE_PIN, GPIO.OUT)
GPIO.setup(ROUTER_PIN, GPIO.OUT)
GPIO.output(ROUTER_PIN, GPIO.HIGH)

# Create a dictionary to store locks for each GPIO
gpio_locks = {
    CAMERA_PIN: threading.Lock(),
    FAN_PIN: threading.Lock(),
    STROBE_PIN: threading.Lock(),
    ROUTER_PIN: threading.Lock(),
}

# Function to control GPIO asynchronously
def control_gpio(pin, action):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

    # Acquire the lock for the GPIO
    with gpio_locks[pin]:
        if action == 'On':
            GPIO.output(pin, GPIO.HIGH)
        elif action == 'Off':
            GPIO.output(pin, GPIO.LOW)
        elif action == 'RouterReset':
            GPIO.output(pin, GPIO.LOW)
            time.sleep(10)  # Keep the router reset for 10 seconds
            GPIO.output(pin, GPIO.HIGH)

# Turn on the camera
def turn_on_camera():
    threading.Thread(target=control_gpio, args=(CAMERA_PIN, 'On')).start()

# Turn off the camera
def turn_off_camera():
    threading.Thread(target=control_gpio, args=(CAMERA_PIN, 'Off')).start()

# Turn on the fan
def turn_on_fan():
    threading.Thread(target=control_gpio, args=(FAN_PIN, 'On')).start()

# Turn off the fan
def turn_off_fan():
    threading.Thread(target=control_gpio, args=(FAN_PIN, 'Off')).start()

# Turn on the strobe
def turn_on_strobe():
    threading.Thread(target=control_gpio, args=(STROBE_PIN, 'On')).start()

# Turn off the strobe
def turn_off_strobe():
    threading.Thread(target=control_gpio, args=(STROBE_PIN, 'Off')).start()


def reset_router():
    threading.Thread(target=control_gpio, args=(ROUTER_PIN, 'RouterReset')).start()


# Turn on the fan for 5 minutes
def run_fan_for_5_minutes():
    control_gpio(FAN_PIN, 'On')
    threading.Timer(300, control_gpio, args=(FAN_PIN, 'Off')).start()

# Turn on the strobe for 5 minutes
def run_strobe_for_5_minutes():
    control_gpio(STROBE_PIN, 'On')
    threading.Timer(300, control_gpio, args=(STROBE_PIN, 'Off')).start()

# Get camera state
def get_camera_state():
    return GPIO.input(CAMERA_PIN)

# Get fan state
def get_fan_state():
    return GPIO.input(FAN_PIN)

# Get strobe state
def get_strobe_state():
    return GPIO.input(STROBE_PIN)

# Get router state
def get_router_state():
    return GPIO.input(ROUTER_PIN)

# Cleanup GPIO on program exit
def cleanup_gpio():
    GPIO.cleanup()
