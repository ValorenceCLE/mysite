import logging


def get_serial_number():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if line.startswith('Serial'):
                    return line.split(':')[-1].strip()
    except IOError:
        logging.error("Could not read /proc/cpuinfo. Ensure this script is run on a Raspberry Pi.")
        return None

def get_raspberry_pi_id():
    from polls.models import Raspberry_Pi
    raspberry_pi = Raspberry_Pi.objects.first()
    if raspberry_pi:
        return raspberry_pi.id
    raise Exception("No Raspberry_Pi instance found in the database.")

