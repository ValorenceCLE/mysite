import nmap
import requests


## BELOW CODE IS TO RETRIVE CLIENT LIST ##

# Function to perform a MAC address lookup and retrieve device names
def get_device_name(mac_address):
    # Use a MAC address lookup API (You can replace with your preferred API)
    mac_lookup_url = f"https://api.macvendors.com/{mac_address}"
    try:
        response = requests.get(mac_lookup_url)
        if response.status_code == 200:
            return response.text.strip()  # Remove leading/trailing whitespaces
        else:
            return "Unknown Device"
    except Exception as e:
        print(f"Error fetching MAC address information: {e}")
        return "Unknown Device"

def scan_local_network(ip_range):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_range, arguments='-sn')

    client_list = []
    for host in nm.all_hosts():
        if 'mac' in nm[host]['addresses']:
            ip_address = host
            mac_address = nm[host]['addresses']['mac']
            name = get_device_name(mac_address)
            client_list.append({'ip': ip_address, 'mac': mac_address, 'name': name})

    return client_list

# Define the IP range for your local network (adjust as needed)
network_ip_range = "192.168.1.0/24"  # Example: for a /24 subnet

# Perform the network scan and retrieve the client list
clients = scan_local_network(network_ip_range)

# Display the list of clients with names obtained from MAC address lookup
if clients:
    print("IP Address\tMAC Address\tDevice Name")
    for client in clients:
        print(f"{client['ip']}\t{client['mac']}\t{client['name']}")
else:
    print("No devices found on the local network.")
