import socket
import psutil  

class MachineInfo:
    def __init__(self):
        # Retrieve hostname and network interface information
        self.hostname = socket.gethostname()
        self.interfaces = psutil.net_if_addrs()
    
    def get_hostname(self):
        # Return the hostname of the local machine
        return self.hostname
    
    def get_ip_addresses(self):
        # Return IPv4 addresses for each network interface
        ip_dict = {}
        for interface_name, addresses in self.interfaces.items():
            ip_list = []
            for addr in addresses:
                if addr.family == socket.AF_INET:  # Filter IPv4 addresses
                    ip_list.append(addr.address)
            if ip_list:
                ip_dict[interface_name] = ip_list
        return ip_dict
    
    def display_info(self):
        # Print hostname and network interfaces with their IP addresses
        # This output meets the project documentation requirements
        print(f"\nHostname: {self.get_hostname()}")
        print("Network Interfaces & IPs:")
        ip_dict = self.get_ip_addresses()
        for iface, ips in ip_dict.items():
            print(f"  {iface}: {', '.join(ips)}")