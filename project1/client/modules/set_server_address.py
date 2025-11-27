import subprocess
import re

class SetServerAddress:
    def __init__(self):
        """
        Initialize server IP and port placeholders.
        """
        self.server_ip = None
        self.server_port = None

    def list_network_ips(self):
        """
        List all IPs in the local network using 'arp -a'.
        Returns a list of discovered IP addresses.
        """
        print("Scanning local network for IPs...")
        try:
            result = subprocess.run(["arp", "-a"], capture_output=True, text=True)
            ips = re.findall(r"\d+\.\d+\.\d+\.\d+", result.stdout)
            for i, ip in enumerate(ips, 1):
                print(f"{i}. {ip}")
            return ips
        except Exception as e:
            print(f"Error listing network IPs: {e}")
            return []

    def set_server_ip(self):
        """
        Prompt the user to enter a valid server IP.
        Optionally lists network IPs for convenience.
        """
        while True:
            choice = input("Do you want to list all IPs in the network first? (y/n): ").strip().lower()
            if choice == "y":
                self.list_network_ips()

            ip = input("Enter the server IP to use: ").strip()

            if not re.match(r"\d+\.\d+\.\d+\.\d+", ip):
                print("Invalid IP format. Try again.")
                continue

            try:
                # Allow localhost
                if ip == "127.0.0.1" or ip.lower() == "localhost":
                    self.server_ip = ip
                    print(f"Server IP set to: {self.server_ip}")
                    break

                # Verify IP exists in the network
                result = subprocess.run(["arp", "-a"], capture_output=True, text=True)
                ips_in_network = re.findall(r"\d+\.\d+\.\d+\.\d+", result.stdout)
                if ip in ips_in_network:
                    self.server_ip = ip
                    print(f"Server IP set to: {self.server_ip}")
                    break
                else:
                    print("This IP is not found in the network. Try again or list the network IPs.")
            except Exception as e:
                print(f"Error checking network IPs: {e}")

        return self.server_ip

    def set_server_port(self):
        """
        Prompt the user to enter a valid server port number (1-65535).
        """
        while True:
            port_input = input("Enter the server Port to use: ").strip()

            if not port_input.isdigit():
                print("Invalid port number. Must be numeric.")
                continue

            port = int(port_input)

            if not (0 < port < 65536):
                print("Invalid port range. Port number must be between 1 and 65535.")
                continue

            self.server_port = port
            print(f"Server port set to: {self.server_port}")
            break

        return self.server_port