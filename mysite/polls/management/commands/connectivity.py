import pywifi
import time
import socket



def classify_signal_quality(rssi_value):
    if rssi_value > -75:
        return "Good"
    elif -75 >= rssi_value > -85:
        return "Fair"
    elif -85 >= rssi_value > -95:
        return "Poor"
    else:
        return "No signal"


def get_connected_wifi_rssi():
    wifi = pywifi.PyWiFi()  # Initialize the PyWiFi object
    iface = wifi.interfaces()[0]  # Get the first Wi-Fi interface

    connected_bssid = iface.scan_results()[0].bssid

    return connected_bssid


if __name__ == "__main__":
    connected_bssid = get_connected_wifi_rssi()

    if connected_bssid is not None:
        # Assuming the router is at 192.168.1.1
        router_ip = "192.168.1.1"

        wifi = pywifi.PyWiFi()  # Initialize the PyWiFi object
        iface = wifi.interfaces()[0]  # Get the first Wi-Fi interface

        iface.scan()  # Scan for available Wi-Fi networks

        # Wait for a few seconds to allow scanning to complete
        time.sleep(2)

        scan_results = iface.scan_results()  # Get the scan results

        for result in scan_results:
            if result.bssid == connected_bssid:
                rssi_value = result.signal
                signal_quality = classify_signal_quality(rssi_value)
                print(f"RSSI: {rssi_value} dBm ({signal_quality})")

                # You can use 'signal_quality' in your website
                # to display an appropriate indicator or message.
                if signal_quality == "Good":
                    # Display a good indicator on the website
                    print("Signal is Good - Display Good Indicator on the Website")
                elif signal_quality == "Fair":
                    # Display a fair indicator on the website
                    print("Signal is Fair - Display Fair Indicator on the Website")
                elif signal_quality == "Poor":
                    # Display a poor indicator on the website
                    print("Signal is Poor - Display Poor Indicator on the Website")
                else:
                    # Display a no signal indicator on the website
                    print("No Signal - Display No Signal Indicator on the Website")

                break
        else:
            print("Unable to retrieve RSSI")
    else:
        print("Not connected to any Wi-Fi network.")
