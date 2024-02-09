import Adafruit_ADS1x15
import time

# Create an ADS1115 ADC (16-bit) instance explicitly specifying the I2C bus number.
i2c_bus = 1  # Most Raspberry Pi models use bus 1, but older models might use bus 0.
adc = Adafruit_ADS1x15.ADS1115(busnum=i2c_bus)

# Gain settings for ADS1115
# - 2/3 = +/-6.144V
# -   1 = +/-4.096V
# -   2 = +/-2.048V
# -   4 = +/-1.024V
# -   8 = +/-0.512V
# -  16 = +/-0.256V
# Choose a gain that matches the expected voltage range from the ACS723.
GAIN = 1

# The ACS723 outputs a voltage proportional to the current measured.
# Vcc is typically 5V or 3.3V, and the output is centered around Vcc/2.
# The sensitivity (mV/A) depends on your specific ACS723 model (e.g., 40mV/A for ACS723LLCTR-40AU).
# Adjust these values based on your ACS723 model and supply voltage.
Vcc = 5.0  # Supply voltage to ACS723
sensitivity = 40.0  # Sensitivity in mV/A
Voffset = Vcc / 2  # Voltage offset (Vcc/2)

def read_current():
    # Read the ADC channel where the ACS723 output is connected (e.g., channel 0)
    # The ADS1115 value ranges from -32768 to 32767 (16-bit)
    # Convert this value back to voltage by multiplying by the voltage range and dividing by the max value.
    value = adc.read_adc(0, gain=GAIN)
    voltage = value * (4.096 / 32767)  # Example for GAIN=1 (+/-4.096V)

    # Calculate the current based on the ACS723 sensitivity and offset.
    # The current is the voltage difference from the offset, divided by the sensitivity, adjusted for the mV to V conversion.
    current = (voltage - Voffset) / (sensitivity / 1000)

    return current

if __name__ == "__main__":
    try:
        while True:
            current = read_current()
            print(f"Current: {current:.3f} A")
            time.sleep(1)  # Read every second
    except KeyboardInterrupt:
        print("Program terminated by user.")
