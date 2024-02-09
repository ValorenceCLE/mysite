from pysnmp.hlapi import *

# Define SNMP parameters
target_host = '192.168.1.1'  # Replace with your router's IP address
community_string = 'public'  # Replace with your SNMP community string

# Define OIDs for bandwidth monitoring (These OIDs may need adjustment depending on your device)
in_octets_oid = ObjectIdentity('1.3.6.1.2.1.2.2.1.10.1')  # Incoming traffic in octets
out_octets_oid = ObjectIdentity('1.3.6.1.2.1.2.2.1.16.1')  # Outgoing traffic in octets

# SNMP query function
def get_bandwidth_usage():
    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in getCmd(SnmpEngine(),
                             CommunityData(community_string),
                             UdpTransportTarget((target_host, 161)),
                             ContextData(),
                             ObjectType(in_octets_oid),
                             ObjectType(out_octets_oid),
                             lookupMib=False):

        if errorIndication:
            print(f"SNMP Error: {errorIndication}")
            return None

        if errorStatus:
            print(f"SNMP Error: {errorStatus}")
            return None

        # Extract and calculate bandwidth usage
        in_octets, out_octets = varBinds
        in_octets = int(in_octets[1])
        out_octets = int(out_octets[1])

        # Convert octets to Mbps (1 byte = 8 bits, 1 Mbps = 1,000,000 bits)
        in_mbps = (in_octets * 8) / 1e6
        out_mbps = (out_octets * 8) / 1e6

        return in_mbps, out_mbps

# Get and print bandwidth usage
bandwidth = get_bandwidth_usage()
if bandwidth:
    in_mbps, out_mbps = bandwidth
    print(f"Incoming Bandwidth: {in_mbps:.2f} Mbps")
    print(f"Outgoing Bandwidth: {out_mbps:.2f} Mbps")
