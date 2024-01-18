import nmap
import subprocess


def scan_network(network_ip):
    nm = nmap.PortScanner()
    nm.scan(hosts=network_ip, arguments='-sn')  # -sn flag for host discovery

    devices = []

    for host in nm.all_hosts():
        if 'mac' in nm[host]['addresses']:
            device = {
                'ip': host,
                'mac': nm[host]['addresses']['mac'],
                'vendor': nm[host]['vendor'],
            }
            devices.append(device)

    return devices


def run_speed_test(device_ip):
    try:
        result = subprocess.check_output(['speedtest-cli', '--simple'], universal_newlines=True)
        lines = result.split('\n')
        if len(lines) >= 3:
            ping = lines[0].split()[-2]
            download_speed = lines[1].split()[1]
            upload_speed = lines[2].split()[1]
            return ping, download_speed, upload_speed
    except Exception as e:
        return None, None, None


if __name__ == "__main__":
    network_ip = "192.168.1.0/24"  # Replace with your network IP range
    devices = scan_network(network_ip)

    print("Devices on the network:")

    for device in devices:
        print(f"IP: {device['ip']}, MAC: {device['mac']}, Vendor: {device['vendor']}")

    print("\nRunning speed tests on specific devices:")
    for device in devices:
        device_ip = device['ip']
        if device_ip == '192.168.1.1':
            print("Checking Router:")
            ping, download_speed, upload_speed = run_speed_test(device_ip)
            if ping and download_speed and upload_speed:
                print(f"Router IP: {device_ip}")
                print(f"Ping: {ping} ms")
                print(f"Download Speed: {download_speed} Mbps")
                print(f"Upload Speed: {upload_speed} Mbps")
            else:
                print(f"Speed test for Router ({device_ip}) failed.")
        elif device_ip == '192.168.1.3':
            print("Checking Camera:")
            ping, download_speed, upload_speed = run_speed_test(device_ip)
            if ping and download_speed and upload_speed:
                print(f"Camera IP: {device_ip}")
                print(f"Ping: {ping} ms")
                print(f"Download Speed: {download_speed} Mbps")
                print(f"Upload Speed: {upload_speed} Mbps")
            else:
                print(f"Speed test for Camera ({device_ip}) failed.")

        print()
