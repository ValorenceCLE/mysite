from django.core.management.base import BaseCommand
import schedule
import time as wait
import csv
from datetime import datetime, timedelta
import speedtest


class Command(BaseCommand):
    help = 'Execute Speed Checks'

    def handle(self, *args, **kwargs):
        # Define the paths for CSV files
        router_csv_path = 'mysite/polls/static/router_speed.csv'
        camera_csv_path = 'mysite/polls/static/camera_speed.csv'

        def format_timestamp(timestamp):
            # Format the timestamp as ISO 8601 string
            return timestamp.strftime('%Y-%m-%dT%H:%M:%S')

        def individual_speed_test(device_ip, csv_path):
            try:
                servers = ['speedtest.example.com', 'speedtest1.example.com', 'speedtest2.example.com']

                for server in servers:
                    st = speedtest.Speedtest()
                    st.get_best_server()
                    st.get_best_server()

                    download_speed = round(st.download() / 10 ** 6, 2)  # Convert to Mbps and round to 2 decimal places
                    upload_speed = round(st.upload() / 10 ** 6, 2)  # Convert to Mbps and round to 2 decimal places

                    # Get the current timestamp
                    timestamp = datetime.now()

                    # Format the timestamp as ISO 8601 string
                    iso_timestamp = format_timestamp(timestamp)

                    #Print the results to the console
                    print(f"{device_ip} Speed Test - {iso_timestamp}")
                    print(f"Download: {download_speed:.2f} Mbps")
                    print(f"Upload: {upload_speed:.2f} Mbps")

                    # Save the results to a CSV file for the device
                    with open(csv_path, 'a', newline='') as csvfile:
                        fieldnames = ['Timestamp', 'Download (Mbps)', 'Upload (Mbps)']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                        # Write the header row if the file is empty
                        if csvfile.tell() == 0:
                            writer.writeheader()

                        # Write the results to the CSV
                        writer.writerow(
                            {'Timestamp': iso_timestamp, 'Download (Mbps)': download_speed,
                             'Upload (Mbps)': upload_speed})

                    # Break out of the loop if the test was successful
                    break

            except Exception as e:
                print(f"An error occurred in {device_ip} Speed Test: {e}")

        def cleanup_csv_files():
            # Define a function to clean up CSV files
            two_days_ago = datetime.now() - timedelta(days=2)

            def remove_old_entries(csv_file):
                with open(csv_file, 'r') as file:
                    rows = list(csv.DictReader(file))
                rows = [row for row in rows if
                        datetime.strptime(row['Timestamp'], '%Y-%m-%dT%H:%M:%S') >= two_days_ago]
                with open(csv_file, 'w', newline='') as file:
                    fieldnames = ['Timestamp', 'Download (Mbps)', 'Upload (Mbps)']
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)

            remove_old_entries(router_csv_path)
            remove_old_entries(camera_csv_path)

        # Schedule speed tests for the router and camera every 1 minute (adjust as needed)
        schedule.every(1).minutes.do(individual_speed_test, "192.168.1.1", router_csv_path)
        schedule.every(1).minutes.do(individual_speed_test, "192.168.1.3", camera_csv_path)

        # Schedule CSV cleanup every day at 3:00 AM (adjust as needed)
        schedule.every(1).days.at('03:00').do(cleanup_csv_files)

        while True:
            schedule.run_pending()
            wait.sleep(1)

            # Call other management commands here if needed
            # call_command('another_command_name', '--option=value')  # Example of calling another command

        # Indicate successful execution of the custom command
        self.stdout.write(self.style.SUCCESS('Successfully ran my custom command'))
