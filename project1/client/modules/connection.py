import socket
from .set_server_address import SetServerAddress

class Connection:
    def __init__(self):
        """
        Initialize Connection:
        - Uses SetServerAddress to get server IP and port
        - Creates a TCP socket for communication
        """
        self.address_manager = SetServerAddress()
        self.server_ip = self.address_manager.set_server_ip()
        self.server_port = self.address_manager.set_server_port()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        """
        Connect to the server using the provided IP and port.
        Returns the connected socket object.
        """
        try:
            print(f"Connecting to {self.server_ip}:{self.server_port} ...")
            self.client_socket.connect((self.server_ip, self.server_port))
            print("Connected to server.")
            return self.client_socket
        except Exception as e:
            print(f"Client Error: {e}")

    def close(self):
        """
        Close the socket connection and notify the user.
        """
        self.client_socket.close()
        print("Connection closed.")