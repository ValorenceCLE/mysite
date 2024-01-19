import speedtest
from datetime import datetime
import csv

RouterIp = '192.168.1.1'
CameraIp = '192.168.1.3'

# Create separate Speedtest objects for router and camera
st_router = speedtest.Speedtest()
st_camera = speedtest.Speedtest()


def Router_speed_test():
    # Measure download and upload speeds
    download_speed = st_router.download() / 10 ** 6  # Convert to Mbps
    upload_speed = st_router.upload() / 10 ** 6  # Convert to Mbps

    # Get the current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Print the results to the console
    print(f"Router Speed Test - {timestamp}")
    print(f"Download: {download_speed:.2f} Mbps")
    print(f"Upload: {upload_speed:.2f} Mbps")

    # Save the results to a CSV file for the router
    with open('router_speedtest.csv', 'a', newline='') as csvfile:
        fieldnames = ['Timestamp', 'Download (Mbps)', 'Upload (Mbps)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row if the file is empty
        if csvfile.tell() == 0:
            writer.writeheader()

        # Write the results to the CSV
        writer.writerow({'Timestamp': timestamp, 'Download (Mbps)': download_speed, 'Upload (Mbps)': upload_speed})


def Camera_speed_test():
    # Measure download and upload speeds
    download_speed = st_camera.download() / 10 ** 6  # Convert to Mbps
    upload_speed = st_camera.upload() / 10 ** 6  # Convert to Mbps

    # Get the current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Print the results to the console
    print(f"Camera Speed Test - {timestamp}")
    print(f"Download: {download_speed:.2f} Mbps")
    print(f"Upload: {upload_speed:.2f} Mbps")

    # Save the results to a CSV file for the camera
    with open('camera_speedtest.csv', 'a', newline='') as csvfile:
        fieldnames = ['Timestamp', 'Download (Mbps)', 'Upload (Mbps)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row if the file is empty
        if csvfile.tell() == 0:
            writer.writeheader()

        # Write the results to the CSV
        writer.writerow({'Timestamp': timestamp, 'Download (Mbps)': download_speed, 'Upload (Mbps)': upload_speed})


# Perform speed tests
Router_speed_test()
Camera_speed_test()
